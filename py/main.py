import serial
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect(r'C:\sqlite\gui\attendance')
cursor = conn.cursor()

def update_attendance(uid, current_time, status):
    # Extract date and time components
    date, time_part = current_time.split()
    entry_time = exit_time = None

    # Find the student by UID
    cursor.execute("SELECT student_id FROM students WHERE uid = ?", (uid,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]

        if status == 'ENTRY':
            entry_time = time_part
            # Insert or update entry time and set attended to 1
            cursor.execute(
                """
                INSERT OR REPLACE INTO attendance_daily (student_id, date, entry_time, late, attended)
                VALUES (?, ?, ?, COALESCE((SELECT late FROM attendance_daily WHERE student_id = ? AND date = ?), 0), 1)
                """,
                (student_id, date, entry_time, student_id, date)
            )
            # Determine if the student is late (based on entry time)
            if entry_time > '08:00:00':
                cursor.execute(
                    "UPDATE attendance_daily SET late = 1 WHERE student_id = ? AND date = ?",
                    (student_id, date)
                )

        elif status == 'EXIT':
            exit_time = time_part
            # Update exit time and attended to 1
            cursor.execute(
                "UPDATE attendance_daily SET exit_time = ?, attended = 1 WHERE student_id = ? AND date = ?",
                (exit_time, student_id, date)
            )
            # Check if the entry time exists to determine late status
            cursor.execute("SELECT entry_time FROM attendance_daily WHERE student_id = ? AND date = ?", (student_id, date))
            entry_time_record = cursor.fetchone()
            if entry_time_record:
                entry_time = entry_time_record[0]
                # Define 08:00 AM as the threshold for being late
                if entry_time and entry_time > '08:00:00':
                    cursor.execute(
                        "UPDATE attendance_daily SET late = 1 WHERE student_id = ? AND date = ?",
                        (student_id, date)
                    )

        conn.commit()
        print(f"Updated attendance for Student ID: {student_id} on {date} - {status}")
    else:
        print(f"UID {uid} not found in database.")

def send_time_and_status_to_arduino(ser, time_str, status):
    ser.write(f"TIME:{time_str}\n".encode())
    ser.write(f"STATUS:{status}\n".encode())

def main():
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust 'COM3' as needed
        # Ask for the current time and status
        current_time = input("Enter the current time (YYYY-MM-DD HH:MM:SS): ")
        status = input("Enter status (ENTRY/EXIT): ").strip().upper()
        
        if status not in ["ENTRY", "EXIT"]:
            print("Invalid status. Please enter ENTRY or EXIT.")
            return

        send_time_and_status_to_arduino(ser, current_time, status)

        while True:
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                print(f"Received data from Arduino: {data}")  # Debugging line
                uid, time_str, status_received = data.split(',', 2)
                uid = uid.upper()  # Ensure UID is in uppercase
                update_attendance(uid, time_str, status_received)
    except KeyboardInterrupt:
        print("Program stopped.")
    finally:
        ser.close()
        conn.close()

if __name__ == "__main__":
    main()
