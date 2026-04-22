import tkinter as tk
import ctypes
from app import XrayVoidDetector

# Windows DPI 喚醒 (解決高解析度螢幕模糊問題)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = XrayVoidDetector(root)
    root.mainloop()