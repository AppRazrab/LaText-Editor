import os
from tkinter import filedialog
import customtkinter as ctk

# --- ИНИЦИАЛИЗАЦИЯ И ЗАГРУЗКА НАСТРОЕК ---
current_lang = "Русский"
current_theme = "Light"

if os.path.exists("settings.txt"):
    try:
        with open("settings.txt", "r", encoding="utf-8") as settings_file:
            lines = settings_file.read().splitlines()
            if len(lines) >= 2:
                current_lang = lines[0]
                current_theme = lines[1]
    except Exception:
        pass

ctk.set_appearance_mode(current_theme)

app = ctk.CTk()
app.geometry("490x320")  # Сделали окно чуть шире и компактнее по высоте
app.title("LaText Editor")
app.resizable(False, False)

app.configure(bg_color="lightblue")
app.attributes("-topmost", True)
app.attributes("-toolwindow", True)

# Переменная для отслеживания видимости панели кнопок
buttons_visible = True

# --- СЛОВАРЬ ДЛЯ ЛОКАЛИЗАЦИИ ---
TRANSLATIONS = {
    "English": {
        "title": "LaText Editor",
        "settings_title": "Editor Settings",
        "save": "Save",
        "load": "Load",
        "settings": "Settings",
        "close": "Close",
        "apply": "Apply",
        "clear": "Clear",
        "hide_buttons": "Hide Buttons",
        "show_buttons": "Show Buttons"
    },
    "Русский": {
        "title": "LaText Editor",
        "settings_title": "Настройки редактора",
        "save": "Сохранить",
        "load": "Открыть",
        "settings": "Настройки",
        "close": "Закрыть",
        "apply": "Применить",
        "clear": "Очистить",
        "hide_buttons": "Скрыть кнопки",
        "show_buttons": "Показать кнопки"
    }
}

# --- ФУНКЦИИ ---

def update_interface_language(lang):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    app.title(t["title"])
    SettingsWindow.title(t["settings"])
    label_settings.configure(text=t["settings_title"])
    Buttonsave.configure(text=t["save"])
    Buttonload.configure(text=t["load"])
    ButtonSettings.configure(text=t["settings"])
    SettingsCloseButton.configure(text=t["close"])
    SettingsSaveButton.configure(text=t["save"])
    Settingsapplication.configure(text=t["apply"])
    ButtonCleartext.configure(text=t["clear"])
    
    # Обновляем текст кнопки в зависимости от текущего состояния видимости панели
    if buttons_visible:
        Settinghidebutton.configure(text=t["hide_buttons"])
    else:
        Settinghidebutton.configure(text=t["show_buttons"])

def save_file():
    os.makedirs("saved_texts", exist_ok=True)
    file_path = filedialog.asksaveasfilename(
        initialdir="saved_texts",
        initialfile="text.txt",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Сохранить файл как"
    )
    if file_path:
        text_content = texteditor.get("1.0", "end-1c")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_content)

def load_file():
    file_path = filedialog.askopenfilename(
        initialdir="saved_texts",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Открыть файл"
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()
            texteditor.delete("1.0", "end")
            texteditor.insert("1.0", text_content)

def save_settings():
    save_language = SettingsLanguage.get()
    save_theme = SettingsTheme.get()
    with open("settings.txt", "w", encoding="utf-8") as settings_file:
        settings_file.write(f"{save_language}\n{save_theme}")

def open_settings():
    SettingsWindow.deiconify()

def hide_settings():
    SettingsWindow.withdraw()

def apply_settings():
    selected_lang = SettingsLanguage.get()
    selected_theme = SettingsTheme.get()
    ctk.set_appearance_mode(selected_theme)
    update_interface_language(selected_lang)
    save_settings()
    hide_settings()

def toggle_buttons():
    """Переключает видимость панели с кнопками (toolbar_frame)"""
    global buttons_visible
    t = TRANSLATIONS.get(SettingsLanguage.get(), TRANSLATIONS["English"])
    
    if buttons_visible:
        # Прячем фрейм со всеми кнопками внутри
        toolbar_frame.pack_forget()
        buttons_visible = False
        Settinghidebutton.configure(text=t["show_buttons"])
    else:
        # Чтобы сохранить правильный порядок элементов (версия снизу),
        # временно убираем версию, пакуем кнопки и возвращаем версию назад.
        labelversion.pack_forget()
        toolbar_frame.pack(side="top", fill="x", padx=20, pady=5)
        labelversion.pack(side="bottom", pady=5)
        buttons_visible = True
        Settinghidebutton.configure(text=t["hide_buttons"])

# --- СОЗДАНИЕ ОКНА НАСТРОЕК ---
SettingsWindow = ctk.CTkToplevel(app)
SettingsWindow.title("Settings")
SettingsWindow.geometry("300x320")
SettingsWindow.resizable(False, False)
SettingsWindow.withdraw()
SettingsWindow.attributes("-topmost", True)
SettingsWindow.attributes("-toolwindow", True)
SettingsWindow.protocol("WM_DELETE_WINDOW", hide_settings)

label_settings = ctk.CTkLabel(SettingsWindow, text="Настройки редактора", font=("Arial", 14, "bold"))
label_settings.pack(pady=15)

SettingsLanguage = ctk.CTkComboBox(SettingsWindow, values=["English", "Русский"], width=150)
SettingsLanguage.pack(pady=5)
SettingsLanguage.set(current_lang)

SettingsTheme = ctk.CTkComboBox(SettingsWindow, values=["Light", "Dark"], width=150)
SettingsTheme.pack(pady=5)
SettingsTheme.set(current_theme)

SettingsCloseButton = ctk.CTkButton(SettingsWindow, text="Close", command=hide_settings)
SettingsCloseButton.pack(pady=10)

SettingsSaveButton = ctk.CTkButton(SettingsWindow, text="Save", command=save_settings)
SettingsSaveButton.pack(pady=5)

Settingsapplication = ctk.CTkButton(SettingsWindow, text="Apply", command=apply_settings)
Settingsapplication.pack(pady=5)

# ИСПРАВЛЕНО: Кнопка перевязана на функцию toggle_buttons
Settinghidebutton = ctk.CTkButton(SettingsWindow, text="Hide buttons", command=toggle_buttons)
Settinghidebutton.pack(pady=5)


# --- ИНТЕРФЕЙС ГЛАВНОГО ОКНА ---

# Текстовое поле
texteditor = ctk.CTkTextbox(app, width=450, height=180)
texteditor.pack(pady=15)
texteditor.bind("<Button-1>", lambda e: texteditor.focus_set())

# 1. Горизонтальный контейнер для КНОПОК
toolbar_frame = ctk.CTkFrame(app, fg_color="transparent")
toolbar_frame.pack(side="top", fill="x", padx=20, pady=5)

# Кнопки выстраиваются слева направо внутри toolbar_frame
Buttonload = ctk.CTkButton(toolbar_frame, text="Load", command=load_file, width=90)
Buttonload.pack(side="left", padx=5)

Buttonsave = ctk.CTkButton(toolbar_frame, text="Save", command=save_file, width=90)
Buttonsave.pack(side="left", padx=5)

ButtonSettings = ctk.CTkButton(toolbar_frame, text="Settings", command=open_settings, width=90)
ButtonSettings.pack(side="left", padx=5)

# Кнопка Clear (Красная, теперь находится ЧЕТКО СПРАВА)
ButtonCleartext = ctk.CTkButton(toolbar_frame, text="Clear", command=lambda: texteditor.delete("1.0", "end"), width=90, height=30)
ButtonCleartext.configure(fg_color="red", hover_color="darkred", text_color="white", font=("Arial", 12, "bold"))
ButtonCleartext.bind("<Enter>", lambda e: ButtonCleartext.configure(fg_color="darkred"))
ButtonCleartext.bind("<Leave>", lambda e: ButtonCleartext.configure(fg_color="red"))
ButtonCleartext.pack(side="right", padx=5)

# Версия программы в самом низу
labelversion = ctk.CTkLabel(app, text="LaText Editor v0.5.3", font=("Arial", 10))
labelversion.pack(side="bottom", pady=5)

# Первичная настройка языка при запуске
update_interface_language(current_lang)

app.mainloop()
