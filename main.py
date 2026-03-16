import webview
import subprocess
import os
import sys
import time
import threading
import pyperclip

class Api:
    def __init__(self):
        self.current_url = ""

    def get_url(self):
        return self.current_url

    def select_folder(self):
        res = window.create_file_dialog(webview.FOLDER_DIALOG)
        return res[0] if res else None

    def download(self, url, type, quality, format, thumb, save_path):
        try:
            cmd = ["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s"]
            if type == 'audio':
                cmd.extend(["-f", "bestaudio/best", "--extract-audio", "--audio-format", format])
                cmd.extend(["--audio-quality", "320K" if quality == "best" else "128K"])
            else:
                if quality == "1080p": cmd.extend(["-f", "bestvideo[height<=1080]+bestaudio/best"])
                elif quality == "720p": cmd.extend(["-f", "bestvideo[height<=720]+bestaudio/best"])
                else: cmd.extend(["-f", "bestvideo+bestaudio/best"])
                if format != "best": cmd.extend(["--merge-output-format", format])
            if thumb: cmd.append("--embed-thumbnail")
            cmd.append(url)
            subprocess.Popen(cmd)
            return {"status": "success", "message": "Download Initiated"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def clipboard_monitor(api_instance):
    last_url = ""
    while True:
        try:
            url = pyperclip.paste().strip()
            if ("youtube.com/watch" in url or "youtu.be/" in url) and url != last_url:
                last_url = url
                api_instance.current_url = url
                window.show()
                window.restore()
                window.evaluate_js(f"document.getElementById('urlInput').value = '{url}';")
                window.evaluate_js("document.getElementById('status').innerHTML = 'TARGET DETECTED FROM CLIPBOARD';")
        except:
            pass
        time.sleep(1)

api = Api()
window = webview.create_window('HYPER-DLP', 'index.html', js_api=api, width=800, height=650, background_color='#0d0d0d', hidden=False)

if __name__ == "__main__":
    # Start clipboard listener in a separate thread
    monitor_thread = threading.Thread(target=clipboard_monitor, args=(api,), daemon=True)
    monitor_thread.start()
    webview.start()