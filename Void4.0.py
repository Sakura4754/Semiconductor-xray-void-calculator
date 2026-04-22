import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
import ctypes
import os
import sys
import json
import base64

# Windows DPI 喚醒
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def img_to_base64(img):
    if img is None: return None
    success, buffer = cv2.imencode('.png', img)
    if success: return base64.b64encode(buffer).decode('utf-8')
    return None

def base64_to_img(b64_str, is_gray=True):
    if not b64_str: return None
    img_data = base64.b64decode(b64_str)
    nparr = np.frombuffer(img_data, np.uint8)
    mode = cv2.IMREAD_GRAYSCALE if is_gray else cv2.IMREAD_COLOR
    return cv2.imdecode(nparr, mode)

class CustomSlider(tk.Canvas):
    def __init__(self, parent, min_v, max_v, init_v, command, **kwargs):
        super().__init__(parent, height=24, bg="#252526", highlightthickness=0, **kwargs)
        self.min_v = min_v
        self.max_v = max_v
        self.value = init_v
        self.command = command
        
        self.bind("<Configure>", self.draw)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Button-1>", self.drag)
        self.bind("<MouseWheel>", self.wheel)
        self.bind("<Button-4>", self.wheel) 
        self.bind("<Button-5>", self.wheel) 

    def set(self, val):
        self.value = max(self.min_v, min(self.max_v, val))
        self.draw()

    def get(self):
        return self.value

    def draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1: w = 200 
        
        cy = h / 2
        self.create_rectangle(0, cy-2, w, cy+2, fill="#3e3e42", outline="")
        ratio = (self.value - self.min_v) / (self.max_v - self.min_v + 1e-9)
        px = w * ratio
        self.create_rectangle(0, cy-2, px, cy+2, fill="#007acc", outline="")
        r = 7
        self.create_oval(px-r, cy-r, px+r, cy+r, fill="#cccccc", outline="")

    def drag(self, event):
        w = self.winfo_width()
        ratio = event.x / w
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_v + ratio * (self.max_v - self.min_v)
        self.draw()
        if self.command: self.command(self.value)

    def wheel(self, event):
        d = 1 if getattr(event, 'delta', 0) > 0 or getattr(event, 'num', 0) == 4 else -1
        step = (self.max_v - self.min_v) / 20.0
        self.set(self.value + d * step)
        if self.command: self.command(self.value)
        return "break"

# 💡 核心渲染選單基底
class CustomMenuBase:
    active_menu = None

    def __init__(self, root):
        self.root = root
        self.menu_win = None
        self._just_closed = False

    def close(self, event=None):
        if self.menu_win:
            self.menu_win.destroy()
            self.menu_win = None
            self._just_closed = True
            self.root.after(100, lambda: setattr(self, '_just_closed', False))
        if CustomMenuBase.active_menu == self:
            CustomMenuBase.active_menu = None

    def _create_win(self, x, y):
        if CustomMenuBase.active_menu and CustomMenuBase.active_menu != self:
            CustomMenuBase.active_menu.close()

        CustomMenuBase.active_menu = self
        self.menu_win = tk.Toplevel(self.root)
        self.menu_win.overrideredirect(True)
        self.menu_win.configure(bg="#454545")
        
        inner = tk.Frame(self.menu_win, bg="#252526")
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        self.menu_win.focus_set()
        self.menu_win.bind("<FocusOut>", self.close)
        
        return inner

# 💡 下拉選單
class CustomDropdown(CustomMenuBase):
    def __init__(self, root, btn, get_commands_cb):
        super().__init__(root)
        self.btn = btn
        self.get_commands_cb = get_commands_cb
        self.btn.bind("<ButtonPress-1>", self.toggle)

    def toggle(self, event=None):
        if self._just_closed:
            self._just_closed = False
            return "break"
        if self.menu_win:
            self.close()
        else:
            self.show()
        return "break"

    def show(self):
        x = self.btn.winfo_rootx()
        y = self.btn.winfo_rooty() + self.btn.winfo_height()
        inner = self._create_win(x, y)
        
        commands = self.get_commands_cb()
        for label, shortcut, cmd in commands:
            if label == "-":
                tk.Frame(inner, bg="#454545", height=1).pack(fill=tk.X, padx=0, pady=4)
                continue
            
            row = tk.Frame(inner, bg="#252526")
            row.pack(fill=tk.X)
            
            lbl_l = tk.Label(row, text="    " + label, bg="#252526", fg="#cccccc", font=("Segoe UI", 10), anchor=tk.W)
            lbl_l.pack(side=tk.LEFT, pady=8)
            
            lbl_r = tk.Label(row, text=shortcut + "  ", bg="#252526", fg="#888888", font=("Segoe UI", 9), anchor=tk.E)
            lbl_r.pack(side=tk.RIGHT, pady=8, padx=(30, 0)) 
            
            def on_enter(e, r=row, ll=lbl_l, lr=lbl_r): 
                r.config(bg="#094771")
                ll.config(bg="#094771", fg="white")
                lr.config(bg="#094771", fg="white")
            def on_leave(e, r=row, ll=lbl_l, lr=lbl_r): 
                r.config(bg="#252526")
                ll.config(bg="#252526", fg="#cccccc")
                lr.config(bg="#252526", fg="#888888")
                
            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)
            lbl_l.bind("<Enter>", on_enter)
            lbl_l.bind("<Leave>", on_leave)
            lbl_r.bind("<Enter>", on_enter)
            lbl_r.bind("<Leave>", on_leave)
            
            def make_exec(c=cmd): return lambda e: self.execute(c)
            exec_cmd = make_exec()
            row.bind("<ButtonRelease-1>", exec_cmd)
            lbl_l.bind("<ButtonRelease-1>", exec_cmd)
            lbl_r.bind("<ButtonRelease-1>", exec_cmd)
            
        self.root.update_idletasks()
        self.menu_win.geometry(f"+{x}+{y}")

    def execute(self, cmd):
        self.close()
        if cmd: cmd()

# 💡 右鍵選單
class CustomContextMenu(CustomMenuBase):
    def __init__(self, root, get_items_cb, variable, command):
        super().__init__(root)
        self.get_items_cb = get_items_cb
        self.variable = variable
        self.command = command

    def show(self, x, y):
        inner = self._create_win(x, y)
        
        items = self.get_items_cb()
        for label, val in items:
            prefix = " ✔  " if self.variable.get() == val else "      "
            row = tk.Frame(inner, bg="#252526")
            row.pack(fill=tk.X)
            
            lbl = tk.Label(row, text=prefix + label + "    ", bg="#252526", fg="#cccccc", font=("Segoe UI", 10), anchor=tk.W)
            lbl.pack(side=tk.LEFT, pady=8, padx=(0, 20))
            
            def on_enter(e, r=row, l=lbl): 
                r.config(bg="#094771")
                l.config(bg="#094771", fg="white")
            def on_leave(e, r=row, l=lbl): 
                r.config(bg="#252526")
                l.config(bg="#252526", fg="#cccccc")
                
            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)
            lbl.bind("<Enter>", on_enter)
            lbl.bind("<Leave>", on_leave)
            
            def make_exec(v=val): return lambda e: self.execute(v)
            exec_cmd = make_exec()
            row.bind("<ButtonRelease-1>", exec_cmd)
            lbl.bind("<ButtonRelease-1>", exec_cmd)

        self.root.update_idletasks()
        self.menu_win.geometry(f"+{x}+{y}")

    def execute(self, val):
        self.variable.set(val)
        if self.command: self.command()
        self.close()


class XrayVoidDetector:
    def __init__(self, root):
        self.root = root
        self.win_w, self.win_h = 1350, 880
        self.root.geometry(f"{self.win_w}x{self.win_h}")
        self.root.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')

        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except: pass
        
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            value = ctypes.c_int(2)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), 4)
        except: pass

        self.root.overrideredirect(True)

        self.original_img = None      
        self.processed_img = None     
        self.processed_color = None   
        self.base_thresh_mask = None  
        self.user_mask = None         
        self.accumulated_base_mask = None 
        
        self.cached_blended_img = None
        self.current_composite_mask = None
        
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.current_sf = 1.0
        
        self.roi_pts = []
        self.current_mouse_pos = None
        self.selecting_roi = False
        self.is_dragging_roi = False
        self.drag_mode = None 
        self.drag_start_pos = (0,0)
        self.drag_start_roi = []

        self.current_void_rate = 0.0
        self.current_void_labels = []
        
        self.show_mask_var = tk.BooleanVar(value=True)
        self.save_watermark_var = tk.BooleanVar(value=True)
        self.show_void_labels_var = tk.BooleanVar(value=False)
        self.invert_img_var = tk.BooleanVar(value=False)
        self.use_clahe_var = tk.BooleanVar(value=True)
        self.solidify_var = tk.BooleanVar(value=True)
        self.tool_mode = tk.StringVar(value="PAN") 
        
        self.preview_fill_active = False
        self.preview_seed = None
        self.preview_mask = None
        self.fill_tolerance = 15

        self.labels = {}
        self.img_on_canvas = None
        self._error_shown = False
        
        self.setup_i18n()
        self.current_lang = "zh"
        self.ui_vars = {k: tk.StringVar() for k in self.i18n["zh"].keys()}
        
        self.build_custom_title_bar()
        self.setup_ui()
        self.build_menu() 
        
        self.set_language("zh")
        self.bind_shortcuts()
        self.update_cursor()
        
        self.is_maximized = False
        self.root.after(100, self.toggle_maximize) 

    def build_custom_title_bar(self):
        self.title_bar = tk.Frame(self.root, bg="#181818", height=45)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.title_bar.pack_propagate(False)

        icon_lbl = tk.Label(self.title_bar, text="💠", bg="#181818", fg="#007acc", font=("Segoe UI", 12))
        icon_lbl.pack(side=tk.LEFT, padx=12)

        self.menu_container = tk.Frame(self.title_bar, bg="#181818")
        self.menu_container.pack(side=tk.LEFT, fill=tk.Y)

        self.title_lbl = tk.Label(self.title_bar, text="X-ray void cal v4.0", bg="#181818", fg="#cccccc", font=("Segoe UI", 11))
        self.title_lbl.pack(side=tk.LEFT, expand=True)

        self.max_btn = tk.Button(self.title_bar, text=" 🗖 ", bg="#181818", fg="#cccccc", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, command=self.toggle_maximize, activebackground="#333333", activeforeground="white")
        self.max_btn.pack(side=tk.RIGHT, fill=tk.Y)

        close_btn = tk.Button(self.title_bar, text=" ✕ ", bg="#181818", fg="#cccccc", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, command=self.root.destroy, activebackground="#e81123", activeforeground="white")
        close_btn.pack(side=tk.RIGHT, fill=tk.Y)

        self.title_bar.bind("<ButtonPress-1>", self.start_move_window)
        self.title_bar.bind("<B1-Motion>", self.do_move_window)
        self.title_bar.bind("<Double-Button-1>", self.toggle_maximize)
        self.title_lbl.bind("<ButtonPress-1>", self.start_move_window)
        self.title_lbl.bind("<B1-Motion>", self.do_move_window)
        self.title_lbl.bind("<Double-Button-1>", self.toggle_maximize)

    def toggle_maximize(self, event=None):
        if self.is_maximized:
            self.root.state('normal')
            self.max_btn.config(text=" 🗖 ")
            self.is_maximized = False
        else:
            self.root.state('zoomed')
            self.max_btn.config(text=" 🗗 ")
            self.is_maximized = True

    def start_move_window(self, event):
        if self.is_maximized:
            self.toggle_maximize()
            self._x = event.x_root - self.root.winfo_x()
            self._y = event.y_root - self.root.winfo_y()
        else:
            self._x = event.x
            self._y = event.y

    def do_move_window(self, event):
        if not self.is_maximized:
            x = self.root.winfo_x() + event.x - self._x
            y = self.root.winfo_y() + event.y - self._y
            self.root.geometry(f"+{x}+{y}")

    def bind_shortcuts(self):
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.root.bind("<Alt-f>", lambda e: self.file_dropdown.toggle())
        self.root.bind("<Alt-F>", lambda e: self.file_dropdown.toggle())
        self.root.bind("<Alt-l>", lambda e: self.lang_dropdown.toggle())
        self.root.bind("<Alt-L>", lambda e: self.lang_dropdown.toggle())
        self.root.bind("<Alt-h>", lambda e: self.help_dropdown.toggle())
        self.root.bind("<Alt-H>", lambda e: self.help_dropdown.toggle())
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-O>", lambda e: self.load_image())
        self.root.bind("<Control-l>", lambda e: self.load_project())
        self.root.bind("<Control-L>", lambda e: self.load_project())
        self.root.bind("<Control-s>", lambda e: self.save_project())
        self.root.bind("<Control-S>", lambda e: self.save_project())
        self.root.bind("<Control-e>", lambda e: self.export_report())
        self.root.bind("<Control-E>", lambda e: self.export_report())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())
        self.root.bind("<Control-Q>", lambda e: self.root.destroy())

    def setup_i18n(self):
        zh_guide = (
            "【 檢測流程與基本操作 】\n\n"
            "1. 檔案載入：從左上角「檔案」讀取 X-ray 影像檔或專案檔 (.vod)。\n"
            "2. 縮放與平移：\n"
            "   • 畫面內捲動滑鼠滾輪可「無死角縮放」。\n"
            "   • 按住滑鼠中鍵 (或切換至平移模式按左鍵) 可「拖曳平移」畫面。\n"
            "3. 右鍵選單：在影像區域點擊右鍵，可快速呼叫工具列切換模式。\n\n"
            "【 參數分析與氣泡框選 】\n\n"
            "1. 框選晶片 (ROI)：切換至「📌 框選」模式，在畫面上拖曳定義檢測範圍。\n"
            "   • 將游標移至框線邊緣即可拖曳調整大小；移至框內可移動整個區塊。\n"
            "2. AI 自動最佳化：點擊面板「🤖 自動最佳化」，系統會啟動 Otsu 演算法分析背景，自動為您找到數學上最完美的氣泡切割閾值。\n"
            "3. 強制疊加遮罩：若畫面有多個亮度落差極大的區塊，可調好一區的參數後點擊「➕ 鎖定並疊加」，再調整參數抓下一區。\n\n"
            "【 手動編修工具 】\n\n"
            "1. 手動補點/擦除：切換至「🖌️ 補點」或「🧼 擦除」，可手動塗抹遺漏的氣泡或擦去雜訊。滾輪可調整畫筆尺寸。\n"
            "2. 智慧填滿 (油漆桶)：切換至「🪣 油漆」，點擊氣泡內部可自動偵測邊界並填滿。滾輪可調整填滿寬容度。\n"
            "3. 孔洞強制密合：勾選「✨ 強制填補內部孔洞」，可自動將所有甜甜圈狀、C字型的氣泡內部破洞填為實心。\n\n"
            "【 報表匯出 】\n\n"
            "1. 勾選「顯示各氣泡編號與佔比」，即可在畫面上標示所有氣泡排名與其個別空洞率。\n"
            "2. 點選「檔案 -> 匯出報表」，即可將目前的檢測框與計算數據打包儲存為高畫質 JPG 報表。"
        )

        en_guide = (
            "[ Basic Operations ]\n\n"
            "1. File Loading: Open images or project files (.vod) via the 'File' menu.\n"
            "2. Zoom & Pan:\n"
            "   • Scroll the mouse wheel to zoom dynamically.\n"
            "   • Hold the middle mouse button (or left-click in Pan mode) to drag and pan the view.\n"
            "3. Context Menu: Right-click on the image to quickly switch between tools.\n\n"
            "[ Detection & ROI ]\n\n"
            "1. Select ROI: Switch to '📌 ROI' mode and drag to define the detection area.\n"
            "   • Drag edges to resize, or drag inside the box to move the entire ROI.\n"
            "2. AI Optimization: Click '🤖 Auto Optimize'. The system utilizes Otsu's method to analyze background and automatically determines the optimal void threshold.\n"
            "3. Mask Accumulation: For unevenly exposed chips, set parameters for one region, click '➕ Lock & Add', and proceed to adjust parameters for the next region.\n\n"
            "[ Manual Editing Tools ]\n\n"
            "1. Draw / Erase: Use '🖌️ Draw' or '🧼 Erase' to manually patch missing voids or remove noise. Scroll to adjust brush size.\n"
            "2. Smart Fill: In '🪣 Fill' mode, click inside a void to fill it automatically. Scroll to adjust flood-fill tolerance.\n"
            "3. Solidify Holes: Enable '✨ Solidify Holes' to automatically fill internal gaps within doughnut-shaped or c-shaped voids.\n\n"
            "[ Exporting ]\n\n"
            "1. Enable 'Show Void Labels & %' to visualize the ranking and specific void rate of each individual bubble.\n"
            "2. Go to 'File -> Export Report' to save the current ROI and calculated data as a high-resolution JPG report."
        )

        self.i18n = {
            "zh": {
                "title_default": "X-ray void cal v4.0",
                "m_file": "檔案 (F)", "m_lang": "語言 (L)", "m_help": "說明 (H)",
                "m_open": "選擇圖檔...", 
                "m_load": "讀取專案 (.vod)...", 
                "m_save": "儲存專案 (.vod)...", 
                "m_export": "匯出報表 (.jpg)...", 
                "m_close": "關閉", 
                "m_guide": "操作說明",
                "tab_img": "影像", "tab_void": "氣泡", "tab_edit": "編修",
                "p1_title": "影像狀態與預處理", "p2_title": "智能氣泡檢測參數", "p3_title": "手動編修與檢視控制", "p4_title": "檢測數據分析",
                "chk_inv": "影像正負片反轉", "chk_clahe": "強化對比 (CLAHE)",
                "sl_destripe": "去紋平滑度 (Bilateral)", "sl_clahe_limit": "CLAHE 強度",
                "sl_zoom": "畫面縮放", "sl_sharp": "對焦銳化", "sl_alpha": "亮度/對比", "sl_gamma": "Gamma 校正",
                "sl_kernel": "提取範圍 (Kernel)", "sl_thresh": "擷取靈敏度", "sl_morph": "邊緣平滑", "sl_area": "最小氣泡面積", "sl_circ": "最小圓形度",
                "btn_ai": "自動最佳化", "btn_acc": "鎖定並疊加",
                "tb_pan": "平移", "tb_roi": "框選", "tb_draw": "補點", "tb_erase": "擦除", "tb_fill": "油漆",
                "rm_pan": "平移畫面", "rm_roi": "框選晶片", "rm_draw": "繪製補點", "rm_erase": "擦除修改", "rm_fill": "智慧填滿",
                "sl_brush": "畫筆尺寸", "chk_solid": "強制填補內部孔洞", "sl_gap": "縫隙密合度", 
                "chk_labels": "顯示各氣泡編號與佔比",
                "btn_undo": "復原", "btn_clear": "清空所有修改",
                "chk_mask": "顯示紅光", "sl_opacity": "遮罩透明度", "chk_wm": "存檔加入浮水印",
                "status_ready": "✔️ 系統就緒", "void_lbl": "Void Rate : {0:.2f} %",
                "guide_txt": zh_guide
            },
            "en": {
                "title_default": "X-ray void cal v4.0",
                "m_file": "File (F)", "m_lang": "Language (L)", "m_help": "Help (H)",
                "m_open": "Open Image...", 
                "m_load": "Load Project...", 
                "m_save": "Save Project...", 
                "m_export": "Export Report...", 
                "m_close": "Exit", 
                "m_guide": "User Guide",
                "tab_img": "Image", "tab_void": "Detect", "tab_edit": "Edit",
                "p1_title": "Image Preprocessing", "p2_title": "Detection Parameters", "p3_title": "Edit & Masking Controls", "p4_title": "Data Analysis",
                "chk_inv": "Invert (Negative)", "chk_clahe": "Enhance (CLAHE)",
                "sl_destripe": "De-stripe", "sl_clahe_limit": "CLAHE Limit",
                "sl_zoom": "Zoom", "sl_sharp": "Sharpen", "sl_alpha": "Contrast", "sl_gamma": "Gamma",
                "sl_kernel": "Kernel Size", "sl_thresh": "Sensitivity", "sl_morph": "Smooth Edges", "sl_area": "Min Area", "sl_circ": "Min Circularity",
                "btn_ai": "Auto Optimize", "btn_acc": "Lock & Add",
                "tb_pan": "Pan", "tb_roi": "ROI", "tb_draw": "Draw", "tb_erase": "Erase", "tb_fill": "Fill",
                "rm_pan": "Pan View", "rm_roi": "Select ROI", "rm_draw": "Draw (+)", "rm_erase": "Erase (-)", "rm_fill": "Smart Fill",
                "sl_brush": "Brush Size", "chk_solid": "Solidify Holes", "sl_gap": "Close Gaps",
                "chk_labels": "Show Void Labels & %",
                "btn_undo": "Undo", "btn_clear": "Clear All",
                "chk_mask": "Show Mask", "sl_opacity": "Opacity", "chk_wm": "Add Watermark",
                "status_ready": "✔️ Ready", "void_lbl": "Void Rate : {0:.2f} %",
                "guide_txt": en_guide
            }
        }
        self.i18n["zh-CN"] = self.i18n["zh"].copy()
        self.i18n["ja"] = self.i18n["en"].copy()

    def set_language(self, lang):
        self.current_lang = lang
        t = self.i18n[lang]
        if self.original_img is None:
            self.title_lbl.config(text=t["title_default"])
        for k, v in t.items():
            if k in self.ui_vars: self.ui_vars[k].set(v)
        self.build_menu()
        self.update_void_label()
        for attr, (lbl, key) in self.labels.items():
            self.on_slider_change_visual(attr, getattr(self, attr).get(), None)

    def build_menu(self):
        for widget in self.menu_container.winfo_children():
            widget.destroy()
            
        t = self.i18n[self.current_lang]
        mb_font = ("Segoe UI", 11)

        btn_file = tk.Label(self.menu_container, text=t["m_file"], bg="#181818", fg="#cccccc", font=mb_font, padx=20)
        btn_file.pack(side=tk.LEFT, fill=tk.Y)
        btn_file.bind("<Enter>", lambda e: btn_file.config(bg="#333333", fg="white"))
        btn_file.bind("<Leave>", lambda e: btn_file.config(bg="#181818", fg="#cccccc"))
        
        def get_file_cmds():
            tc = self.i18n[self.current_lang]
            return [
                (tc["m_open"], "Ctrl+O", self.load_image),
                (tc["m_load"], "Ctrl+L", self.load_project),
                ("-", "", None),
                (tc["m_save"], "Ctrl+S", self.save_project),
                (tc["m_export"], "Ctrl+E", self.export_report),
                ("-", "", None),
                (tc["m_close"], "Ctrl+Q", self.root.destroy)
            ]
        self.file_dropdown = CustomDropdown(self.root, btn_file, get_file_cmds)

        btn_lang = tk.Label(self.menu_container, text=t["m_lang"], bg="#181818", fg="#cccccc", font=mb_font, padx=20)
        btn_lang.pack(side=tk.LEFT, fill=tk.Y)
        btn_lang.bind("<Enter>", lambda e: btn_lang.config(bg="#333333", fg="white"))
        btn_lang.bind("<Leave>", lambda e: btn_lang.config(bg="#181818", fg="#cccccc"))
        
        def get_lang_cmds():
            return [
                ("繁體中文", "", lambda: self.set_language("zh")),
                ("English", "", lambda: self.set_language("en"))
            ]
        self.lang_dropdown = CustomDropdown(self.root, btn_lang, get_lang_cmds)

        btn_help = tk.Label(self.menu_container, text=t["m_help"], bg="#181818", fg="#cccccc", font=mb_font, padx=20)
        btn_help.pack(side=tk.LEFT, fill=tk.Y)
        btn_help.bind("<Enter>", lambda e: btn_help.config(bg="#333333", fg="white"))
        btn_help.bind("<Leave>", lambda e: btn_help.config(bg="#181818", fg="#cccccc"))
        
        def get_help_cmds():
            tc = self.i18n[self.current_lang]
            return [
                (tc["m_guide"], "", self.show_help)
            ]
        self.help_dropdown = CustomDropdown(self.root, btn_help, get_help_cmds)
        
        def get_context_cmds():
            tc = self.i18n[self.current_lang]
            return [
                (tc["rm_pan"], "PAN"),
                (tc["rm_roi"], "ROI"),
                (tc["rm_draw"], "DRAW"),
                (tc["rm_erase"], "ERASE"),
                (tc["rm_fill"], "FILL")
            ]
        self.custom_context_menu = CustomContextMenu(self.root, get_context_cmds, self.tool_mode, self.on_tool_change)


    def create_panel(self, parent, title_var):
        container = tk.Frame(parent, bg="#252526")
        container.pack(fill=tk.X, pady=(0, 2))
        
        # 💡 面板標題放大為 12pt
        header = tk.Label(container, textvariable=title_var, bg="#252526", fg="#cccccc", font=("Segoe UI", 12, "bold"), anchor=tk.W, padx=10, pady=6)
        header.pack(fill=tk.X)
        
        content = tk.Frame(container, bg="#252526", padx=15, pady=5)
        content.pack(fill=tk.BOTH, expand=True)
        return content

    def setup_ui(self):
        self.right_panel = tk.Frame(self.root, width=500, bg="#252526")
        self.right_panel.pack_propagate(False)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        tab_btn_frame = tk.Frame(self.right_panel, bg="#252526")
        tab_btn_frame.pack(side=tk.TOP, fill=tk.X)
        for i in range(3): tab_btn_frame.columnconfigure(i, weight=1, uniform="tab")
        
        self.tab_var = tk.StringVar(value="IMG")
        # 💡 頁籤按鈕放大為 13pt
        rb_opts = {"bg": "#2d2d2d", "fg": "#888888", "selectcolor": "#252526", "activebackground": "#333333", "activeforeground": "#cccccc", "indicatoron": False, "font": ("Segoe UI", 13), "relief": tk.FLAT, "bd": 0, "pady": 12, "cursor": "hand2"}
        
        self.btn_tab_img = tk.Radiobutton(tab_btn_frame, textvariable=self.ui_vars["tab_img"], variable=self.tab_var, value="IMG", command=self.switch_tab, **rb_opts)
        self.btn_tab_img.grid(row=0, column=0, sticky="ew")
        self.btn_tab_void = tk.Radiobutton(tab_btn_frame, textvariable=self.ui_vars["tab_void"], variable=self.tab_var, value="VOID", command=self.switch_tab, **rb_opts)
        self.btn_tab_void.grid(row=0, column=1, sticky="ew")
        self.btn_tab_edit = tk.Radiobutton(tab_btn_frame, textvariable=self.ui_vars["tab_edit"], variable=self.tab_var, value="EDIT", command=self.switch_tab, **rb_opts)
        self.btn_tab_edit.grid(row=0, column=2, sticky="ew")

        self.fixed_bottom = tk.Frame(self.right_panel, bg="#252526", padx=10, pady=10)
        self.fixed_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        p4 = self.create_panel(self.fixed_bottom, self.ui_vars["p4_title"])
        # 💡 只有這裡維持 24pt
        self.void_info = tk.Label(p4, text="-- %", font=("Segoe UI", 24, "bold"), bg="#252526", fg="#f14c4c", pady=0)
        self.void_info.pack(fill=tk.X)
        
        self.void_bar = tk.Canvas(p4, height=4, bg="#3e3e42", highlightthickness=0)
        self.void_bar.pack(fill=tk.X, pady=(5, 10))
        self.void_bar.bind("<Configure>", lambda e: self.update_void_label())
        
        # 💡 浮水印選項放大為 12pt
        tk.Checkbutton(p4, textvariable=self.ui_vars["chk_wm"], variable=self.save_watermark_var, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", activeforeground="white", cursor="hand2", relief=tk.FLAT).pack(anchor=tk.W)
        # 💡 狀態列放大為 12pt
        self.status_lbl = tk.Label(self.fixed_bottom, textvariable=self.ui_vars["status_ready"], font=("Segoe UI", 12), bg="#252526", fg="#89d185", anchor=tk.W)
        self.status_lbl.pack(side=tk.LEFT, pady=(5, 0))

        self.resizer = tk.Label(self.fixed_bottom, text="⇲", bg="#252526", fg="#666666", cursor="size_nw_se", font=("Segoe UI", 14))
        self.resizer.pack(side=tk.RIGHT, anchor=tk.SE)
        self.resizer.bind("<ButtonPress-1>", self.start_resize)
        self.resizer.bind("<B1-Motion>", self.do_resize)

        self.ctrl_canvas = tk.Canvas(self.right_panel, bg="#252526", highlightthickness=0)
        self.ctrl_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.control_frame = tk.Frame(self.ctrl_canvas, bg="#252526", padx=0, pady=5)
        self.ctrl_window = self.ctrl_canvas.create_window((0, 0), window=self.control_frame, anchor=tk.NW)
        self.control_frame.bind("<Configure>", lambda e: self.ctrl_canvas.configure(scrollregion=self.ctrl_canvas.bbox("all")))
        self.ctrl_canvas.bind("<Configure>", lambda e: self.ctrl_canvas.itemconfig(self.ctrl_window, width=e.width))

        def _on_panel_scroll(event):
            widget = self.root.winfo_containing(event.x_root, event.y_root)
            if widget:
                if str(widget).startswith(str(self.canvas_frame)) or str(widget) == str(self.canvas): return
                if str(widget).startswith(str(self.right_panel)):
                    delta = -1 if (getattr(event, 'delta', 0) > 0 or getattr(event, 'num', 0) == 4) else 1
                    self.ctrl_canvas.yview_scroll(delta, "units")
        self.root.bind_all("<MouseWheel>", _on_panel_scroll, add="+")
        self.root.bind_all("<Button-4>", _on_panel_scroll, add="+")
        self.root.bind_all("<Button-5>", _on_panel_scroll, add="+")

        self.canvas_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, cursor="cross", bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_left_click)      
        self.canvas.bind("<B1-Motion>", self.on_left_drag)       
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release) 
        self.canvas.bind("<Motion>", self.on_mouse_move)         
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)    
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)
        self.canvas.bind("<ButtonPress-2>", self.on_pan_start)   
        self.canvas.bind("<B2-Motion>", self.on_pan_move)

        self.tab_img_frame = tk.Frame(self.control_frame, bg="#252526")
        p1 = self.create_panel(self.tab_img_frame, self.ui_vars["p1_title"])
        
        toggles_frame = tk.Frame(p1, bg="#252526")
        toggles_frame.pack(fill=tk.X, pady=(0, 5))
        # 💡 按鈕放大為 12pt
        tk.Checkbutton(toggles_frame, textvariable=self.ui_vars["chk_inv"], variable=self.invert_img_var, command=self.schedule_base, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", cursor="hand2").pack(side=tk.LEFT)
        tk.Checkbutton(toggles_frame, textvariable=self.ui_vars["chk_clahe"], variable=self.use_clahe_var, command=self.schedule_base, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", cursor="hand2").pack(side=tk.LEFT, padx=(10, 0))

        self.add_slider("sl_destripe", "destripe_slider", 0, 15, 0, self.schedule_base, parent=p1)
        self.add_slider("sl_clahe_limit", "clahe_limit_slider", 1.0, 10.0, 3.0, self.schedule_base, parent=p1)
        self.add_slider("sl_zoom", "zoom_slider", 0.1, 10.0, 1.0, self.on_slider_zoom, parent=p1)
        self.add_slider("sl_sharp", "sharpen_slider", 0.0, 5.0, 0.0, self.schedule_base, parent=p1)
        self.add_slider("sl_alpha", "alpha_slider", 0.5, 3.0, 1.0, self.schedule_base, parent=p1)
        self.add_slider("sl_gamma", "gamma_slider", 0.1, 3.0, 1.0, self.schedule_base, parent=p1)

        self.tab_void_frame = tk.Frame(self.control_frame, bg="#252526")
        p2 = self.create_panel(self.tab_void_frame, self.ui_vars["p2_title"])
        self.add_slider("sl_kernel", "bh_size_slider", 11, 201, 51, self.update_base_thresh_mask, parent=p2)
        self.add_slider("sl_thresh", "bh_thresh_slider", 1, 100, 15, self.update_base_thresh_mask, parent=p2)
        self.add_slider("sl_morph", "morph_slider", 0, 15, 3, self.update_base_thresh_mask, parent=p2)
        self.add_slider("sl_area", "area_slider", 1, 500, 20, self.update_base_thresh_mask, parent=p2)
        self.add_slider("sl_circ", "circ_slider", 0.05, 1.0, 0.40, self.update_base_thresh_mask, parent=p2)
        
        btn_frame_ai = tk.Frame(p2, bg="#252526")
        btn_frame_ai.pack(fill=tk.X, pady=(15, 0))
        btn_frame_ai.columnconfigure(0, weight=1, uniform="ai_btn")
        btn_frame_ai.columnconfigure(1, weight=1, uniform="ai_btn")
        
        # 💡 AI 按鈕放大為 12pt
        tk.Button(btn_frame_ai, textvariable=self.ui_vars["btn_ai"], command=self.auto_heuristic_search, bg="#0e639c", fg="white", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, pady=8, cursor="hand2", activebackground="#1177bb", activeforeground="white").grid(row=0, column=0, sticky="ew", padx=(0, 2))
        tk.Button(btn_frame_ai, textvariable=self.ui_vars["btn_acc"], command=self.accumulate_mask, bg="#3c3c3c", fg="#cccccc", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, pady=8, cursor="hand2", activebackground="#4d4d4d", activeforeground="white").grid(row=0, column=1, sticky="ew", padx=(2, 0))

        self.tab_edit_frame = tk.Frame(self.control_frame, bg="#252526")
        p3 = self.create_panel(self.tab_edit_frame, self.ui_vars["p3_title"])
        
        toolbar = tk.Frame(p3, bg="#252526")
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 💡 工具列按鈕放大為 12pt
        rb_opts2 = {"bg": "#3c3c3c", "fg": "#cccccc", "selectcolor": "#094771", "activebackground": "#4d4d4d", "activeforeground": "white", "indicatoron": False, "font": ("Segoe UI", 12), "relief": tk.FLAT, "bd": 0, "pady": 8, "cursor": "hand2"}
        
        btn_pan = tk.Radiobutton(toolbar, textvariable=self.ui_vars["tb_pan"], variable=self.tool_mode, value="PAN", command=self.on_tool_change, **rb_opts2)
        btn_roi = tk.Radiobutton(toolbar, textvariable=self.ui_vars["tb_roi"], variable=self.tool_mode, value="ROI", command=self.on_tool_change, **rb_opts2)
        btn_fill = tk.Radiobutton(toolbar, textvariable=self.ui_vars["tb_fill"], variable=self.tool_mode, value="FILL", command=self.on_tool_change, **rb_opts2)
        btn_draw = tk.Radiobutton(toolbar, textvariable=self.ui_vars["tb_draw"], variable=self.tool_mode, value="DRAW", command=self.on_tool_change, **rb_opts2)
        btn_erase = tk.Radiobutton(toolbar, textvariable=self.ui_vars["tb_erase"], variable=self.tool_mode, value="ERASE", command=self.on_tool_change, **rb_opts2)
        
        for i in range(3): toolbar.columnconfigure(i, weight=1, uniform="tb_btn")
        
        btn_pan.grid(row=0, column=0, sticky="ew", padx=1, pady=1)
        btn_roi.grid(row=0, column=1, sticky="ew", padx=1, pady=1)
        btn_fill.grid(row=0, column=2, sticky="ew", padx=1, pady=1)
        btn_draw.grid(row=1, column=0, sticky="ew", padx=1, pady=1)
        btn_erase.grid(row=1, column=1, sticky="ew", padx=1, pady=1)
        
        self.add_slider("sl_brush", "brush_slider", 1, 100, 10, self.on_render_config_change, parent=p3)
        # 💡 選項放大為 12pt
        tk.Checkbutton(p3, textvariable=self.ui_vars["chk_solid"], variable=self.solidify_var, command=self.on_render_config_change, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", cursor="hand2", relief=tk.FLAT).pack(anchor=tk.W, pady=(5,2))
        tk.Checkbutton(p3, textvariable=self.ui_vars["chk_labels"], variable=self.show_void_labels_var, command=self.on_render_config_change, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", cursor="hand2", relief=tk.FLAT).pack(anchor=tk.W, pady=(0,5))
        self.add_slider("sl_gap", "fill_gap_slider", 0, 51, 0, self.on_render_config_change, parent=p3)
        
        edit_action_frame = tk.Frame(p3, bg="#252526")
        edit_action_frame.pack(fill=tk.X, pady=(15, 10))
        edit_action_frame.columnconfigure(0, weight=1, uniform="act_btn")
        edit_action_frame.columnconfigure(1, weight=1, uniform="act_btn")
        
        # 💡 操作按鈕放大為 12pt
        tk.Button(edit_action_frame, textvariable=self.ui_vars["btn_undo"], command=self.undo_fill, bg="#3c3c3c", fg="#cccccc", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, pady=8, cursor="hand2", activebackground="#4d4d4d").grid(row=0, column=0, sticky="ew", padx=(0, 2))
        tk.Button(edit_action_frame, textvariable=self.ui_vars["btn_clear"], command=self.clear_all, bg="#3c3c3c", fg="#cccccc", font=("Segoe UI", 12), relief=tk.FLAT, bd=0, pady=8, cursor="hand2", activebackground="#4d4d4d").grid(row=0, column=1, sticky="ew", padx=(2, 0))

        view_frame = tk.Frame(p3, bg="#252526")
        view_frame.pack(fill=tk.X, pady=(5, 0))
        # 💡 顯示紅光放大為 12pt
        tk.Checkbutton(view_frame, textvariable=self.ui_vars["chk_mask"], variable=self.show_mask_var, command=self.on_render_config_change, font=("Segoe UI", 12), bg="#252526", fg="#cccccc", selectcolor="#3c3c3c", activebackground="#252526", cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT)
        self.add_slider("sl_opacity", "opacity_slider", 0.0, 1.0, 0.7, self.on_render_config_change, parent=view_frame)

        self.switch_tab()

    def start_resize(self, event):
        self._resize_x = event.x_root
        self._resize_y = event.y_root
        self._resize_w = self.root.winfo_width()
        self._resize_h = self.root.winfo_height()

    def do_resize(self, event):
        if self.is_maximized:
            self.toggle_maximize()
            return
        new_w = max(800, self._resize_w + (event.x_root - self._resize_x))
        new_h = max(600, self._resize_h + (event.y_root - self._resize_y))
        self.root.geometry(f"{new_w}x{new_h}")

    def switch_tab(self):
        for f in [self.tab_img_frame, self.tab_void_frame, self.tab_edit_frame]: f.pack_forget()
        for btn in [self.btn_tab_img, self.btn_tab_void, self.btn_tab_edit]: btn.config(fg="#888888")
        sel = self.tab_var.get()
        if sel == "IMG":
            self.tab_img_frame.pack(fill=tk.BOTH, expand=True); self.btn_tab_img.config(fg="#ffffff")
        elif sel == "VOID":
            self.tab_void_frame.pack(fill=tk.BOTH, expand=True); self.btn_tab_void.config(fg="#ffffff")
        elif sel == "EDIT":
            self.tab_edit_frame.pack(fill=tk.BOTH, expand=True); self.btn_tab_edit.config(fg="#ffffff")
        self.root.update_idletasks()
        self.ctrl_canvas.configure(scrollregion=self.ctrl_canvas.bbox("all"))
        self.ctrl_canvas.yview_moveto(0)

    def update_void_label(self):
        txt = self.i18n[self.current_lang]["void_lbl"].format(self.current_void_rate)
        self.void_info.config(text=txt)
        self.void_bar.delete("all")
        w = self.void_bar.winfo_width()
        if w > 1:
            ratio = self.current_void_rate / 100.0
            self.void_bar.create_rectangle(0, 0, w * ratio, 4, fill="#f14c4c", outline="")

    def on_tool_change(self):
        self.cancel_preview()
        self.update_cursor()
        self.schedule_render()

    def update_cursor(self):
        mode = self.tool_mode.get()
        if mode == "PAN": self.canvas.config(cursor="hand2") 
        elif mode == "DRAW": self.canvas.config(cursor="pencil") 
        elif mode == "ERASE": self.canvas.config(cursor="X_cursor") 
        elif mode == "FILL": self.canvas.config(cursor="target")
        elif mode == "ROI": self.canvas.config(cursor="crosshair")

    def add_slider(self, key, attr, min_v, max_v, init, cmd, parent=None):
        if parent is None: parent = self.control_frame
        bg = parent.cget("bg")
        # 💡 拉桿名稱標籤放大為 12pt
        lbl = tk.Label(parent, text="", bg=bg, fg="#cccccc", font=("Segoe UI", 12))
        lbl.pack(anchor=tk.W, pady=(5, 0) if "opacity" not in key else (0,0))
        self.labels[attr] = (lbl, key)
        slider = CustomSlider(parent, min_v, max_v, init, command=lambda v, a=attr, c=cmd: self.on_slider_change(a, v, c))
        slider.pack(fill=tk.X, pady=(2, 5) if "opacity" not in key else (2,0))
        setattr(self, attr, slider)
        
        def _lbl_wheel(event): return slider.wheel(event)
        lbl.bind("<MouseWheel>", _lbl_wheel)
        lbl.bind("<Button-4>", _lbl_wheel)
        lbl.bind("<Button-5>", _lbl_wheel)

    def on_slider_change_visual(self, attr, v, cmd):
        val = float(v)
        lbl, key = self.labels[attr]
        label_str = self.i18n[self.current_lang][key]
        if attr in ['zoom_slider', 'alpha_slider', 'gamma_slider', 'opacity_slider', 'circ_slider', 'sharpen_slider', 'clahe_limit_slider']:
            lbl.config(text=f"{label_str}: {val:.2f}")
        else:
            lbl.config(text=f"{label_str}: {int(val)}")

    def on_slider_change(self, attr, v, cmd):
        self.on_slider_change_visual(attr, v, cmd)
        if cmd: cmd()

    def on_slider_zoom(self):
        if self.processed_img is not None:
            old_sf = self.current_sf
            new_sf = self.zoom_slider.get()
            self.current_sf = new_sf
            
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            if cw > 1:
                cx = cw / 2.0
                cy = ch / 2.0
                img_x = (self.cam_x + cx) / old_sf
                img_y = (self.cam_y + cy) / old_sf
                self.cam_x = img_x * new_sf - cx
                self.cam_y = img_y * new_sf - cy
            
        self.schedule_render()

    def on_render_config_change(self, *args):
        self.update_display_cache()
        self.schedule_render()

    def load_image(self):
        f = filedialog.askopenfilename()
        if f:
            try:
                with open(f, 'rb') as fp: img_data = fp.read()
                self.original_img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_GRAYSCALE)
                if self.original_img is None: return messagebox.showerror("Error", "Format Error")
                filename = os.path.basename(f)
                
                self.title_lbl.config(text=f"{filename} - X-ray void cal v4.0")
                self.canvas.delete("all")
                self.img_on_canvas = None
                
                self.roi_pts = []; self.tool_mode.set("PAN"); self.selecting_roi = False
                self.update_cursor()
                
                self.cam_x = 0.0; self.cam_y = 0.0
                self.zoom_slider.set(1.0); self.current_sf = 1.0
                self.sharpen_slider.set(0.0); self.fill_gap_slider.set(0.0)
                self.destripe_slider.set(0); self.clahe_limit_slider.set(3.0)
                
                self.root.update_idletasks()
                cw = self.canvas.winfo_width()
                ch = self.canvas.winfo_height()
                h, w = self.original_img.shape[:2]
                self.cam_x = (w - cw) / 2.0
                self.cam_y = (h - ch) / 2.0

                self.cancel_preview(); self.drawn_bounds = None
                self.update_base()
                self.tab_var.set("VOID"); self.switch_tab()
            except Exception as e: messagebox.showerror("Error", str(e))

    def load_project(self):
        f = filedialog.askopenfilename(filetypes=[("VOD Project", "*.vod")])
        if not f: return
        try:
            with open(f, 'r', encoding='utf-8') as f_vod: data = json.load(f_vod)
            self.original_img = base64_to_img(data.get('original_img'))
            self.user_mask = base64_to_img(data.get('user_mask'))
            self.accumulated_base_mask = base64_to_img(data.get('accumulated_base_mask'))
            self.roi_pts = [tuple(pt) for pt in data.get('roi_pts', [])]
            self.zoom_slider.set(data.get('zoom', 1.0)); self.current_sf = data.get('zoom', 1.0)
            self.sharpen_slider.set(data.get('sharpen', 0.0))
            self.alpha_slider.set(data.get('alpha', 1.0)); self.gamma_slider.set(data.get('gamma', 1.0))
            self.bh_size_slider.set(data.get('bh_size', 51)); self.bh_thresh_slider.set(data.get('bh_thresh', 15))
            self.morph_slider.set(data.get('morph', 3)); self.area_slider.set(data.get('area', 20))
            self.circ_slider.set(data.get('circ', 0.4)); self.opacity_slider.set(data.get('opacity', 0.7))
            self.brush_slider.set(data.get('brush', 10)); self.fill_gap_slider.set(data.get('fill_gap', 0))
            self.destripe_slider.set(data.get('destripe', 0)); self.clahe_limit_slider.set(data.get('clahe_limit', 3.0))
            self.solidify_var.set(data.get('solidify', True)); self.show_mask_var.set(data.get('show_mask', True))
            self.save_watermark_var.set(data.get('save_watermark', True)); self.invert_img_var.set(data.get('invert_img', False))
            self.use_clahe_var.set(data.get('use_clahe', True)); self.tool_mode.set(data.get('tool_mode', 'PAN'))
            self.show_void_labels_var.set(data.get('show_void_labels', False)) 
            self.selecting_roi = data.get('selecting_roi', False)
            filename = os.path.basename(f)
            
            self.title_lbl.config(text=f"{filename} - X-ray void cal v4.0")
                
            self.canvas.delete("all"); self.img_on_canvas = None; self.drawn_bounds = None
            
            self.root.update_idletasks()
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            h, w = self.original_img.shape[:2]
            self.cam_x = (w * self.current_sf - cw) / 2.0
            self.cam_y = (h * self.current_sf - ch) / 2.0
            
            self.cancel_preview(); self.update_base()
            self.status_lbl.config(text="✔️ Project Loaded", fg="#89d185")
            self.tab_var.set("EDIT"); self.switch_tab()
            self.update_cursor()
        except Exception as e: messagebox.showerror("Error", f"Failed:\n{str(e)}")

    def save_project(self):
        if self.original_img is None: return messagebox.showwarning("!", "Load image first!")
        f_p = filedialog.asksaveasfilename(defaultextension=".vod", filetypes=[("VOD Project", "*.vod")])
        if not f_p: return
        project_data = {
            'original_img': img_to_base64(self.original_img), 'user_mask': img_to_base64(self.user_mask),
            'accumulated_base_mask': img_to_base64(self.accumulated_base_mask), 'roi_pts': self.roi_pts,
            'zoom': self.zoom_slider.get(), 'sharpen': self.sharpen_slider.get(), 'alpha': self.alpha_slider.get(),
            'gamma': self.gamma_slider.get(), 'bh_size': self.bh_size_slider.get(), 'bh_thresh': self.bh_thresh_slider.get(),
            'morph': self.morph_slider.get(), 'area': self.area_slider.get(), 'circ': self.circ_slider.get(),
            'opacity': self.opacity_slider.get(), 'brush': self.brush_slider.get(), 'fill_gap': self.fill_gap_slider.get(),
            'destripe': self.destripe_slider.get(), 'clahe_limit': self.clahe_limit_slider.get(),
            'solidify': self.solidify_var.get(), 'show_mask': self.show_mask_var.get(), 'save_watermark': self.save_watermark_var.get(),
            'show_void_labels': self.show_void_labels_var.get(),
            'invert_img': self.invert_img_var.get(), 'use_clahe': self.use_clahe_var.get(), 'tool_mode': self.tool_mode.get(),
            'selecting_roi': self.selecting_roi
        }
        try:
            with open(f_p, 'w', encoding='utf-8') as f_vod: json.dump(project_data, f_vod, ensure_ascii=False)
            messagebox.showinfo("Success", "Project Saved")
        except Exception as e: messagebox.showerror("Error", str(e))

    def export_report(self):
        if self.processed_img is None or len(self.roi_pts) != 2: return messagebox.showwarning("!", "Please Select ROI first!")
        f_p = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
        if not f_p: return
        p1, p2 = self.roi_pts; x1, y1, x2, y2 = min(p1[0],p2[0]), min(p1[1],p2[1]), max(p1[0],p2[0]), max(p1[1],p2[1])
        full_m = self.get_composite_mask(); roi_c = self.processed_color[y1:y2, x1:x2].copy(); roi_m = full_m[y1:y2, x1:x2]
        
        if self.show_mask_var.get():
            rl = roi_c.copy(); rl[roi_m==255]=[255,0,0]; cv2.addWeighted(rl, self.opacity_slider.get(), roi_c, 1.0-self.opacity_slider.get(), 0, roi_c)
        
        if self.show_void_labels_var.get() and hasattr(self, 'current_void_labels'):
            roi_w = x2 - x1
            font_scale = max(0.4, min(roi_w * 0.0015, 1.0))
            th = max(1, int(font_scale * 1.5))
            for text, cx, cy in self.current_void_labels:
                tx_c, ty_c = int(cx - x1), int(cy - y1)
                (t_w, t_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, th)
                tx = int(tx_c - t_w / 2)
                ty = int(ty_c + t_h / 2)
                cv2.putText(roi_c, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), th + 2, cv2.LINE_AA)
                cv2.putText(roi_c, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 0), th, cv2.LINE_AA)

        if self.save_watermark_var.get():
            txt = f"Void rate: {(np.sum(roi_m == 255) / roi_m.size) * 100 if roi_m.size > 0 else 0:.2f}%  {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            roi_w, roi_h = x2 - x1, y2 - y1; fs = max(0.3, min(max(150, int(roi_w * 0.45)) / cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1)[0][0], 3.0))
            th = max(1, int(fs * 1.8)); (t_w, t_h), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, fs, th)
            margin = int(max(10, roi_w * 0.02)); tx, ty = max(10, roi_w - t_w - margin), max(t_h + 10, roi_h - margin)
            cv2.putText(roi_c, txt, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, fs, (0,0,0), th + max(1, int(th*0.8)), cv2.LINE_AA)
            cv2.putText(roi_c, txt, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, fs, (255,255,255), th, cv2.LINE_AA)
            
        is_success, im_buf_arr = cv2.imencode(".jpg", cv2.cvtColor(roi_c, cv2.COLOR_RGB2BGR))
        if is_success:
            with open(f_p, 'wb') as fp: fp.write(im_buf_arr.tobytes())
            messagebox.showinfo("Success", "Report Exported")

    def accumulate_mask(self):
        if self.base_thresh_mask is None: return
        if self.accumulated_base_mask is None: self.accumulated_base_mask = self.base_thresh_mask.copy()
        else: self.accumulated_base_mask = cv2.bitwise_or(self.accumulated_base_mask, self.base_thresh_mask)
        self.update_display_cache(); self.schedule_render()
        self.status_lbl.config(text="✔️ Mask Accumulated", fg="#89d185")

    def update_base(self):
        if self.original_img is None: return
        base_img = self.original_img.copy()
        if self.invert_img_var.get(): base_img = cv2.bitwise_not(base_img)
        destripe_v = int(self.destripe_slider.get())
        if destripe_v > 0:
            base_img = cv2.bilateralFilter(base_img, destripe_v, destripe_v * 2, destripe_v / 2.0)
        if self.use_clahe_var.get():
            limit = self.clahe_limit_slider.get()
            clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=(8, 8))
            base_img = clahe.apply(base_img)
        sharpen_amt = self.sharpen_slider.get()
        if sharpen_amt > 0:
            blur = cv2.GaussianBlur(base_img, (0, 0), 2.0)
            base_img = cv2.addWeighted(base_img, 1.0 + sharpen_amt, blur, -sharpen_amt, 0)
        adj = cv2.convertScaleAbs(base_img, alpha=self.alpha_slider.get(), beta=0)
        lut = np.array([((i/255.0)**(1.0/self.gamma_slider.get()))*255 for i in np.arange(0, 256)]).astype("uint8")
        self.processed_img = cv2.LUT(adj, lut)
        self.processed_color = cv2.cvtColor(self.processed_img, cv2.COLOR_GRAY2RGB)
        if self.user_mask is None or self.user_mask.shape != self.processed_img.shape:
            self.user_mask = np.zeros_like(self.processed_img)
            self.drawn_bounds = None
        self.update_base_thresh_mask()

    def update_base_thresh_mask(self):
        if self.processed_img is None: return
        bh_size = int(self.bh_size_slider.get()); bh_size += 1 if bh_size % 2 == 0 else 0
        bh_thresh = int(self.bh_thresh_slider.get())
        m_size = int(self.morph_slider.get()); min_area = float(self.area_slider.get()); min_circ = float(self.circ_slider.get())

        kernel_bh = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (bh_size, bh_size))
        extracted_img = cv2.morphologyEx(self.processed_img, cv2.MORPH_BLACKHAT, kernel_bh)
        
        if m_size > 0:
            d = min(15, m_size * 2 + 1) 
            extracted_img = cv2.bilateralFilter(extracted_img, d, d * 3, d * 3)

        _, mask = cv2.threshold(extracted_img, bh_thresh, 255, cv2.THRESH_BINARY)
            
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_mask = np.zeros_like(mask)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area: continue 
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0: continue
            if (4 * np.pi * area) / (perimeter ** 2) >= min_circ:
                cv2.drawContours(filtered_mask, [cnt], -1, 255, thickness=cv2.FILLED)

        if self.accumulated_base_mask is not None: self.base_thresh_mask = cv2.bitwise_or(filtered_mask, self.accumulated_base_mask)
        else: self.base_thresh_mask = filtered_mask
        self.update_display_cache()
        self.schedule_render()

    def auto_heuristic_search(self):
        if self.processed_img is None: return
        self.status_lbl.config(text="⌛ 幾何邊界分析中...", fg="#d7ba7d"); self.root.update()
        
        eval_area = self.processed_img
        if len(self.roi_pts) == 2:
            p1, p2 = self.roi_pts; x1, y1, x2, y2 = min(p1[0],p2[0]), min(p1[1],p2[1]), max(p1[0],p2[0]), max(p1[1],p2[1])
            eval_area = self.processed_img[y1:y2, x1:x2]
        if eval_area.size == 0: return

        bh_size = int(self.bh_size_slider.get()); bh_size += 1 if bh_size % 2 == 0 else 0
        kernel_bh = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (bh_size, bh_size))
        extracted_img = cv2.morphologyEx(eval_area, cv2.MORPH_BLACKHAT, kernel_bh)

        blurred = cv2.bilateralFilter(extracted_img, 9, 30, 30)
        otsu_thresh, _ = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        best_thresh = max(1, int(otsu_thresh * 0.85))

        self.bh_thresh_slider.set(best_thresh)
        self.morph_slider.set(2) 
        self.area_slider.set(10)
        self.circ_slider.set(0.15)
        self.update_base_thresh_mask()
        self.status_lbl.config(text=f"✔️ 邊緣精準最佳化完成 (閾值: {best_thresh})", fg="#89d185")

    def get_composite_mask(self):
        if self.base_thresh_mask is None: return None
        mask = self.base_thresh_mask.copy()
        if self.user_mask is not None:
            mask[self.user_mask == 255] = 255
            mask[self.user_mask == 128] = 0
            
        gap_size = int(self.fill_gap_slider.get())
        if gap_size > 0:
            if gap_size % 2 == 0: gap_size += 1
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (gap_size, gap_size)))
            
        if self.solidify_var.get():
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            solid_mask = np.zeros_like(mask)
            cv2.drawContours(solid_mask, contours, -1, 255, -1)
            mask = solid_mask
        return mask

    def update_display_cache(self):
        if self.processed_img is None: return
        self.current_composite_mask = self.get_composite_mask()
        self.cached_blended_img = self.processed_color.copy()
        
        display_mask = self.current_composite_mask.copy() if self.current_composite_mask is not None else None
        
        if len(self.roi_pts) == 2 and display_mask is not None:
            p1, p2 = self.roi_pts
            x1, y1 = int(min(p1[0], p2[0])), int(min(p1[1], p2[1]))
            x2, y2 = int(max(p1[0], p2[0])), int(max(p1[1], p2[1]))
            cropped_mask = np.zeros_like(display_mask)
            cropped_mask[y1:y2, x1:x2] = display_mask[y1:y2, x1:x2]
            display_mask = cropped_mask
        
        if self.show_mask_var.get() and display_mask is not None:
            rl = self.cached_blended_img.copy()
            rl[display_mask == 255] = [255, 0, 0]
            cv2.addWeighted(rl, self.opacity_slider.get(), self.cached_blended_img, 1.0 - self.opacity_slider.get(), 0, self.cached_blended_img)
            
        self.current_void_labels = []
        if len(self.roi_pts) == 2 and self.current_composite_mask is not None:
            p1, p2 = self.roi_pts
            x1, y1 = int(min(p1[0], p2[0])), int(min(p1[1], p2[1]))
            x2, y2 = int(max(p1[0], p2[0])), int(max(p1[1], p2[1]))
            m_roi = self.current_composite_mask[y1:y2, x1:x2]
            if m_roi.size > 0: 
                self.current_void_rate = (np.sum(m_roi == 255) / m_roi.size) * 100
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(m_roi, connectivity=8)
                valid_labels = [i for i in range(1, num_labels)]
                valid_labels.sort(key=lambda i: stats[i, cv2.CC_STAT_AREA], reverse=True)
                for idx, l in enumerate(valid_labels):
                    area = stats[l, cv2.CC_STAT_AREA]
                    if area == 0: continue
                    pct = (area / m_roi.size) * 100
                    cx, cy = centroids[l]
                    abs_cx = x1 + cx
                    abs_cy = y1 + cy
                    text = f"{idx+1}({pct:.1f}%)"
                    self.current_void_labels.append((text, abs_cx, abs_cy))
            else: 
                self.current_void_rate = 0.0
        else: 
            self.current_void_rate = 0.0
            
        self.update_void_label()

    def on_left_click(self, event):
        if self.original_img is None: return
        rx, ry = self.get_real_coords(event)
        
        if self.tool_mode.get() == "PAN":
            self.pan_start_x = event.x
            self.pan_start_y = event.y
            self.pan_start_cam_x = self.cam_x
            self.pan_start_cam_y = self.cam_y
            
        elif self.tool_mode.get() == "ROI":
            sf = self.current_sf
            threshold = 15 / sf 
            
            if len(self.roi_pts) == 2 and not self.selecting_roi:
                p1, p2 = self.roi_pts
                corners = [(p1, p2), ((p2[0], p1[1]), (p1[0], p2[1])), ((p1[0], p2[1]), (p2[0], p1[1])), (p2, p1)]
                for click_pt, fixed_pt in corners:
                    if np.hypot(rx - click_pt[0], ry - click_pt[1]) <= threshold:
                        self.roi_pts = [fixed_pt, (rx, ry)]; self.selecting_roi = False; self.is_dragging_roi = True; self.drag_mode = "resize"
                        return
                
                x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
                x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
                if x1 <= rx <= x2 and y1 <= ry <= y2:
                    self.is_dragging_roi = True; self.drag_mode = "move"; self.drag_start_pos = (rx, ry); self.drag_start_roi = [p1, p2]
                    return

            if len(self.roi_pts) == 1 and self.selecting_roi:
                self.roi_pts.append((rx, ry)); self.selecting_roi = False; self.is_dragging_roi = False
                p1, p2 = self.roi_pts; self.roi_pts = [(min(p1[0], p2[0]), min(p1[1], p2[1])), (max(p1[0], p2[0]), max(p1[1], p2[1]))]
                self.update_display_cache()
            else:
                self.roi_pts = [(rx, ry)]; self.selecting_roi = True; self.is_dragging_roi = True; self.drag_mode = "resize"
                
        elif self.tool_mode.get() in ["DRAW", "ERASE"]:
            v = 255 if self.tool_mode.get() == "DRAW" else 128
            cv2.circle(self.user_mask, (rx, ry), int(self.brush_slider.get()), v, -1)
            self.update_display_cache()
            
        elif self.tool_mode.get() == "FILL":
            if self.preview_fill_active:
                self.last_fill_mask = self.user_mask.copy()
                if self.preview_mask is not None: 
                    self.user_mask[self.preview_mask == 255] = 255; self.user_mask[self.preview_mask == 128] = 128
                self.cancel_preview()
                self.update_display_cache()
            else:
                curr_m = self.current_composite_mask; self.preview_fill_active, self.preview_seed = True, (rx, ry); self.fill_target_type = curr_m[ry, rx]
                self.update_fill_preview()
                
        self.schedule_render()

    def on_left_drag(self, event):
        if self.original_img is None: return
        rx, ry = self.get_real_coords(event)
        
        if self.tool_mode.get() == "PAN":
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            self.cam_x = self.pan_start_cam_x - dx
            self.cam_y = self.pan_start_cam_y - dy
            self.schedule_render()
            
        elif self.tool_mode.get() == "ROI":
            if getattr(self, 'is_dragging_roi', False):
                if getattr(self, 'drag_mode', 'resize') == "resize":
                    if len(self.roi_pts) == 1: self.roi_pts.append((rx, ry))
                    elif len(self.roi_pts) == 2: self.roi_pts[1] = (rx, ry)
                elif self.drag_mode == "move":
                    dx = rx - self.drag_start_pos[0]; dy = ry - self.drag_start_pos[1]; op1, op2 = self.drag_start_roi
                    self.roi_pts = [(op1[0]+dx, op1[1]+dy), (op2[0]+dx, op2[1]+dy)]
                self.update_display_cache()
                self.schedule_render()
                
        elif self.tool_mode.get() in ["DRAW", "ERASE"]:
            self.current_mouse_pos = (rx, ry)
            v = 255 if self.tool_mode.get() == "DRAW" else 128
            cv2.circle(self.user_mask, (rx, ry), int(self.brush_slider.get()), v, -1)
            self.update_display_cache()
            self.schedule_render()

    def on_left_release(self, event):
        if self.tool_mode.get() == "ROI" and getattr(self, 'is_dragging_roi', False):
            self.is_dragging_roi = False; self.drag_mode = None
            if len(self.roi_pts) == 2:
                p1, p2 = self.roi_pts
                if np.hypot(p2[0] - p1[0], p2[1] - p1[1]) < 5:
                    self.roi_pts = [p1]; self.selecting_roi = True
                else:
                    self.selecting_roi = False
                    self.roi_pts = [(min(p1[0], p2[0]), min(p1[1], p2[1])), (max(p1[0], p2[0]), max(p1[1], p2[1]))]
            self.update_display_cache()
            self.schedule_render()

    def render_canvas(self):
        try:
            if self.processed_img is None or not hasattr(self, 'cached_blended_img') or self.cached_blended_img is None: 
                return
            sf = self.current_sf
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            if cw < 10 or ch < 10: return
            
            cam_x_int = int(round(self.cam_x))
            cam_y_int = int(round(self.cam_y))
            
            x0 = int(np.floor(cam_x_int / sf))
            y0 = int(np.floor(cam_y_int / sf))
            x1 = int(np.ceil((cam_x_int + cw) / sf))
            y1 = int(np.ceil((cam_y_int + ch) / sf))
            
            h, w = self.processed_img.shape[:2]
            crop_x0 = max(0, min(w, x0))
            crop_y0 = max(0, min(h, y0))
            crop_x1 = max(0, min(w, x1))
            crop_y1 = max(0, min(h, y1))
            
            if crop_x1 <= crop_x0 or crop_y1 <= crop_y0:
                self.canvas.delete("all")
                self.img_on_canvas = None
                return
                
            crop_c = self.cached_blended_img[crop_y0:crop_y1, crop_x0:crop_x1].copy()
            
            if self.preview_fill_active and self.preview_mask is not None:
                crop_prev = self.preview_mask[crop_y0:crop_y1, crop_x0:crop_x1]
                crop_c[crop_prev == 255] = [0, 255, 255]
                
            target_w = int(round(crop_x1 * sf)) - int(round(crop_x0 * sf))
            target_h = int(round(crop_y1 * sf)) - int(round(crop_y0 * sf))
            
            if target_w <= 0 or target_h <= 0: return
            
            zoomed = cv2.resize(crop_c, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
            
            base_x = int(round(crop_x0 * sf))
            base_y = int(round(crop_y0 * sf))
            
            if len(self.roi_pts) >= 1:
                p1_s = (int(round(self.roi_pts[0][0]*sf)) - base_x, int(round(self.roi_pts[0][1]*sf)) - base_y)
                if len(self.roi_pts) == 2:
                    p2_s = (int(round(self.roi_pts[1][0]*sf)) - base_x, int(round(self.roi_pts[1][1]*sf)) - base_y)
                    cv2.rectangle(zoomed, p1_s, p2_s, (0, 255, 0), 3)
                elif getattr(self, 'current_mouse_pos', None) and self.tool_mode.get() == "ROI":
                    p2_s = (int(round(self.current_mouse_pos[0]*sf)) - base_x, int(round(self.current_mouse_pos[1]*sf)) - base_y)
                    cv2.rectangle(zoomed, p1_s, p2_s, (0, 255, 255), 2)
            
            if self.show_void_labels_var.get() and hasattr(self, 'current_void_labels'):
                font_scale = 0.45
                thickness = 1
                for text, cx, cy in self.current_void_labels:
                    px_s = int(round(cx * sf)) - base_x
                    py_s = int(round(cy * sf)) - base_y
                    
                    if -50 <= px_s < target_w + 50 and -50 <= py_s < target_h + 50:
                        (t_w, t_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                        tx = int(px_s - t_w / 2)
                        ty = int(py_s + t_h / 2)
                        cv2.putText(zoomed, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
                        cv2.putText(zoomed, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 0), thickness, cv2.LINE_AA)

            if getattr(self, 'current_mouse_pos', None):
                cp = (int(round(self.current_mouse_pos[0]*sf)) - base_x, int(round(self.current_mouse_pos[1]*sf)) - base_y)
                mode = self.tool_mode.get()
                if self.preview_fill_active and self.preview_seed:
                    ps = (int(round(self.preview_seed[0]*sf)) - base_x, int(round(self.preview_seed[1]*sf)) - base_y)
                    cv2.drawMarker(zoomed, ps, (0, 0, 255), cv2.MARKER_CROSS, 20, 2)
                elif mode in ["DRAW", "ERASE"]:
                    color = (0, 255, 255) if mode == "DRAW" else (255, 105, 180)
                    cv2.circle(zoomed, cp, int(self.brush_slider.get() * sf), color, 1)
                elif mode == "FILL":
                    cv2.drawMarker(zoomed, cp, (0, 255, 0), cv2.MARKER_CROSS, 15, 1)
            
            self.tk_img = ImageTk.PhotoImage(image=Image.fromarray(zoomed))
            
            place_x = base_x - cam_x_int
            place_y = base_y - cam_y_int
            
            if self.img_on_canvas is None: 
                self.img_on_canvas = self.canvas.create_image(place_x, place_y, anchor=tk.NW, image=self.tk_img)
            else: 
                self.canvas.coords(self.img_on_canvas, place_x, place_y)
                self.canvas.itemconfig(self.img_on_canvas, image=self.tk_img)
                
            self._render_pending = False
            
        except Exception as e:
            if not self._error_shown: 
                self._error_shown = True
                messagebox.showerror("Render Error", str(e))

    def get_real_coords(self, event):
        if self.processed_img is None: return 0, 0
        sf = self.current_sf
        img_x = (self.cam_x + event.x) / sf
        img_y = (self.cam_y + event.y) / sf
        return max(0, min(self.processed_img.shape[1]-1, int(img_x))), \
               max(0, min(self.processed_img.shape[0]-1, int(img_y)))

    def on_mouse_wheel(self, event):
        if self.original_img is None: return "break"
        
        d = 1 if getattr(event, 'delta', 0) > 0 or getattr(event, 'num', 0) == 4 else -1
        
        mode = self.tool_mode.get()
        if mode == "FILL" and self.preview_fill_active:
            self.fill_tolerance = max(0, min(100, self.fill_tolerance + d * 2))
            self.update_fill_preview()
            self.schedule_render()
            return "break"
        elif mode in ["DRAW", "ERASE"]:
            self.brush_slider.set(max(1, min(100, self.brush_slider.get() + d * 2)))
            if self.current_mouse_pos: self.schedule_render()
            return "break"
        else:
            old_sf = self.current_sf
            new_sf = max(0.1, min(10.0, old_sf * (1.1 if d > 0 else 0.9)))
            
            img_x = (self.cam_x + event.x) / old_sf
            img_y = (self.cam_y + event.y) / old_sf
            
            self.current_sf = new_sf
            self.zoom_slider.set(new_sf) 
            
            self.cam_x = img_x * new_sf - event.x
            self.cam_y = img_y * new_sf - event.y
            
            self.schedule_render()
            return "break"

    def update_fill_preview(self):
        if not self.preview_fill_active: return
        rx, ry = self.preview_seed
        self.preview_mask = np.zeros_like(self.user_mask)
        ff_m = np.zeros((self.processed_img.shape[0]+2, self.processed_img.shape[1]+2), np.uint8)
        flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
        cv2.floodFill(self.processed_img, ff_m, (rx, ry), 0, (self.fill_tolerance,), (self.fill_tolerance,), flags)
        self.preview_mask[ff_m[1:-1, 1:-1] == 255] = 255 if self.fill_target_type == 0 else 128

    def on_mouse_move(self, event):
        if self.original_img is None: return
        self.current_mouse_pos = self.get_real_coords(event)
        rx, ry = self.current_mouse_pos
        
        mode = self.tool_mode.get()
        if mode == "ROI":
            if len(self.roi_pts) == 2 and not self.selecting_roi:
                sf = self.current_sf
                threshold = 15 / sf
                p1, p2 = self.roi_pts
                corners = [p1, (p2[0], p1[1]), (p1[0], p2[1]), p2]
                
                if any(np.hypot(rx - pt[0], ry - pt[1]) <= threshold for pt in corners):
                    self.canvas.config(cursor="sizing")
                elif min(p1[0], p2[0]) <= rx <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= ry <= max(p1[1], p2[1]):
                    self.canvas.config(cursor="fleur")
                else:
                    self.canvas.config(cursor="crosshair")
            else:
                self.canvas.config(cursor="crosshair")
                
        if self.selecting_roi or mode in ["DRAW", "ERASE", "FILL"]:
            self.schedule_render()

    def on_right_click(self, event): 
        if self.preview_fill_active: self.cancel_preview(); self.schedule_render()
        else:
            self.custom_context_menu.show(event.x_root, event.y_root)

    def cancel_preview(self): self.preview_fill_active = False; self.preview_mask = None
    
    def undo_fill(self): 
        if getattr(self, 'last_fill_mask', None) is not None: 
            self.user_mask = self.last_fill_mask.copy()
            self.update_display_cache()
            self.schedule_render()
        
    def clear_all(self): 
        if self.user_mask is not None: self.user_mask.fill(0)
        self.accumulated_base_mask = None; self.roi_pts = []; self.selecting_roi = True  
        self.cancel_preview(); self.update_base_thresh_mask()
        
    def on_pan_start(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.pan_start_cam_x = self.cam_x
        self.pan_start_cam_y = self.cam_y
        
    def on_pan_move(self, event):
        if not hasattr(self, 'pan_start_x'): return
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.cam_x = self.pan_start_cam_x - dx
        self.cam_y = self.pan_start_cam_y - dy
        self.schedule_render()

    def schedule_render(self):
        if not getattr(self, '_render_pending', False): self._render_pending = True; self.root.after(5, self._execute_render)
    def _execute_render(self): self.render_canvas()
    
    def schedule_base(self):
        if getattr(self, 'base_timer', None): self.root.after_cancel(self.base_timer)
        self.base_timer = self.root.after(30, self.update_base)

    def show_help(self):
        help_win = tk.Toplevel(self.root)
        hw, hh = 600, 500
        
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        cx = rx + (rw - hw) // 2
        cy = ry + (rh - hh) // 2
        
        help_win.geometry(f"{hw}x{hh}+{cx}+{cy}")
        help_win.configure(bg="#1e1e1e")
        help_win.attributes('-topmost', True) 
        help_win.overrideredirect(True) 
        
        h_title_bar = tk.Frame(help_win, bg="#181818", height=35)
        h_title_bar.pack(side=tk.TOP, fill=tk.X)
        h_title_bar.pack_propagate(False)

        h_title_lbl = tk.Label(h_title_bar, text="操作說明 / User Guide", bg="#181818", fg="#cccccc", font=("Segoe UI", 10, "bold"))
        h_title_lbl.pack(side=tk.LEFT, padx=15)

        h_close_btn = tk.Button(h_title_bar, text=" ✕ ", bg="#181818", fg="#cccccc", font=("Segoe UI", 10), relief=tk.FLAT, bd=0, command=help_win.destroy, activebackground="#e81123", activeforeground="white")
        h_close_btn.pack(side=tk.RIGHT, fill=tk.Y)

        def start_move_help(event):
            help_win._offset_x = event.x_root - help_win.winfo_x()
            help_win._offset_y = event.y_root - help_win.winfo_y()
        def do_move_help(event):
            x = event.x_root - help_win._offset_x
            y = event.y_root - help_win._offset_y
            help_win.geometry(f"+{x}+{y}")
            
        h_title_bar.bind("<ButtonPress-1>", start_move_help)
        h_title_bar.bind("<B1-Motion>", do_move_help)
        h_title_lbl.bind("<ButtonPress-1>", start_move_help)
        h_title_lbl.bind("<B1-Motion>", do_move_help)

        content_txt = tk.Text(help_win, bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 10), wrap=tk.WORD, relief=tk.FLAT, padx=25, pady=20)
        content_txt.pack(fill=tk.BOTH, expand=True)
        content_txt.insert(tk.END, self.i18n[self.current_lang]["guide_txt"])
        content_txt.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = XrayVoidDetector(root)
    root.mainloop()