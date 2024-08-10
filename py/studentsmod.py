import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
DATABASE = r"C:\sqlite\gui\attendance"

def connect_db():
    return sqlite3.connect(DATABASE)

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        student_id TEXT,
        name TEXT
    )
    ''')
    conn.commit()
    conn.close()

create_table()

class StudentsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        # Create and configure the Treeview (excluding the 'id' column)
        self.tree = ttk.Treeview(root, columns=("uid", "student_id", "name"), show='headings')
        self.tree.heading("uid", text="UID")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Buttons
        self.add_button = tk.Button(root, text="Add Student", command=self.add_student)
        self.add_button.pack(side='left', padx=5, pady=5)

        self.edit_button = tk.Button(root, text="Edit Student", command=self.edit_student)
        self.edit_button.pack(side='left', padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Delete Student", command=self.delete_student)
        self.delete_button.pack(side='left', padx=5, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, uid, student_id, name FROM students")
        rows = c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, iid=row[0], values=row[1:])  # Exclude the 'id' column for display
        conn.close()

    def add_student(self):
        def save_student():
            uid = uid_entry.get()
            student_id = student_id_entry.get()
            name = name_entry.get()

            if not all([uid, student_id, name]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO students (uid, student_id, name) VALUES (?, ?, ?)",
                      (uid, student_id, name))
            conn.commit()
            conn.close()
            self.load_data()
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")

        tk.Label(add_window, text="UID").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Student ID").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Name").grid(row=2, column=0, padx=5, pady=5)

        uid_entry = tk.Entry(add_window)
        student_id_entry = tk.Entry(add_window)
        name_entry = tk.Entry(add_window)

        uid_entry.grid(row=0, column=1, padx=5, pady=5)
        student_id_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Save", command=save_student).grid(row=3, column=0, columnspan=2, pady=10)

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a student to edit.")
            return

        item_id = selected_item[0]
        item = self.tree.item(item_id)
        values = item['values']

        def save_edit():
            uid = uid_entry.get()
            student_id = student_id_entry.get()
            name = name_entry.get()

            if not all([uid, student_id, name]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            conn = connect_db()
            c = conn.cursor()
            c.execute("UPDATE students SET uid=?, student_id=?, name=? WHERE id=?",
                      (uid, student_id, name, item_id))
            conn.commit()
            conn.close()
            self.load_data()
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student")

        tk.Label(edit_window, text="UID").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Student ID").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Name").grid(row=2, column=0, padx=5, pady=5)

        uid_entry = tk.Entry(edit_window)
        student_id_entry = tk.Entry(edit_window)
        name_entry = tk.Entry(edit_window)

        uid_entry.grid(row=0, column=1, padx=5, pady=5)
        student_id_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry.grid(row=2, column=1, padx=5, pady=5)

        # Populate the entry fields with existing data
        uid_entry.insert(0, values[0])
        student_id_entry.insert(0, values[1])
        name_entry.insert(0, values[2])

        tk.Button(edit_window, text="Save", command=save_edit).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a student to delete.")
            return

        item_id = selected_item[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            conn = connect_db()
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE id=?", (item_id,))
            conn.commit()
            conn.close()
            self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentsApp(root)
    root.mainloop()
