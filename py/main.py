import serial
import sqlite3
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime
import threading
import time

# Function to update attendance
def update_attendance(uid, current_time, status):
    conn = sqlite3.connect(r'C:\sqlite\gui\attendance')
    cursor = conn.cursor()
    
    date, time_part = current_time.split()
    entry_time = exit_time = None

    cursor.execute("SELECT student_id, name FROM students WHERE uid = ?", (uid,))
    student = cursor.fetchone()

    if student:
        student_id, name = student

        if status == 'ENTRY':
            entry_time = time_part
            cursor.execute(
                """
                INSERT OR REPLACE INTO attendance_daily (student_id, date, entry_time, late, attended)
                VALUES (?, ?, ?, COALESCE((SELECT late FROM attendance_daily WHERE student_id = ? AND date = ?), 0), 1)
                """,
                (student_id, date, entry_time, student_id, date)
            )
            if entry_time > '08:00:00':
                cursor.execute(
                    "UPDATE attendance_daily SET late = 1 WHERE student_id = ? AND date = ?",
                    (student_id, date)
                )
        elif status == 'EXIT':
            exit_time = time_part
            cursor.execute(
                "UPDATE attendance_daily SET exit_time = ?, attended = 1 WHERE student_id = ? AND date = ?",
                (exit_time, student_id, date)
            )
        conn.commit()
        display_message(f"Student ID: {student_id}, Name: {name}\nTime: {current_time}\nStatus: {status}")
    else:
        display_message(f"UID {uid} not found in database.")
    
    conn.close()

def send_time_and_status_to_arduino(ser, time_str, status):
    ser.write(f"TIME:{time_str}\n".encode())
    ser.write(f"STATUS:{status}\n".encode())

def start_system():
    current_time = entry_time.get()
    status = status_var.get()

    if not current_time or not status:
        display_message("Please set both time and status.")
        return

    root.withdraw()
    show_main_gui(current_time, status)

def run_serial_communication(ser, current_time, status):
    send_time_and_status_to_arduino(ser, current_time, status)

    while True:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            uid = data.split(',')[0].strip().upper()  # Extract only the UID
            handle_database_operations(uid, current_time, status)  # Use the current_time from GUI, not from Arduino

def handle_database_operations(uid, current_time, status_received):
    threading.Thread(target=update_attendance, args=(uid, current_time, status_received)).start()
    time.sleep(5)
    display_message("Please tap your card.")

def display_message(message):
    message_label.config(text=message)
    message_label.update()

def show_main_gui(current_time, status):
    main_gui = Toplevel(root)
    main_gui.title("iAttend - Tap Card")

    # Set the window size to match the main GUI (2560x1440 or as needed)
    main_gui.geometry("800x350")

    frame = ttk.Frame(main_gui, padding="20")
    frame.grid(row=0, column=0, sticky=(N, S, E, W))

    ttk.Label(frame, text=f"Date: {current_time.split()[0]}", font=("Helvetica", 24)).grid(column=1, row=1, sticky=W)
    ttk.Label(frame, text=f"Time: {current_time.split()[1]}", font=("Helvetica", 24)).grid(column=2, row=1, sticky=W)
    ttk.Label(frame, text=f"Status: {status}", font=("Helvetica", 24)).grid(column=3, row=1, sticky=W)

    global message_label
    message_label = ttk.Label(frame, text="Please tap your card.", foreground="blue", font=("Helvetica", 24))
    message_label.grid(column=1, row=2, columnspan=3, sticky=(W, E))

    ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust 'COM3' as needed
    threading.Thread(target=run_serial_communication, args=(ser, current_time, status)).start()

# GUI Setup
root = ThemedTk(theme="arc")
root.title("iAttend System")

# Set the window size to 2560x1440 (or adjust as needed)
root.geometry("1400x800")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(N, S, E, W))

ttk.Label(frame, text="Set Date and Time (YYYY-MM-DD HH:MM:SS):", font=("Helvetica", 24)).grid(column=1, row=1, sticky=W)
entry_time = ttk.Entry(frame, width=40, font=("Helvetica", 20))
entry_time.grid(column=2, row=1, sticky=(W, E))

ttk.Label(frame, text="Select Status:", font=("Helvetica", 24)).grid(column=1, row=2, sticky=W)
status_var = StringVar()
status_combobox = ttk.Combobox(frame, textvariable=status_var, values=("ENTRY", "EXIT"), state="readonly", font=("Helvetica", 20))
status_combobox.grid(column=2, row=2, sticky=(W, E))

start_button = ttk.Button(frame, text="Start System", command=start_system, width=20, padding=10, style="TButton")
start_button.grid(column=2, row=3, sticky=(W, E))

# Customize TButton style to make it larger
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 20), padding=10)

for child in frame.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.mainloop()
