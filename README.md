# 🏥 Hospital Management System

A **Python-based Hospital Management System** for managing patient records through both a **GUI and CLI interface**. The project uses **Object-Oriented Programming (OOP)** and **CSV-based storage** to maintain patient data across sessions.

## ✨ Features

* 👤 Add, update, search, and delete patients
* 🏥 Patient admission and discharge management
* 🔎 Search and filter patient records
* 📊 Real-time patient statistics
* 🖥️ Tkinter-based GUI
* 💻 Command-Line Interface
* 💾 Persistent CSV data storage
* 🔄 Shared data between GUI and CLI
* 🧱 OOP-based `Patient` class

## 🛠️ Technologies Used

* **Python**
* **Tkinter**
* **OOP**
* **CSV & File Handling**

## 📂 Project Structure

```text
Hospital-Management-System/
│
├── main.py
├── patient.py
├── file_handler.py
├── operations.py
├── gui.py
├── patients.csv
└── README.md
```

## 🚀 How to Run

### GUI Mode

```bash
python main.py
```

### CLI Mode

```bash
python main.py --cli
```

## 💾 Data Storage

Patient records are stored in `patients.csv`. Both GUI and CLI use the same file, so changes made in one mode are available in the other.

## 🎯 Key Highlights

* Modular multi-file architecture
* Object-oriented patient management
* Persistent data storage
* GUI + CLI support
* Patient admission/discharge tracking
* Search and filtering functionality
* Clean separation of UI, operations, and data handling

## 🔮 Future Improvements

* Doctor and appointment management
* Billing and medicine records
* Database integration with MySQL/SQLite
* User authentication
* PDF report generation

## 👨‍💻 Author

**Swopnil Biswas**

> Built as a Python project to practice **OOP, file handling, GUI development, and modular programming**.

