# 🏥 Hospital Management System

A **Python-based Hospital Management System** developed to manage patient records efficiently through a simple command-line interface with basic GUI support. The project follows a **modular Object-Oriented Programming (OOP)** architecture and uses **CSV files** for persistent data storage.

---

# 📌 Overview

This project provides an efficient way to manage hospital patient records, including adding, viewing, updating, searching, and deleting patient information. The application separates data management, file handling, and user interaction into independent modules, making the system easy to maintain and extend.

---

# ✨ Features

* 🏥 Register new patients
* 📋 View all patient records
* 🔍 Search patients
* ✏️ Update patient information
* 🗑️ Delete patient records
* 🖥️ Simple GUI interface
* 💾 CSV-based persistent storage
* ⚠️ Input validation and exception handling
* 📊 Menu-driven application

---

# 🛠️ Technologies Used

* **Python**
* **Object-Oriented Programming (OOP)**
* **CSV File Handling**
* **Tkinter (GUI)**
* **Command-Line Interface (CLI)**
* **Modular Programming**

---

# 📁 Project Structure

```text
Hospital-Management-System/
│
├── __pycache__/
├── file_handler.py        # CSV file operations
├── gui.py                 # Graphical User Interface
├── main.py                # Application entry point
├── operations.py          # Hospital management operations
├── patient.py             # Patient model
├── patients.csv           # Patient database
└── README.md
```

---

# 📖 Workflow

```text
Program Start
      │
      ▼
main.py
      │
      ▼
Load patients.csv
      │
      ▼
Initialize GUI
      │
      ▼
User Selects Operation
      │
      ├── Add Patient
      ├── View Patients
      ├── Search Patient
      ├── Update Patient
      ├── Delete Patient
      └── Exit
      │
      ▼
operations.py
      │
      ▼
Update Patient Records
      │
      ▼
file_handler.py
      │
      ▼
Save Changes to patients.csv
      │
      ▼
Refresh GUI / Return to Menu
```

---

# 🚀 How to Run

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd Hospital-Management-System
```

### 3. Run the Application

```bash
python main.py
```

---

# 🔄 Data Flow

```text
patients.csv
      ▲
      │
      ▼
file_handler.py
      │
      ▼
operations.py
      │
      ▼
patient.py
      │
      ▼
gui.py
      │
      ▼
main.py
```

---

# 📂 Module Responsibilities

### 📄 main.py

* Entry point of the application
* Initializes the system
* Launches the GUI

### 📄 gui.py

* Provides the graphical interface
* Handles user interactions
* Displays patient information

### 📄 patient.py

* Defines the Patient class
* Stores patient details

### 📄 operations.py

* Implements CRUD operations
* Manages patient records
* Connects the GUI with the data layer

### 📄 file_handler.py

* Reads patient data from CSV
* Writes updated data to CSV
* Handles persistent storage

### 📄 patients.csv

* Stores patient records
* Automatically updated whenever data changes

---

# 🔮 Future Improvements

* 👨‍⚕️ Doctor management
* 📅 Appointment scheduling
* 💊 Medicine & pharmacy management
* 🧾 Billing and payment system
* 🛏️ Bed and ward management
* 🗄️ MySQL / SQLite database integration
* 🌐 Web-based Hospital Management System

---

# 👨‍💻 Author

**Swopnil Biswas**

B.Tech – Electronics & Communication Engineering

---

⭐ **A practical Python project built to strengthen Object-Oriented Programming, CSV file handling, GUI development, modular programming, and real-world healthcare application development.**
