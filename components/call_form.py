import tkinter as tk
from tkinter import ttk, messagebox
import db


def open_call_form(parent, refresh_callback, call=None):
    """
    Вікно додавання або редагування виклику
    param parent батьківський фрейм
    param refresh_callback функція оновлення таблиці
    param call словник з даними виклику (для редагування)
    """
    window = tk.Toplevel(parent)
    window.title("Редагування виклику" if call else "Новий виклик")
    window.geometry("400x350")
    window.resizable(False, False)

    #  довідкові списки
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT PatientID, Name || ' ' || Surname FROM Patient ORDER BY Name")
    patients = cur.fetchall()

    cur.execute("SELECT BrigadeID, Specialization FROM Brigade ORDER BY Specialization")
    brigades = cur.fetchall()

    cur.close()
    conn.close()

    # випадаючі списки
    tk.Label(window, text="Пацієнт:").pack(pady=5)
    combo_patient = ttk.Combobox(window, values=[p[1] for p in patients], state="readonly")
    combo_patient.pack(fill="x", padx=20)

    tk.Label(window, text="Бригада:").pack(pady=5)
    combo_brigade = ttk.Combobox(window, values=[b[1] for b in brigades], state="readonly")
    combo_brigade.pack(fill="x", padx=20)

    tk.Label(window, text="Дата і час виклику (YYYY-MM-DD HH:MM):").pack(pady=5)
    entry_time = ttk.Entry(window)
    entry_time.pack(fill="x", padx=20)

    tk.Label(window, text="Симптоми:").pack(pady=5)
    entry_symptoms = ttk.Entry(window)
    entry_symptoms.pack(fill="x", padx=20)

    tk.Label(window, text="Статус:").pack(pady=5)
    combo_status = ttk.Combobox(window, values=["Очікується", "Виконується", "Завершено"], state="readonly")
    combo_status.pack(fill="x", padx=20)

    # редагування
    if call:
        combo_patient.set(call["patient"])
        combo_brigade.set(call["brigade"])
        entry_time.insert(0, call["calltime"])
        entry_symptoms.insert(0, call["symptoms"])
        combo_status.set(call["status"])

    def save_call():
        patient_name = combo_patient.get()
        brigade_name = combo_brigade.get()
        call_time = entry_time.get().strip()
        symptoms = entry_symptoms.get().strip()
        status = combo_status.get().strip()

        if not all([patient_name, brigade_name, call_time, symptoms, status]):
            return messagebox.showwarning("Помилка", "Заповніть усі поля!")

        # ID за назвою
        patient_id = next((p[0] for p in patients if p[1] == patient_name), None)
        brigade_id = next((b[0] for b in brigades if b[1] == brigade_name), None)

        conn = db.get_connection()
        cur = conn.cursor()

        if call:
            cur.execute("""
                UPDATE Call
                SET PatientID=%s, BrigadeID=%s, CallTime=%s, Symptoms=%s, Status=%s
                WHERE CallID=%s
            """, (patient_id, brigade_id, call_time, symptoms, status, call["id"]))
        else:
            cur.execute("""
                INSERT INTO Call (PatientID, BrigadeID, CallTime, Symptoms, Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (patient_id, brigade_id, call_time, symptoms, status))

        conn.commit()
        cur.close()
        conn.close()

        refresh_callback()
        window.destroy()

    ttk.Button(window, text="💾 Зберегти", command=save_call).pack(pady=10)
