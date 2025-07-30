import tkinter as tk
from tkinter import messagebox
import os
import shutil
import psutil
import threading
import winreg
import locale

language = "ru"
system_lang = locale.getdefaultlocale()[0]
language = "ru" if system_lang.startswith("ru") else "en"
found = False
status_text = ""

def check_registry_for_yandex():
    found_in_registry = False
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    try:
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if "Яндекс" in display_name or "Yandex" in display_name:
                            found_in_registry = True
                            break
                    except FileNotFoundError:
                        continue
    except Exception as e:
        print("Ошибка при доступе к реестру:", e)

    if found_in_registry:
        update_status("Найден в реестре" if language == "ru" else "Found in registry", "green")
        messagebox.showinfo(t("title"), "Яндекс найден в реестре." if language == "ru" else "Yandex found in registry.")
    else:
        update_status("В реестре не найден" if language == "ru" else "Not found in registry", "red")
        messagebox.showwarning(t("title"), "Не найден в реестре." if language == "ru" else "Not found in registry.")

def t(key):
    translations = {
        "ru": {
            "title": "Удаление Яндекс Браузера",
            "search_btn": "Поиск Яндекс Браузера",
            "delete_btn": "Удалить Яндекс Браузер",
            "kill_btn": "Завершить процесс Яндекса",
            "status_wait": "Статус: Ожидание",
            "status_searching": "Идёт поиск...",
            "status_found": "Яндекс Браузер найден:\n{}",
            "status_not_found": "Яндекс Браузер не найден",
            "status_killed": "Статус: Процессы завершены",
            "status_no_proc": "Статус: Процессов нет",
            "success_kill": "Процессы Яндекс Браузера завершены.",
            "not_found_warning": "Процессы Яндекс Браузера не найдены.",
            "delete_success": "Яндекс Браузер успешно удалён.",
            "delete_fail": "Яндекс Браузер не найден.",
            "delete_first": "Сначала нужно найти Яндекс Браузер.",
            "registry_check_btn": "Проверить реестр"
        },
        "en": {
            "title": "Yandex Browser Remover",
            "search_btn": "Search for Yandex Browser",
            "delete_btn": "Delete Yandex Browser",
            "kill_btn": "Kill Yandex Process",
            "status_wait": "Status: Waiting",
            "status_searching": "Searching...",
            "status_found": "Yandex Browser found:\n{}",
            "status_not_found": "Yandex Browser not found",
            "status_killed": "Status: Processes killed",
            "status_no_proc": "Status: No processes found",
            "success_kill": "Yandex Browser processes have been killed.",
            "not_found_warning": "No Yandex Browser processes found.",
            "delete_success": "Yandex Browser successfully deleted.",
            "delete_fail": "Yandex Browser not found.",
            "delete_first": "You must find the browser first.",
            "registry_check_btn": "Check Registry"
        }
    }
    return translations[language].get(key, key)

def kill_yandex_processes():
    killed = False
    target_processes = ["browser.exe", "yandex.exe"]

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in target_processes:
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed:
        messagebox.showinfo(t("title"), t("success_kill"))
        update_status(t("status_killed"), "green")
    else:
        messagebox.showwarning(t("title"), t("not_found_warning"))
        update_status(t("status_no_proc"), "orange")

def check_yandex_browser():
    def task():
        global found
        update_status(t("status_searching"), "blue")

        paths = [
            "C:\\Program Files (x86)\\Yandex\\YandexBrowser\\",
            "C:\\Program Files\\Yandex\\YandexBrowser\\",
            os.path.join("C:\\Users", os.getenv('USERNAME'), "AppData", "Local", "Yandex", "YandexBrowser"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "Application", "browser.exe"),
            os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Yandex", "YandexBrowser", "Application", "browser.exe"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "Application", "service_update.exe")
        ]

        for path in paths:
            if os.path.exists(path):
                found = True
                update_status(t("status_found").format(path), "green")
                return

        found = False
        update_status(t("status_not_found"), "red")

    threading.Thread(target=task, daemon=True).start()

def uninstall_yandex_browser():
    global found
    if not found:
        messagebox.showwarning(t("title"), t("delete_first"))
        return

    def task():
        global found
        try:
            paths = [
                "C:\\Program Files (x86)\\Yandex\\YandexBrowser\\",
                "C:\\Program Files\\Yandex\\YandexBrowser\\",
                os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser"),
                os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Yandex", "YandexBrowser")
            ]

            for path in paths:
                if os.path.exists(path):
                    shutil.rmtree(path, ignore_errors=True)
                    found = False
                    update_status(t("delete_success"), "green")
                    messagebox.showinfo(t("title"), t("delete_success"))
                    return

            update_status(t("delete_fail"), "red")
            messagebox.showwarning(t("title"), t("delete_fail"))
        except Exception as e:
            update_status(t("delete_fail"), "red")
            messagebox.showerror(t("title"), f"{t('delete_fail')}\n{e}")

    threading.Thread(target=task, daemon=True).start()

def update_status(status, color):
    global status_text
    status_text = status
    status_label.config(text=status_text, fg=color)

# GUI
root = tk.Tk()
root.title("АнтиЯндекс")
root.geometry("500x300")
root.resizable(False, False)

label = tk.Label(root, text=t("title"), font=("Arial", 14))
label.pack(pady=15)

btn_check = tk.Button(root, text=t("search_btn"), font=("Arial", 12), command=check_yandex_browser)
btn_check.pack(pady=5)

btn_delete = tk.Button(root, text=t("delete_btn"), font=("Arial", 12), bg="red", fg="white", command=uninstall_yandex_browser)
btn_delete.pack(pady=5)

status_label = tk.Label(root, text=t("status_wait"), font=("Arial", 11), fg="blue")
status_label.pack(pady=20)

kill_button = tk.Button(root, text=t("kill_btn"), command=kill_yandex_processes)
kill_button.pack(pady=5)

btn_check_registry = tk.Button(root, text=t("registry_check_btn"), command=check_registry_for_yandex)
btn_check_registry.pack(pady=5)

def toggle_language():
    global language
    language = "en" if language == "ru" else "ru"
    update_ui_texts()

def update_ui_texts():
    root.title(t("title"))
    label.config(text=t("title"))
    btn_check.config(text=t("search_btn"))
    btn_delete.config(text=t("delete_btn"))
    kill_button.config(text=t("kill_btn"))
    btn_check_registry.config(text=t("registry_check_btn"))
    update_status(t("status_wait"), "blue")

lang_button = tk.Button(root, text="EN/RU", command=toggle_language)
lang_button.place(x=430, y=16, width=40, height=25)

root.mainloop()
