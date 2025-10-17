import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import db


def fill_query_tab(frame):
    """
    Вкладка 'Запити' з параметризованим пошуком
    Користувач може вибрати бригаду або дату виклику для фільтрації
    """

    # верхній фільтр
    filter_frame = ttk.LabelFrame(frame, text="Фільтр запитів")
    filter_frame.pack(fill="x", padx=10, pady=10)

    # вибір бригади
    ttk.Label(filter_frame, text="Бригада:").grid(row=0, column=0, padx=5, pady=5)
    combo_brigade = ttk.Combobox(filter_frame, state="readonly")
    combo_brigade.grid(row=0, column=1, padx=5, pady=5)

    # вибір дати
    ttk.Label(filter_frame, text="Дата виклику:").grid(row=0, column=2, padx=5, pady=5)
    date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
    date_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(filter_frame, text="🔍 Пошук", command=lambda: search_calls()).grid(row=0, column=4, padx=10)

    # таблиця результатів
    tree = ttk.Treeview(
        frame,
        columns=("Patient", "Brigade", "CallTime", "Symptoms", "Status"),
        show="headings"
    )

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=140)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # список бригад
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT BrigadeID, Specialization FROM Brigade ORDER BY Specialization")
    brigades = cur.fetchall()
    cur.close()
    conn.close()

    combo_brigade["values"] = [b[1] for b in brigades]

    # пошук
    def search_calls():
        tree.delete(*tree.get_children())
        brigade_name = combo_brigade.get().strip()
        date_value = date_entry.get_date()

        query = """
            SELECT p.Name || ' ' || p.Surname, b.Specialization, c.CallTime, c.Symptoms, c.Status
            FROM Call c
            JOIN Patient p ON c.PatientID = p.PatientID
            JOIN Brigade b ON c.BrigadeID = b.BrigadeID
            WHERE 1=1
        """
        params = []

        if brigade_name:
            query += " AND b.Specialization = %s"
            params.append(brigade_name)
        if date_value:
            query += " AND DATE(c.CallTime) = %s"
            params.append(date_value)

        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(query, tuple(params))

        for row in cur.fetchall():
            tree.insert("", "end", values=row)

        cur.close()
        conn.close()

        if not tree.get_children():
            messagebox.showinfo("Результат", "Даних за вибраними параметрами не знайдено.")
