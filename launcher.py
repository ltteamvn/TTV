import os
import sys
import threading
import subprocess
import urllib.request
import json
import ssl
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

# -------------------------------------------------
# Cấu hình version check
# -------------------------------------------------
DRIVE_FILE_ID = "1S1g5p1x6qEwP2xFZV3fMtrJRMcXyVfsq"
REMOTE_JSON_URL = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"
LOCAL_VERSION = "1.0.2"       # <-- version hiện tại của bạn
CHECK_INTERVAL_MS = 2 * 3600 * 1000  # 2 giờ

# ----------------------------------------
# 1) Bỏ prompt email của Streamlit lần đầu
# ----------------------------------------
home = Path.home() / ".streamlit"
home.mkdir(exist_ok=True)
cred = home / "credentials.toml"
if not cred.exists():
    cred.write_text("[general]\nemail=\"\"\n", encoding="utf-8")

# ----------------------------------------
# 2) Tắt developmentMode để cho phép set port
# ----------------------------------------
os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"

# ----------------------------------------
# 3) Nếu gọi với --run-streamlit thì chạy Streamlit
# ----------------------------------------
if getattr(sys, "frozen", False) and len(sys.argv) > 1 and sys.argv[1] == "--run-streamlit":
    sys.argv = [
        "streamlit", "run", "webui/Main.py",
        "--browser.gatherUsageStats=False",
        "--server.enableCORS=False",
        "--server.enableXsrfProtection=False",
        "--server.port=1998",
    ]
    from streamlit.web import cli as stcli
    sys.exit(stcli.main())

# ----------------------------------------
# 4) Cấu hình command để spawn child process
# ----------------------------------------
EXE = sys.executable
CMD = [EXE, "--run-streamlit"]


class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LTTEAM Free Video")
        base = getattr(sys, "_MEIPASS", os.getcwd())
        icon_path = os.path.join(base, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Nút Bắt đầu
        self.btn = tk.Button(self, text="Bắt đầu", command=self.start_streamlit)
        self.btn.pack(pady=10)

        # Label hiện thông báo version
        self.lbl_version = tk.Label(self, text="", fg="red")
        self.lbl_version.pack()

        # Ô log
        self.logbox = ScrolledText(self, height=20, width=80, state="disabled", wrap="word")
        self.logbox.pack(fill="both", expand=True, padx=10, pady=5)

        self.proc = None

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Khởi kiểm tra version ngay và lập lịch sau mỗi 2 giờ
        self.after(0, self.check_version)

    def log(self, msg: str):
        """Append một dòng log vào ScrolledText."""
        self.logbox.configure(state="normal")
        self.logbox.insert("end", msg + "\n")
        self.logbox.see("end")
        self.logbox.configure(state="disabled")

    def start_streamlit(self):
        """Disable nút và spawn thread chạy Streamlit."""
        self.btn.configure(state="disabled")
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        self.log("➤ Bắt đầu Streamlit trên cổng 1998…")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.proc = subprocess.Popen(
            CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            startupinfo=startupinfo,
        )
        for line in self.proc.stdout:
            self.log(line.rstrip())
        self.proc.wait()
        self.log(f"■ Streamlit đã thoát với mã {self.proc.returncode}")

    def on_closing(self):
        """Khi user đóng GUI, terminate con process nếu còn chạy."""
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=5)
            except Exception:
                pass
        self.destroy()

    def check_version(self):
        """Kiểm tra JSON version remote, chặn dùng nếu version khác."""
        try:
            # Tạo context bỏ qua kiểm tra SSL
            ctx = ssl._create_unverified_context()

            with urllib.request.urlopen(REMOTE_JSON_URL, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            remote_ver = data.get("version", "")
            if remote_ver != LOCAL_VERSION:
                self.btn.pack_forget()
                self.lbl_version.config(
                    text=(
                        f"Phiên bản mới ({remote_ver}) đã có sẵn! "
                        "Vui lòng tải bản cập nhật."
                    )
                )
                self.log(f"⚠️ Version mismatch: local={LOCAL_VERSION}, remote={remote_ver}")
                return
            else:
                self.log(f"✔️ Phiên bản hợp lệ: {LOCAL_VERSION}")
        except Exception as e:
            # nếu lỗi mạng (bao gồm SSL), vẫn cho phép dùng và log lỗi
            self.log(f"❗️ Kiểm tra version lỗi: {e}")

        # Lên lịch check lại sau 2 giờ
        self.after(CHECK_INTERVAL_MS, self.check_version)


if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
