import tkinter as tk
from tkinter import ttk, messagebox
import db
from components.patient_form import open_patient_form
from components.call_form import open_call_form
from components.query_tab import fill_query_tab


# ======================================================
#                 ВКЛАДКА "ПАЦІЄНТИ"
# ======================================================
def fill_patients_tab(frame):
    """Заповнення вкладки 'Пацієнти'."""

    tree = ttk.Treeview(
        frame,
        columns=("Name", "Surname", "DOB", "Phone", "Address"),
        show="headings"
    )

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_tree():
        """Оновлює таблицю пацієнтів."""
        tree.delete(*tree.get_children())
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT PatientID, Name, Surname, DateOfBirth, PhoneNumber, Address 
            FROM Patient
        """)
        for row in cur.fetchall():
            tree.insert("", "end", iid=row[0], values=row[1:])
        cur.close()
        conn.close()

    def add_patient():
        open_patient_form(frame, refresh_tree)

    def edit_patient():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Увага", "Оберіть пацієнта для редагування")

        values = tree.item(selected)["values"]
        patient = {
            "id": int(selected),
            "name": values[0],
            "surname": values[1],
            "dob": values[2],
            "phone": values[3],
            "address": values[4],
        }
        open_patient_form(frame, refresh_tree, patient)

    def delete_patient():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Увага", "Оберіть пацієнта для видалення")

        if messagebox.askyesno("Підтвердження", "Ви дійсно хочете видалити пацієнта?"):
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Patient WHERE PatientID = %s", (selected,))
            conn.commit()
            cur.close()
            conn.close()
            refresh_tree()

    # --- Кнопки ---
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="➕ Додати", command=add_patient).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="✏️ Редагувати", command=edit_patient).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="❌ Видалити", command=delete_patient).pack(side="left", padx=5)

    refresh_tree()


# ======================================================
#                   ВКЛАДКА "ВИКЛИКИ"
# ======================================================
def fill_calls_tab(frame):
    """Заповнення вкладки 'Виклики'."""

    tree = ttk.Treeview(
        frame,
        columns=("Patient", "Brigade", "CallTime", "Symptoms", "Status"),
        show="headings"
    )

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_tree():
        """Оновлює список викликів."""
        tree.delete(*tree.get_children())
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.CallID, p.Name || ' ' || p.Surname, 
                   b.Specialization, c.CallTime, c.Symptoms, c.Status
            FROM Call c
            JOIN Patient p ON c.PatientID = p.PatientID
            JOIN Brigade b ON c.BrigadeID = b.BrigadeID
        """)
        for row in cur.fetchall():
            tree.insert("", "end", iid=row[0], values=row[1:])
        cur.close()
        conn.close()

    def add_call():
        open_call_form(frame, refresh_tree)

    def edit_call():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Увага", "Оберіть виклик для редагування")

        values = tree.item(selected)["values"]
        call = {
            "id": int(selected),
            "patient": values[0],
            "brigade": values[1],
            "calltime": str(values[2]),
            "symptoms": values[3],
            "status": values[4],
        }
        open_call_form(frame, refresh_tree, call)

    def delete_call():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Увага", "Оберіть виклик для видалення")

        if messagebox.askyesno("Підтвердження", "Ви дійсно хочете видалити виклик?"):
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Call WHERE CallID = %s", (selected,))
            conn.commit()
            cur.close()
            conn.close()
            refresh_tree()

    # --- Кнопки ---
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="➕ Додати", command=add_call).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="✏️ Редагувати", command=edit_call).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="❌ Видалити", command=delete_call).pack(side="left", padx=5)

    refresh_tree()


# ======================================================
#                 ГОЛОВНЕ ВІКНО ПРОГРАМИ
# ======================================================
def show_main_window(user):
    """Створює головне вікно додатка після авторизації."""
    root = tk.Tk()
    root.title("Головне меню")
    root.geometry("800x600")

    # --- Верхня панель ---
    top_frame = ttk.Frame(root)
    top_frame.pack(side="top", fill="x", pady=5)

    ttk.Label(top_frame, text="Вітаємо!", font=("Arial", 12)).pack(side="left", padx=10)
    ttk.Button(top_frame, text="Вийти", command=root.destroy).pack(side="right", padx=10)

    # --- Вкладки ---
    notebook = ttk.Notebook(root)

    patients_frame = ttk.Frame(notebook)
    notebook.add(patients_frame, text="Пацієнти")
    fill_patients_tab(patients_frame)

    calls_frame = ttk.Frame(notebook)
    notebook.add(calls_frame, text="Виклики")
    fill_calls_tab(calls_frame)

    queries_frame = ttk.Frame(notebook)
    notebook.add(queries_frame, text="Запити")
    fill_query_tab(queries_frame)

    notebook.pack(expand=True, fill="both")

    root.mainloop()
