import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
DATABASE = r'C:\sqlite\gui\attendance'

def connect_db():
    return sqlite3.connect(DATABASE)

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS attendance_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        date TEXT,
        entry_time TEXT,
        exit_time TEXT,
        late INTEGER,
        attended INTEGER
    )
    ''')
    conn.commit()
    conn.close()

create_table()

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")

        # Create and configure the Treeview (excluding the 'id' column)
        self.tree = ttk.Treeview(root, columns=("student_id", "date", "entry_time", "exit_time", "late", "attended"), show='headings')
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("entry_time", text="Entry Time")
        self.tree.heading("exit_time", text="Exit Time")
        self.tree.heading("late", text="Late")
        self.tree.heading("attended", text="Attended")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Buttons
        self.add_button = tk.Button(root, text="Add Record", command=self.add_record)
        self.add_button.pack(side='left', padx=5, pady=5)

        self.edit_button = tk.Button(root, text="Edit Record", command=self.edit_record)
        self.edit_button.pack(side='left', padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Delete Record", command=self.delete_record)
        self.delete_button.pack(side='left', padx=5, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, student_id, date, entry_time, exit_time, late, attended FROM attendance_daily")
        rows = c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, iid=row[0], values=row[1:])  # Exclude the 'id' column for display
        conn.close()

    def add_record(self):
        def save_record():
            student_id = student_id_entry.get()
            date = date_entry.get()
            entry_time = entry_time_entry.get()
            exit_time = exit_time_entry.get()
            late = int(late_entry.get())
            attended = int(attended_entry.get())

            if not all([student_id, date, entry_time, exit_time]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO attendance_daily (student_id, date, entry_time, exit_time, late, attended) VALUES (?, ?, ?, ?, ?, ?)",
                      (student_id, date, entry_time, exit_time, late, attended))
            conn.commit()
            conn.close()
            self.load_data()
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Record")

        tk.Label(add_window, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Date").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Entry Time").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Exit Time").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Late").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(add_window, text="Attended").grid(row=5, column=0, padx=5, pady=5)

        student_id_entry = tk.Entry(add_window)
        date_entry = tk.Entry(add_window)
        entry_time_entry = tk.Entry(add_window)
        exit_time_entry = tk.Entry(add_window)
        late_entry = tk.Entry(add_window)
        attended_entry = tk.Entry(add_window)

        student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.grid(row=1, column=1, padx=5, pady=5)
        entry_time_entry.grid(row=2, column=1, padx=5, pady=5)
        exit_time_entry.grid(row=3, column=1, padx=5, pady=5)
        late_entry.grid(row=4, column=1, padx=5, pady=5)
        attended_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Save", command=save_record).grid(row=6, column=0, columnspan=2, pady=10)

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to edit.")
            return

        item_id = selected_item[0]
        item = self.tree.item(item_id)
        values = item['values']

        def save_edit():
            student_id = student_id_entry.get()
            date = date_entry.get()
            entry_time = entry_time_entry.get()
            exit_time = exit_time_entry.get()
            late = int(late_entry.get())
            attended = int(attended_entry.get())

            if not all([student_id, date, entry_time, exit_time]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            conn = connect_db()
            c = conn.cursor()
            c.execute("UPDATE attendance_daily SET student_id=?, date=?, entry_time=?, exit_time=?, late=?, attended=? WHERE id=?",
                      (student_id, date, entry_time, exit_time, late, attended, item_id))
            conn.commit()
            conn.close()
            self.load_data()
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Record")

        tk.Label(edit_window, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Date").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Entry Time").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Exit Time").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Late").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(edit_window, text="Attended").grid(row=5, column=0, padx=5, pady=5)

        student_id_entry = tk.Entry(edit_window)
        date_entry = tk.Entry(edit_window)
        entry_time_entry = tk.Entry(edit_window)
        exit_time_entry = tk.Entry(edit_window)
        late_entry = tk.Entry(edit_window)
        attended_entry = tk.Entry(edit_window)

        student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.grid(row=1, column=1, padx=5, pady=5)
        entry_time_entry.grid(row=2, column=1, padx=5, pady=5)
        exit_time_entry.grid(row=3, column=1, padx=5, pady=5)
        late_entry.grid(row=4, column=1, padx=5, pady=5)
        attended_entry.grid(row=5, column=1, padx=5, pady=5)

        # Populate the entry fields with existing data
        student_id_entry.insert(0, values[0])
        date_entry.insert(0, values[1])
        entry_time_entry.insert(0, values[2])
        exit_time_entry.insert(0, values[3])
        late_entry.insert(0, values[4])
        attended_entry.insert(0, values[5])

        tk.Button(edit_window, text="Save", command=save_edit).grid(row=6, column=0, columnspan=2, pady=10)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        item_id = selected_item[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            conn = connect_db()
            c = conn.cursor()
            c.execute("DELETE FROM attendance_daily WHERE id=?", (item_id,))
            conn.commit()
            conn.close()
            self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop
