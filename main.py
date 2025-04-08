import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import shutil

found = False  # поставить true для принудительного удаление ( не пробовать, не работает )

import threading

def check_yandex_browser():
    def task():
        global found
        status_label.config(text="Идёт поиск...", fg="blue")

        paths = [
            "C:\\Users\\%username%\\AppData\\Local\\Yandex\\YandexBrowser\\Application",
            os.path.join(os.getenv("LOCALAPPDATA"), "Yandex", "YandexBrowser", "Application", "browser.exe")
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

    # Функция для выполнения удаления в отдельном потоке
    def task():
        try:
            # Получаем имя текущего пользователя
            username = os.getenv('USERNAME')
            # Используем путь, как в большинстве установок
            browser_path = f"C:\\Users\\{username}\\AppData\\Local\\Yandex\\YandexBrowser"
            if not os.path.exists(browser_path):
                # Пробуем альтернативный путь
                browser_path = f"C:\\Users\\{username}\\AppData\\Local\\Yandex\\YandexBrowser\\Application"
            
            # Проверка существует ли папка с браузером
            if os.path.exists(browser_path):
                # Удаление папки с браузером
                shutil.rmtree(browser_path)
                status_label.config(text="Статус: Удалён успешно", fg="green")
                messagebox.showinfo("Успех", "Яндекс Браузер успешно удалён.")
                found = False
            else:
                status_label.config(text="Статус: Браузер не найден", fg="red")
                messagebox.showwarning("Не найдено", "Яндекс Браузер не найден.")

        except Exception as e:
            status_label.config(text="Статус: Ошибка", fg="red")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    # Запуск в отдельном потоке, чтобы избежать зависания интерфейса
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

root.mainloop()
