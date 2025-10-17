import tkinter as tk
from tkinter import ttk, messagebox
import db


def open_patient_form(parent, refresh_callback, patient=None):
    """
    Вікно додавання або редагування пацієнта.
    param parent: батьківський фрейм
    param refresh_callback: функція для оновлення таблиці після змін
    param patient: словник з даними пацієнта (для редагування)
    """
    window = tk.Toplevel(parent)
    window.title("Редагування пацієнта" if patient else "Новий пацієнт")
    window.geometry("350x300")
    window.resizable(False, False)

    # поля введення
    tk.Label(window, text="Ім'я:").pack(pady=5)
    entry_name = ttk.Entry(window)
    entry_name.pack(fill="x", padx=20)

    tk.Label(window, text="Прізвище:").pack(pady=5)
    entry_surname = ttk.Entry(window)
    entry_surname.pack(fill="x", padx=20)

    tk.Label(window, text="Дата народження (YYYY-MM-DD):").pack(pady=5)
    entry_dob = ttk.Entry(window)
    entry_dob.pack(fill="x", padx=20)

    tk.Label(window, text="Телефон:").pack(pady=5)
    entry_phone = ttk.Entry(window)
    entry_phone.pack(fill="x", padx=20)

    tk.Label(window, text="Адреса:").pack(pady=5)
    entry_address = ttk.Entry(window)
    entry_address.pack(fill="x", padx=20)

    if patient:
        entry_name.insert(0, patient["name"])
        entry_surname.insert(0, patient["surname"])
        entry_dob.insert(0, patient["dob"])
        entry_phone.insert(0, patient["phone"])
        entry_address.insert(0, patient["address"])

    def save_patient():
        name = entry_name.get().strip()
        surname = entry_surname.get().strip()
        dob = entry_dob.get().strip()
        phone = entry_phone.get().strip()
        address = entry_address.get().strip()

        if not all([name, surname, dob, phone, address]):
            return messagebox.showwarning("Помилка", "Заповніть усі поля!")

        conn = db.get_connection()
        cur = conn.cursor()

        if patient:
            cur.execute("""
                UPDATE Patient
                SET Name=%s, Surname=%s, DateOfBirth=%s, PhoneNumber=%s, Address=%s
                WHERE PatientID=%s
            """, (name, surname, dob, phone, address, patient["id"]))
        else:
            cur.execute("""
                INSERT INTO Patient (Name, Surname, DateOfBirth, PhoneNumber, Address)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, surname, dob, phone, address))

        conn.commit()
        cur.close()
        conn.close()

        refresh_callback()
        window.destroy()

    ttk.Button(window, text="💾 Зберегти", command=save_patient).pack(pady=10)
