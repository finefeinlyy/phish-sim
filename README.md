# 🛡️ Phishing Simulation Dashboard

A **phishing simulation tool** with a beautiful admin dashboard inspired by [V0 Vercel](https://v0.dev/chat), built with **Flask** and **Tailwind CSS**,.  
Perfect for demo, awareness training, or UI prototyping.

## ✨ Features

- 🔐 **Fake login & OTP forms** styled like modern SaaS apps  
- 📁 **Download logs as CSV** for credentials & OTPs  
- 💨 **No database required** – everything is saved in plain text files  
- 🧼 **Ephemeral logs** – data disappears on server restart, **safe for local testing**

## 🚀 Getting Started

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/phish-sim.git
cd phish-simulator
```
### 2. Set up Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```
### 3. Run the app
```bash
python app.py
```
Then visit http://localhost:8000 🚪

## 📁 Log Files
Captured data is saved in the logs/ folder as plain text:
- logs/captured.txt – for login credentials
- logs/otp.txt – for OTPs

## 📦 Export Options
Admin can export logs in CSV format:
- /download/credentials
- /download/otps

## 🛑 Disclaimer
This project is for educational and demonstration purposes only.
Use responsibly and do not deploy publicly without consent.
Built for internal awareness, testing, and UI exploration. No DB, no persistent tracking, safe for demo use.


