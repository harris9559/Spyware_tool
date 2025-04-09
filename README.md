# 🕵️ Spyware Tool (Educational Purpose Only)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Last Commit](https://img.shields.io/github/last-commit/harris9559/Spyware_tool?label=Last%20Update&color=green)

This project is a **Python-based spyware simulation tool** developed for ethical hacking research and cybersecurity education.

> ⚠️ **Disclaimer:** This tool is intended strictly for educational use and ethical testing in controlled environments. Unauthorized use on others' systems without permission is illegal.

---

## 🚀 Features

- ✅ Keystroke logging  
- 📸 Screenshot capture  
- 🎙️ Microphone audio recording  
- 📷 Webcam image capture  
- 🌍 Geolocation via IP  
- 📤 Real-time data upload to Telegram bot

---

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/harris9559/Spyware_tool.git
   cd Spyware_tool
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file with your Telegram Bot credentials:

env
Copy
Edit
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
⚙️ How it Works
On startup, the script collects system info, location, and media (audio, webcam, screenshot).

It logs keystrokes continuously and sends them to a Telegram bot at intervals or when the log size exceeds a threshold.

Audio and screenshots are recorded in the background and sent silently.

📦 Dependencies
pynput

pyautogui

opencv-python

sounddevice

soundfile

geocoder

python-dotenv

requests

Install all with:

bash
Copy
Edit
pip install -r requirements.txt
🧪 For Testing / Simulation Only
Tested on Windows 10

Make sure you run with administrator privileges if certain permissions fail

Recommended to use inside a virtual machine or isolated lab environment

📜 License
MIT License. See LICENSE file.

🤖 Developed By
Harshit Pandey
GitHub: @harris9559



