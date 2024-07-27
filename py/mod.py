import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
db_path = r'C:\sqlite\gui\attendance'

def execute_query(query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

def add_attendance_record():
    student_id = entry_attendance_student_id.get()
    date = entry_attendance_date.get()
    attended = var_attended.get()
    if not student_id or not date:
        messagebox.showwarning("Input Error", "Please provide both Student ID and Date.")
        return
    query = "INSERT INTO attendance_daily (student_id, date, attended) VALUES (?, ?, ?) "
    execute_query(query, (student_id, date, attended))
    messagebox.showinfo("Success", "Attendance record added successfully.")

def update_attendance_record():
    student_id = entry_attendance_student_id.get()
    date = entry_attendance_date.get()
    attended = var_attended.get()
    if not student_id or not date:
        messagebox.showwarning("Input Error", "Please provide both Student ID and Date.")
        return
    query = "UPDATE attendance_daily SET attended = ? WHERE student_id = ? AND date = ?"
    execute_query(query, (attended, student_id, date))
    messagebox.showinfo("Success", "Attendance record updated successfully.")

def delete_attendance_record():
    student_id = entry_attendance_student_id.get()
    date = entry_attendance_date.get()
    if not student_id or not date:
        messagebox.showwarning("Input Error", "Please provide both Student ID and Date.")
        return
    query = "DELETE FROM attendance_daily WHERE student_id = ? AND date = ?"
    execute_query(query, (student_id, date))
    messagebox.showinfo("Success", "Attendance record deleted successfully.")

def add_student():
    uid = entry_student_uid.get()
    student_id = entry_student_id.get()
    name = entry_student_name.get()
    if not uid or not student_id or not name:
        messagebox.showwarning("Input Error", "Please provide UID, Student ID, and Name.")
        return
    query = "INSERT INTO students (uid, student_id, name) VALUES (?, ?, ?)"
    execute_query(query, (uid, student_id, name))
    messagebox.showinfo("Success", "Student added successfully.")

def update_student():
    uid = entry_student_uid.get()
    student_id = entry_student_id.get()
    name = entry_student_name.get()
    if not uid or not student_id or not name:
        messagebox.showwarning("Input Error", "Please provide UID, Student ID, and Name.")
        return
    query = "UPDATE students SET student_id = ?, name = ? WHERE uid = ?"
    execute_query(query, (student_id, name, uid))
    messagebox.showinfo("Success", "Student updated successfully.")

def delete_student():
    uid = entry_student_uid.get()
    if not uid:
        messagebox.showwarning("Input Error", "Please provide UID.")
        return
    query = "DELETE FROM students WHERE uid = ?"
    execute_query(query, (uid,))
    messagebox.showinfo("Success", "Student deleted successfully.")

def create_gui():
    global entry_attendance_student_id, entry_attendance_date, var_attended
    global entry_student_uid, entry_student_id, entry_student_name
    
    root = tk.Tk()
    root.title("Attendance and Student Management")

    # Attendance Management
    tk.Label(root, text="Attendance Management").grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Student ID:").grid(row=1, column=0, padx=10, pady=5)
    entry_attendance_student_id = tk.Entry(root)
    entry_attendance_student_id.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
    entry_attendance_date = tk.Entry(root)
    entry_attendance_date.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Attended (1 for Yes, 0 for No):").grid(row=3, column=0, padx=10, pady=5)
    var_attended = tk.IntVar()
    tk.Entry(root, textvariable=var_attended).grid(row=3, column=1, padx=10, pady=5)

    tk.Button(root, text="Add Attendance Record", command=add_attendance_record).grid(row=4, column=0, padx=10, pady=5)
    tk.Button(root, text="Update Attendance Record", command=update_attendance_record).grid(row=4, column=1, padx=10, pady=5)
    tk.Button(root, text="Delete Attendance Record", command=delete_attendance_record).grid(row=4, column=2, padx=10, pady=5)

    # Student Management
    tk.Label(root, text="Student Management").grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="UID:").grid(row=6, column=0, padx=10, pady=5)
    entry_student_uid = tk.Entry(root)
    entry_student_uid.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(root, text="Student ID:").grid(row=7, column=0, padx=10, pady=5)
    entry_student_id = tk.Entry(root)
    entry_student_id.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(root, text="Name:").grid(row=8, column=0, padx=10, pady=5)
    entry_student_name = tk.Entry(root)
    entry_student_name.grid(row=8, column=1, padx=10, pady=5)

    tk.Button(root, text="Add Student", command=add_student).grid(row=9, column=0, padx=10, pady=5)
    tk.Button(root, text="Update Student", command=update_student).grid(row=9, column=1, padx=10, pady=5)
    tk.Button(root, text="Delete Student", command=delete_student).grid(row=9, column=2, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
