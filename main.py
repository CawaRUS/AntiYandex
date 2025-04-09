import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import shutil
import psutil
import threading


found = False  # поставить true для принудительного удаление ( не пробовать, не работает )


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
        messagebox.showinfo("Успех", "Процессы Яндекс Браузера завершены.")
        status_label.config(text="Статус: Процессы завершены", fg="green")
    else:
        messagebox.showwarning("Не найдено", "Процессы Яндекс Браузера не найдены.")
        status_label.config(text="Статус: Процессов нет", fg="orange")


def check_yandex_browser():
    def task():
        global found
        status_label.config(text="Идёт поиск...", fg="blue")

        paths = [
            "C:\\Program Files (x86)\\Yandex\\YandexBrowser\\",
            "C:\\Program Files\\Yandex\\YandexBrowser\\",
            os.path.join("C:\\Users", os.getenv('USERNAME'), "AppData", "Local", "Yandex", "YandexBrowser"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "Application", "browser.exe"),
            os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Yandex", "YandexBrowser", "Application", "browser.exe")
]


        for path in paths:
            if os.path.exists(path):
                found = True
                status_label.config(text=f"Яндекс Браузер найден:\n{path}", fg="green")
                return

        found = False
        status_label.config(text="Яндекс Браузер не найден", fg="red")

    threading.Thread(target=task, daemon=True).start()

def uninstall_yandex_browser():
    global found

    if not found:
        messagebox.showwarning("Внимание", "Сначала нужно найти Яндекс Браузер.")
        return

    def task():
        try:
            paths = [
                "C:\\Program Files (x86)\\Yandex\\YandexBrowser\\",
                "C:\\Program Files\\Yandex\\YandexBrowser\\",
                os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser"),
                os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Yandex", "YandexBrowser")
            ]
            
            for path in paths:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    status_label.config(text="Статус: Удалён успешно", fg="green")
                    messagebox.showinfo("Успех", "Яндекс Браузер успешно удалён.")
                    found = False
                    return  

            
            status_label.config(text="Статус: Браузер не найден", fg="red")
            messagebox.showwarning("Не найдено", "Яндекс Браузер не найден.")

        except Exception as e:
            status_label.config(text="Статус: Ошибка", fg="red")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    threading.Thread(target=task, daemon=True).start()

# GUI
root = tk.Tk()
root.title("Антияндекс")
root.geometry("400x250")
root.resizable(False, False)

label = tk.Label(root, text="Удаление Яндекс Браузера", font=("Arial", 14))
label.pack(pady=15)

btn_check = tk.Button(root, text="Поиск Яндекс Браузера", font=("Arial", 12), command=check_yandex_browser)
btn_check.pack(pady=5)

btn_delete = tk.Button(root, text="Удалить Яндекс Браузер", font=("Arial", 12), bg="red", fg="white", command=uninstall_yandex_browser)
btn_delete.pack(pady=5)

status_label = tk.Label(root, text="Статус: Ожидание", font=("Arial", 11), fg="gray")
status_label.pack(pady=20)

kill_button = tk.Button(root, text="Завершить процесс яндекса", command=kill_yandex_processes)
kill_button.pack(pady=5)


root.mainloop()
