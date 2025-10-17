import tkinter as tk
from tkinter import messagebox
import db
import main_window


def show_login_window():
    """Вікно авторизації диспетчера"""

    def try_login():
        """Перевіряє логін і пароль користувача"""
        login = entry_login.get().strip()
        password = entry_password.get().strip()

        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM Dispatcher WHERE Login = %s AND Password = %s",
                (login, password)
            )
            user = cur.fetchone()
        finally:
            cur.close()
            conn.close()

        if user:
            root.destroy()
            main_window.show_main_window(user)
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль")

    root = tk.Tk()
    root.title("Авторизація")
    root.geometry("300x180")

    # поля введення
    tk.Label(root, text="Логін").pack(pady=5)
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Пароль").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Увійти", command=try_login).pack(pady=10)

    root.mainloop()
