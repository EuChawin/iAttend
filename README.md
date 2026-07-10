# iAttend — RFID Student Attendance System 🎓

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![PHP](https://img.shields.io/badge/php-8.x-purple.svg)
![Arduino](https://img.shields.io/badge/arduino-uno-teal.svg)

**iAttend** is a complete hardware-software hybrid attendance system designed for educational institutions. It uses an Arduino-powered RFID reader, a Python desktop client for processing scans in real-time, an SQLite database for lightweight local storage, and a modern PHP web dashboard for students to view their records.

Originally developed for *Assumption College Nakhonratchasima (ACN)*.

## ✨ Features

- **Real-Time RFID Scanning**: Instant logging of entry and exit times via an Arduino MFRC522 reader.
- **Python Desktop GUI**: A clean control panel for teachers to manage the reader, add new students, and modify attendance records manually.
- **Modern Web Dashboard**: A responsive, dark-theme web portal for students to check their daily attendance, calculate their attendance percentage, and track late arrivals.
- **Clean Architecture**: Separation of concerns between hardware, middleware, database, and web frontend.

## 🏗️ Project Architecture

```text
[ Arduino RFID Reader ] 
       │ 
    (Serial USB)
       │
[ Python Desktop App ] ──(Reads/Writes)──> [ SQLite Database ]
                                                │
                                            (Reads)
                                                │
                                     [ PHP Web Dashboard ]
```

## 🛠️ Hardware Setup

### Requirements
- Arduino Uno / Nano
- MFRC522 RFID Module
- Breadboard & Jumper wires
- 3x LEDs (Blue, Green, Red)

### Wiring Guide
| MFRC522 Pin | Arduino Pin |
|-------------|-------------|
| SDA (SS)    | 10          |
| SCK         | 13          |
| MOSI        | 11          |
| MISO        | 12          |
| RST         | 9           |

| Component   | Arduino Pin |
|-------------|-------------|
| Ready LED   | 7           |
| Success LED | 6           |
| Error LED   | 5           |

## 🚀 Installation & Usage

### 1. Database Setup
The system uses SQLite. The database schema is documented in `database/schema.sql`.
The database file `attendance.db` will be created automatically when you run the Python application.

### 2. Arduino Firmware
1. Open `arduino/rfid_reader/rfid_reader.ino` in the Arduino IDE.
2. Install the `MFRC522` library via the Library Manager.
3. Flash to your Arduino board.

### 3. Python Desktop Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your COM port in `desktop/config.py`.
3. Run the main system:
   ```bash
   python desktop/main.py
   ```
*(Additional tools available: `desktop/attendance_records.py` and `desktop/students.py` for manual database management).*

### 4. Web Dashboard
1. Point your local PHP server (XAMPP, WAMP, or PHP Built-in Server) to the `web/` directory.
   ```bash
   cd web
   php -S localhost:8000
   ```
2. Open `http://localhost:8000` in your browser.
3. Login using a registered Student ID.

## 📸 Screenshots

*(Add screenshots of the Web Dashboard and Python GUI here in `docs/screenshots/`)*

## 📄 License

This project is open-source and available under the MIT License.
