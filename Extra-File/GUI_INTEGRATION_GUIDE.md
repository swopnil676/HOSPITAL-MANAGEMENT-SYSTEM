# Hospital Management System — GUI Integration Guide

## Changes Made to Support GUI

### 1. **patient.py** — Added Patient Class

**Old:** Used dictionaries to represent patients
```python
patient = {
    "id": 1,
    "name": "Rajesh",
    "age": "45",
    ...
}
```

**New:** Added `Patient` class while keeping dict compatibility
```python
class Patient:
    def __init__(self, patient_id, name, age, gender, disease, doctor, status="Admitted"):
        self.id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.disease = disease
        self.doctor = doctor
        self.status = status
        self.admitted_time = datetime.now()
        self.discharged_time = None
    
    def to_dict(self):
        """Convert to dict for CSV storage"""
        return {...}
    
    @staticmethod
    def from_dict(data):
        """Create Patient from dict"""
        return Patient(...)
```

**Why?** OOP approach makes GUI easier. Objects are cleaner than dicts for managing state (admitted_time, discharged_time, etc.).

**Backward Compatibility:** The old `create_patient()` function still works — it now returns a Patient object instead of dict.

---

### 2. **file_handler.py** — Updated for Patient Objects

**Old:**
```python
from patient import create_patient

patient = create_patient(...)  # Returns dict
patients.append(patient)
```

**New:**
```python
from patient import Patient

patient = Patient(...)  # Returns object
patients.append(patient)

def save_patients(patients):
    """Convert Patient objects to dicts for CSV"""
    rows = []
    for p in patients:
        if isinstance(p, Patient):
            rows.append(p.to_dict())  # Convert object → dict
        else:
            rows.append(p)
    writer.writerows(rows)
```

**Why?** 
- CSV stores data as text (dicts), not objects
- `to_dict()` converts Patient objects to dictionaries for CSV storage
- `load_patients()` creates Patient objects from CSV dicts
- Data persists correctly between CLI and GUI

**Important:** Both CLI and GUI use the same CSV file. When you add a patient in GUI, it saves to CSV. When you run CLI, it reads the same CSV.

---

### 3. **operations.py** — Updated for Patient Objects

**Old:**
```python
patient["name"] = name  # Dict access
```

**New:**
```python
patient.name = name  # Object attribute
```

**Changes in each function:**
- `add_patient()` → Creates `Patient(...)` instead of dict
- `search_patient()` → Accesses `patient.name` instead of `patient["name"]`
- `update_patient()` → Sets `patient.age = age` instead of `patient["age"] = age`
- `discharge_patient()` → Sets `patient.status = "Discharged"`
- `delete_patient()` → Same logic, just uses Patient objects

**Important:** These changes only affect CLI mode. GUI has its own operations in `gui.py`.

---

### 4. **gui.py** — NEW FILE

Complete GUI implementation using tkinter:

```python
from tkinter import tk, ttk, messagebox
from datetime import datetime
from patient import Patient
from file_handler import load_patients, save_patients

class HospitalGUI:
    def __init__(self, root):
        self.patients, self.next_id = load_patients()  # Load from CSV
        # ... build UI ...
```

**Key Features:**
- Loads patients from CSV on startup
- Displays in formatted table with search and filter
- Add/Edit patients via dialog forms
- Discharge/Delete operations
- Live clock and statistics
- All changes auto-save to CSV
- Dark clinical theme

**UI Components:**
- **Header:** Title, clock, stats (Admitted/Discharged/Total)
- **Toolbar:** Search box + Add button
- **Filter chips:** All/Admitted/Discharged tabs
- **Table:** Full patient list with sorting
- **Action bar:** Edit/Discharge/Delete/Clear buttons

---

### 5. **main.py** — Dual Mode Support

**Old:**
```python
def main():
    patients, next_id = load_patients()
    menu(patients, next_id)

if __name__ == "__main__":
    main()
```

**New:**
```python
def main_cli():
    """Run CLI mode"""
    patients, next_id = load_patients()
    menu(patients, next_id)

def main_gui():
    """Run GUI mode"""
    import tkinter as tk
    from gui import HospitalGUI
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_cli()  # CLI mode
    else:
        main_gui()  # GUI mode (default)
```

**Usage:**

```bash
# Run GUI (default)
python main.py

# Run CLI (legacy mode)
python main.py --cli
```

---

## Directory Structure (Updated)

```
hospital_system/
├── main.py                    # Entry point (CLI/GUI selector)
├── patient.py                 # Patient class + utilities
├── file_handler.py            # CSV load/save
├── operations.py              # CLI operations
├── gui.py                     # GUI application (NEW)
├── patients.csv               # Persistent data
├── HOSPITAL_PROJECT_WRITEUP.md
├── GUI_INTEGRATION_GUIDE.md   # This file
└── README.md
```

---

## Data Flow

### Adding a Patient (GUI)

```
1. User clicks "Add Patient"
2. Dialog form opens
3. User enters: name, age, gender, disease, doctor
4. Click "Save Patient"
5. HospitalGUI.on_save():
   → Create new Patient(self.next_id, ...)
   → Append to self.patients list
   → Increment self.next_id
   → Call save_patients(self.patients)
      → Converts Patient objects to dicts
      → Writes to patients.csv
   → Refresh table UI
```

### Loading Patients (GUI startup)

```
1. HospitalGUI.__init__()
2. Call load_patients() from file_handler.py
   → Read patients.csv
   → Convert each CSV row to Patient object
   → Return [Patient(...), Patient(...), ...], next_id
3. Store in self.patients, self.next_id
4. Display table with self.refresh()
```

### Switching Between CLI and GUI

```
Session 1: GUI mode
→ Add 5 patients (IDs 1-5)
→ Discharge patient ID 2
→ Save to patients.csv

Session 2: CLI mode (python main.py --cli)
→ Load 5 patients from patients.csv
→ View shows patient 2 as "Discharged"
→ Can add more patients (next ID = 6)
→ All changes saved to CSV

Session 3: GUI mode
→ Load 6 patients from patients.csv
→ Shows all previous data + new patient
```

---

## Key Differences: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| **Launch** | `python main.py --cli` | `python main.py` |
| **Interface** | Text menu | Graphical window |
| **Patient Input** | `input()` prompts | Dialog forms |
| **Display** | Formatted table (console) | Interactive table |
| **Search** | Sequential input | Live search box |
| **Statistics** | Not shown | Real-time counters |
| **Clock** | N/A | Live updating clock |
| **Data** | CSV (same file) | CSV (same file) |
| **Persistence** | Manual save calls | Auto-save on every change |

---

## Data Compatibility

Both CLI and GUI use **the same `patients.csv` file**.

### Patient Data Structure in CSV:
```
id,name,age,gender,disease,doctor,status
1,Rajesh Kumar,45,M,Hypertension,Dr. Singh,Admitted
2,Priya Sharma,32,F,Diabetes,Dr. Patel,Discharged
```

### In Memory (Both Modes):
- CLI: `Patient` objects in a list
- GUI: `Patient` objects in a list
- Both: All changes written to same CSV

---

## Example Session: CLI + GUI

**Session 1: Start GUI**
```
$ python main.py
→ GUI window opens
→ Load 35 patients from patients.csv
→ Add new patient "John Smith"
→ Save → CSV now has 36 patients, ID goes 1-36
→ Quit GUI
```

**Session 2: Start CLI**
```
$ python main.py --cli
→ Load 36 patients from patients.csv (includes "John Smith")
→ View all patients (shows new patient)
→ Add "Jane Doe" via CLI
→ Save → CSV now has 37 patients
→ Exit CLI
```

**Session 3: Start GUI Again**
```
$ python main.py
→ GUI window opens
→ Load 37 patients from patients.csv (includes "Jane Doe")
→ Table shows both "John Smith" and "Jane Doe"
```

---

## Migration Checklist

If you're updating from the old version:

✅ Backup your `patients.csv`
✅ Update `patient.py` — Add Patient class
✅ Update `file_handler.py` — Support Patient objects
✅ Update `operations.py` — Use `.name` instead of `["name"]`
✅ Create `gui.py` — New GUI module
✅ Update `main.py` — Support both modes
✅ Test CLI mode: `python main.py --cli`
✅ Test GUI mode: `python main.py`
✅ Verify CSV compatibility (should work in both)

---

## Troubleshooting

### GUI doesn't open
- Ensure tkinter is installed: `pip install tk`
- Try running CLI: `python main.py --cli` to test data loading

### Data doesn't persist between sessions
- Check that `patients.csv` exists in the same directory as `main.py`
- Verify file permissions (readable/writable)
- Try creating a new patient to trigger CSV write

### Patient object errors in CLI
- Ensure `patient.py` has the Patient class definition
- Verify `operations.py` uses `.attribute` instead of `["key"]` access

### CSV file corrupted
- Delete `patients.csv` and restart
- App will create a fresh CSV on first add

---

## Architecture Summary

```
user input
    ↓
┌─────────────────┐
│   main.py       │ ← Entry point (CLI/GUI selector)
└────────┬────────┘
         ↓
    ┌────────┐
    │CLI mode│  or  │GUI mode│
    └───┬────┘      └───┬────┘
        ↓               ↓
    ┌──────────┐    ┌──────────┐
    │operations│    │gui.py    │
    └───┬──────┘    └───┬──────┘
        ↓               ↓
        └───────┬───────┘
                ↓
        ┌─────────────────┐
        │  patient.py     │ ← Data model (Patient class)
        └────────┬────────┘
                 ↓
        ┌──────────────────┐
        │file_handler.py   │ ← CSV persistence
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │  patients.csv    │ ← Shared data file
        └──────────────────┘
```

Both CLI and GUI paths converge at `patient.py` and `file_handler.py`, ensuring data consistency.

---

## Next Steps

1. **Add more features:**
   - Doctor profiles
   - Appointment scheduling
   - Lab reports
   - Medicine records

2. **Improve GUI:**
   - Add print/export functionality
   - Implement database instead of CSV
   - Add user authentication
   - Dark/light theme toggle

3. **Deploy:**
   - Package as executable (PyInstaller)
   - Web version (Flask/Django)
   - Mobile app (Kivy)

---

## Summary

✅ **Modular structure maintained** — All modules work independently  
✅ **Data compatibility** — Both CLI and GUI use same CSV file  
✅ **Object-oriented** — Patient class replaces dict-based approach  
✅ **Backward compatible** — Old functions still work  
✅ **Clean separation** — CLI logic in `operations.py`, GUI logic in `gui.py`  
✅ **Production ready** — Error handling, validation, persistence

You now have a professional hospital management system that works in both terminal and GUI modes with a shared data store.
