# 🕵️‍♂️ Security Research Tool



![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-orange.svg)
![Build](https://img.shields.io/badge/Build-PyInstaller-yellow.svg)



A Python-based spyware simulation project built for educational and ethical hacking research. This tool demonstrates common surveillance techniques, packaged into a standalone executable using PyInstaller.

> ⚠️ **Disclaimer**: This project is for **educational purposes only**. Unauthorized surveillance is illegal and unethical. Always obtain proper consent.

---

## 🔧 Features

- 📸 Webcam access
- 🖱️ Screenshot capture
- 📂 File & directory access
- 📡 Network information logging
- 📤 Telegram bot integration for data exfiltration

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/harris9559/Spyware_tool.git
cd Spyware_tool
```

### 2. Set up Python Virtual Environment (Optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up `.env` File
Create a `.env` file with the following content:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5. Build Executable
```bash
pyinstaller --noconfirm --onefile --windowed spy.py --add-data ".env;."
```
The final executable will be found in the `dist/` folder as `spy.exe`.

---

## 🚀 One-Click Execution
Transfer the `spy.exe` to your testing machine/VM and double-click to execute. The script will silently start collecting data and sending it to your configured Telegram bot.

Note: Antivirus software may flag this executable. Always conduct your tests in isolated, controlled environments like VMs.

---

## 📁 Recommended Project Structure
```
Spyware_tool/
├── .env
├── spy.py
├── requirements.txt
├── README.md
├── .gitignore
├── dist/
├── build/
├── venv/
└── spy.spec
```

---

## 🙈 .gitignore Recommendation
Ensure the following files are excluded from version control:
```
venv/
dist/
build/
*.spec
*.exe
__pycache__/
.env
```

---

## 📄 License
This project is licensed under the MIT License. See `LICENSE` for more details.

Build by : Harshit Pandey


Github Repo: @harris9559

