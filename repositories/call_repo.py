from db import execute_query

def get_all_patients():
    return execute_query("SELECT PatientID, FullName, BirthDate, Address, Phone FROM Patient ORDER BY FullName", fetch=True)

def add_patient(fullname, birthdate, address, phone):
    execute_query(
        "INSERT INTO Patient (FullName, BirthDate, Address, Phone) VALUES (%s, %s, %s, %s)",
        (fullname, birthdate, address, phone)
    )

def update_patient(pid, fullname, birthdate, address, phone):
    execute_query(
        "UPDATE Patient SET FullName=%s, BirthDate=%s, Address=%s, Phone=%s WHERE PatientID=%s",
        (fullname, birthdate, address, phone, pid)
    )

def delete_patient(pid):
    execute_query("DELETE FROM Patient WHERE PatientID=%s", (pid,))
