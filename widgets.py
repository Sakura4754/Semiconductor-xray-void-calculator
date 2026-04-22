import tkinter as tk

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