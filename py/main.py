import serial
import sqlite3
import time

# Connect to the serial port where Arduino is connected
ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust 'COM3' as needed

# Connect to SQLite database
conn = sqlite3.connect(r'C:\sqlite\gui\attendance')
cursor = conn.cursor()

def clean_uid(uid):
    # Remove prefix and extra spaces
    uid = uid.replace("UID: ", "").replace(" ", "").upper()
    return uid

def update_attendance(uid):
    today = time.strftime('%Y-%m-%d')
    cleaned_uid = clean_uid(uid)

    print(f"Normalized UID to check in database: '{cleaned_uid}'")

    cursor.execute("SELECT student_id FROM students WHERE uid = ?", (cleaned_uid,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]
        cursor.execute(
            "INSERT INTO attendance_daily (student_id, date, attended) VALUES (?, ?, 1) "
            "ON CONFLICT(student_id, date) DO UPDATE SET attended=1", 
            (student_id, today)
        )
        conn.commit()
        print(f"Updated attendance for Student ID: {student_id}")
    else:
        print(f"UID {cleaned_uid} not found in database.")

try:
    while True:
        if ser.in_waiting:
            uid = ser.readline().decode().strip()
            print(f"Read UID: {uid}")
            update_attendance(uid)
except KeyboardInterrupt:
    print("Program stopped.")
finally:
    ser.close()
    conn.close()
