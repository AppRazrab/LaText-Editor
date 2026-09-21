

# Hello! This is new version of LaText Editor. It is a simple text editor with a user-friendly interface and support for multiple languages. You can save and load your texts, change the appearance of the editor, and customize settings according to your preferences.
#Thanks for using LaText Editor! If you have any questions or suggestions, feel free to contact the developer.

import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

# --- ПУТИ ---
APP_DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LLTextEditor")
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.txt")
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "LLTextEditor", "saved_texts")

os.makedirs(APP_DATA_DIR, exist_ok=True)
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# --- ЗАГРУЗКА НАСТРОЕК ---
current_lang, current_theme = "English", "Dark"
if os.path.exists(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                if lines[0] in ["English", "Русский", "Украинский"]: current_lang = lines[0]
                if lines[1] in ["Light", "Dark"]: current_theme = lines[1]
    except Exception:
        pass

ctk.set_appearance_mode(current_theme)

app = ctk.CTk()
app.geometry("490x360")  # Немного увеличили высоту, чтобы текст не влезал на метки
app.title("LLText Editor")
app.resizable(False, False)
app.attributes("-topmost", True, "-toolwindow", True)
buttons_visible = True

# --- СЛОВАРЬ ---
TRANSLATIONS = {
    "English": {"title": "LLText Editor", "st_title": "Editor Settings", "save": "Save", "load": "Load", "set": "Settings", "close": "Close", "apply": "Apply", "clear": "Clear", "hide": "Hide Buttons", "show": "Show Buttons"},
    "Русский": {"title": "LLText Editor", "st_title": "Настройки редактора", "save": "Сохранить", "load": "Открыть", "set": "Настройки", "close": "Закрыть", "apply": "Применить", "clear": "Очистить", "hide": "Скрыть кнопки", "show": "Показать кнопки"},
    "Украинский": {"title": "LLText Editor", "st_title": "Налаштування редактора", "save": "Зберегти", "load": "Відкрити", "set": "Налаштування","close": "Закрити", "apply": "Застосувати", "clear": "Очистити", "hide": "Приховати кнопки", "show": "Показать кнопки"}
}

# --- ФУНКЦИИ ---
def update_lang(lang):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    app.title(t["title"])
    SettingsWindow.title(t["set"])
    lbl_settings.configure(text=t["st_title"])
    btn_save.configure(text=t["save"])
    btn_load.configure(text=t["load"])
    btn_set.configure(text=t["set"])
    btn_close.configure(text=t["close"])
    btn_st_save.configure(text=t["save"])
    btn_apply.configure(text=t["apply"])
    btn_clear.configure(text=t["clear"])
    btn_hide.configure(text=t["hide"] if buttons_visible else t["show"])

def save_file(event=None):
    path = filedialog.asksaveasfilename(initialdir=DOCUMENTS_DIR, initialfile="text.txt", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if path:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(texteditor.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось сохранить файл:\n\n{e}")
    return "break" # Предотвращает стандартное поведение Tkinter

def load_file(event=None):
    path = filedialog.askopenfilename(initialdir=DOCUMENTS_DIR, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if path:
        try:
            with open(path, "r", encoding="utf-8") as f:
                texteditor.delete("1.0", "end")
                texteditor.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось открыть файл:\n\n{e}")
    return "break"

def save_settings(event=None):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            f.write(f"{cb_lang.get()}\n{cb_theme.get()}")
        return "break"
    except Exception as e:
        messagebox.showerror("Error", f"Не удалось сохранить настройки:\n\n{e}")
        return "break"

def load_settings_hotkey(event=None):
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    cb_lang.set(lines[0])
                    cb_theme.set(lines[1])
                    apply_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось загрузить настройки:\n\n{e}")
    return "break"

def apply_settings():
    global current_lang, current_theme
    current_lang, current_theme = cb_lang.get(), cb_theme.get()
    ctk.set_appearance_mode(current_theme)
    update_lang(current_lang)
    save_settings()
    SettingsWindow.withdraw()

def toggle_buttons():
    global buttons_visible
    t = TRANSLATIONS.get(current_lang, TRANSLATIONS["English"])
    if buttons_visible:
        toolbar_frame.pack_forget()
        buttons_visible = False
        btn_hide.configure(text=t["show"])
    else:
        lbl_version.pack_forget()
        ButtonHotKey.pack_forget()
        toolbar_frame.pack(side="top", fill="x", padx=20, pady=5)
        lbl_version.pack(side="bottom", pady=5)
        ButtonHotKey.pack(side="bottom", pady=5)
        buttons_visible = True
        btn_hide.configure(text=t["hide"])

# --- ОКНО НАСТРОЕК ---
SettingsWindow = ctk.CTkToplevel(app)
SettingsWindow.geometry("300x320")
SettingsWindow.resizable(False, False)
SettingsWindow.withdraw()
SettingsWindow.attributes("-topmost", True, "-toolwindow", True)
SettingsWindow.protocol("WM_DELETE_WINDOW", SettingsWindow.withdraw)

lbl_settings = ctk.CTkLabel(SettingsWindow, text="", font=("Arial", 14, "bold"))
lbl_settings.pack(pady=15)

cb_lang = ctk.CTkComboBox(SettingsWindow, values=["English", "Русский", "Украинский"], width=150)
cb_lang.pack(pady=5)
cb_lang.set(current_lang)

cb_theme = ctk.CTkComboBox(SettingsWindow, values=["Light", "Dark"], width=150)
cb_theme.pack(pady=5)
cb_theme.set(current_theme)

btn_close = ctk.CTkButton(SettingsWindow, command=SettingsWindow.withdraw)
btn_close.pack(pady=10)

btn_st_save = ctk.CTkButton(SettingsWindow, command=save_settings)
btn_st_save.pack(pady=5)

btn_apply = ctk.CTkButton(SettingsWindow, command=apply_settings)
btn_apply.pack(pady=5)

btn_hide = ctk.CTkButton(SettingsWindow, command=toggle_buttons)
btn_hide.pack(pady=5)

# --- ГЛАВНОЕ ОКНО ---
texteditor = ctk.CTkTextbox(app, width=450, height=180)
texteditor.pack(pady=15)
texteditor.bind("<Button-1>", lambda e: texteditor.focus_set())

# Привязываем горячие клавиши ко всему приложению (регистронезависимо)
app.bind("<Control-Key-s>", save_file)
app.bind("<Control-Key-S>", save_file)
app.bind("<Control-Key-o>", load_file)
app.bind("<Control-Key-O>", load_file)
app.bind("<Control-Shift-Key-s>", save_settings)
app.bind("<Control-Shift-Key-S>", save_settings)
app.bind("<Control-Shift-Key-l>", load_settings_hotkey)
app.bind("<Control-Shift-Key-L>", load_settings_hotkey)

toolbar_frame = ctk.CTkFrame(app, fg_color="transparent")
toolbar_frame.pack(side="top", fill="x", padx=20, pady=5)

btn_load = ctk.CTkButton(toolbar_frame, command=load_file, width=90)
btn_load.pack(side="left", padx=5)

btn_save = ctk.CTkButton(toolbar_frame, command=save_file, width=90)
btn_save.pack(side="left", padx=5)

btn_set = ctk.CTkButton(toolbar_frame, command=lambda: [SettingsWindow.deiconify(), SettingsWindow.lift()], width=90)
btn_set.pack(side="left", padx=5)

btn_clear = ctk.CTkButton(toolbar_frame, command=lambda: texteditor.delete("1.0", "end"), width=90, height=30, fg_color="red", hover_color="darkred", text_color="white", font=("Arial", 12, "bold"))
btn_clear.pack(side="right", padx=5)

lbl_version = ctk.CTkLabel(app, text="LLText Editor v0.6.3", font=("Arial", 10))
lbl_version.pack(side="bottom", pady=2)

ButtonHotKey = ctk.CTkLabel(app, text="Hotkeys: Ctrl+S - Save | Ctrl+O - Load | Ctrl+Shift+S - Save Settings | Ctrl+Shift+L - Load Settings", font=("Arial", 9), justify="center")
ButtonHotKey.pack(side="bottom", pady=2)

update_lang(current_lang)
app.mainloop()
