import tkinter as tk
from tkinter import ttk
import pyttsx3
import threading


# -------------------- TTS Engine --------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
voice_names = [v.name for v in voices]


# -------------------- GUI --------------------
root = tk.Tk()
root.title("Text To Speech")
root.geometry("820x540")
root.resizable(False, False)

# -------------------- Colors (Black Theme) --------------------
BG = "#000000"          # Pure Black
PANEL = "#111111"       # Dark Panel
FG = "#FFFFFF"          # White Text
MUTED = "#A0A0A0"       # Grey Text

ACCENT = "#2ECC71"      # Green (Speak Button)
ACCENT_HOVER = "#27AE60"

DANGER = "#E74C3C"      # Red (Stop Button)
DANGER_HOVER = "#C0392B"

ACCENT2 = "#333333"     # Dark Grey (Clear Button)
ACCENT2_HOVER = "#555555"

BORDER = "#2A2A2A"
TEXT_BG = "#1A1A1A"

root.configure(bg=BG)

style = ttk.Style(root)
try:
    style.theme_use("clam")
except Exception:
    pass

# ttk colors
style.configure("TFrame", background=BG)
style.configure("TLabelframe", background=PANEL, foreground=FG)
style.configure("TLabel", background=BG, foreground=FG)
style.configure(
    "TCombobox",
    fieldbackground="#1A1A1A",
    background="#1A1A1A",
    foreground="white",
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", "#1A1A1A")],
    background=[("readonly", "#1A1A1A")],
    foreground=[("readonly", "white")]
)
style.configure("Horizontal.TScale", background=BG)


def set_buttons_speaking(is_speaking: bool):
    # Speak disabled while speaking; Stop enabled while speaking.
    if is_speaking:
        speak_btn.configure(state="disabled", fg="#94a3b8")
        stop_btn.configure(state="normal", fg="white")
        clear_btn.configure(state="disabled", fg="#94a3b8")
        status_var.set("Now speaking…")
    else:
        speak_btn.configure(state="normal", fg="white")
        stop_btn.configure(state="disabled", fg="#94a3b8")
        clear_btn.configure(state="normal", fg="white")
        status_var.set("Ready")


# -------------------- Helpers --------------------
class HoverButton(tk.Button):
    def __init__(self, master, *, normal_bg, hover_bg, **kwargs):
        super().__init__(master, **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.default_fg = kwargs.get("fg", "white")
        self.disabled_bg = "#0b1226"

        self.configure(
            bg=normal_bg,
            activebackground=hover_bg,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _evt):
        if str(self["state"]) == "disabled":
            self.configure(bg=self.disabled_bg)
            return
        self.configure(bg=self.hover_bg)

    def _on_leave(self, _evt):
        if str(self["state"]) == "disabled":
            self.configure(bg=self.disabled_bg)
            return
        self.configure(bg=self.normal_bg)


def _run_speech(text):
    engine = pyttsx3.init()

    engine.setProperty("rate", int(speed_var.get()))
    engine.setProperty("voice", voices[voice_combo.current()].id)

    try:
        engine.say(text)
        engine.runAndWait()
    finally:
        engine.stop()
        root.after(0, lambda: set_buttons_speaking(False))
def speak():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        status_var.set("Type something first")
        return

    # UI state
    set_buttons_speaking(True)

    
    threading.Thread(target=_run_speech, args=(text,), daemon=True).start()


def stop():
    engine.stop()
    root.after(0, lambda: set_buttons_speaking(False))


def clear():
    text_box.delete("1.0", tk.END)
    status_var.set("Ready")


# -------------------- Layout --------------------
title = tk.Label(
    root,
    text="🗣 Text To Speech",
    font=("Segoe UI", 22, "bold"),
    bg=BG,
    fg=FG,
)
title.pack(pady=18)

# Main panel
panel = tk.Frame(root, bg=PANEL, bd=0)
panel.pack(padx=18, pady=12, fill="both", expand=True)

header = tk.Frame(panel, bg=PANEL)
header.pack(padx=16, pady=(16, 8), fill="x")

tk.Label(
    header,
    text="Write text below and control voice + speed.",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 11),
).pack(side="left")

status_var = tk.StringVar(value="Ready")
status_label = tk.Label(
    header,
    textvariable=status_var,
    bg=PANEL,
    fg="#00FF88" ,
    font=("Segoe UI", 11, "bold"),
)
status_label.pack(side="right")

# Text input
text_box = tk.Text(
    panel,
    font=("Segoe UI", 13),
    height=10,
    width=70,
    bg=TEXT_BG,
    fg=FG,
    insertbackground="white",
    bd=0,
    relief="flat",
    highlightthickness=2,
    highlightbackground=BORDER,
    highlightcolor="#FFFFFF",
)
text_box.pack(padx=16, pady=(8, 14), fill="x")

# Controls
controls = ttk.LabelFrame(panel, text="Voice Settings")
controls.pack(padx=16, pady=(0, 14), fill="x")

# Voice row
voice_label = ttk.Label(controls, text="Voice")
voice_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")

voice_combo = ttk.Combobox(
    controls,
    values=voice_names,
    state="readonly",
    width=35,
)
voice_combo.current(0)
voice_combo.grid(row=0, column=1, padx=12, pady=12, sticky="w")

# Speed row
speed_label = ttk.Label(controls, text="Speed")
speed_label.grid(row=1, column=0, padx=12, pady=8, sticky="w")

speed_var = tk.IntVar(value=150)
speed = tk.Scale(
    controls,
    from_=80,
    to=250,
    orient="horizontal",
    variable=speed_var,
    length=320,
    bg=PANEL,
    fg=FG,
    highlightthickness=0,
)
speed.grid(row=1, column=1, padx=12, pady=8, sticky="w")

# Buttons
btn_frame = tk.Frame(panel, bg=PANEL)
btn_frame.pack(padx=16, pady=(0, 18))

speak_btn = HoverButton(
    btn_frame,
    text="▶ Speak",
    normal_bg=ACCENT,
    hover_bg=ACCENT_HOVER,
    command=speak,
    width=14,
    state="normal",
)
speak_btn.grid(row=0, column=0, padx=10)

stop_btn = HoverButton(
    btn_frame,
    text="⏹ Stop",
    normal_bg=DANGER,
    hover_bg=DANGER_HOVER,
    command=stop,
    width=14,
    state="disabled",
)
stop_btn.grid(row=0, column=1, padx=10)

clear_btn = HoverButton(
    btn_frame,
    text="🗑 Clear",
    normal_bg=ACCENT2,
    hover_bg=ACCENT2_HOVER,
    command=clear,
    width=14,
    state="normal",
)
clear_btn.grid(row=0, column=2, padx=10)

# Optional: keyboard shortcut
root.bind("<Control-Return>", lambda _e: speak())
root.bind("<Escape>", lambda _e: stop())

set_buttons_speaking(False)
root.mainloop()

