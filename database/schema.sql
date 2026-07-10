-- iAttend Database Schema
-- Run this file against a new SQLite database to initialise the structure.

-- Students Table
-- Stores the registered students and their corresponding RFID UIDs.
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,           -- The RFID card unique identifier
    student_id TEXT UNIQUE NOT NULL,    -- The school-issued student ID number
    name TEXT NOT NULL                  -- Full name of the student
);

-- Daily Attendance Table
-- Stores the entry and exit logs for each student per day.
CREATE TABLE IF NOT EXISTS attendance_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,           -- References students.student_id
    date TEXT NOT NULL,                 -- Format: YYYY-MM-DD
    entry_time TEXT,                    -- Format: HH:MM:SS
    exit_time TEXT,                     -- Format: HH:MM:SS
    late INTEGER DEFAULT 0,             -- 1 if late, 0 if on time
    attended INTEGER DEFAULT 0,         -- 1 if present, 0 if absent
    UNIQUE(student_id, date)
);

-- Demo Data (Optional)
-- INSERT INTO students (uid, student_id, name) VALUES ('A1B2C3D4', '12345', 'John Doe');
