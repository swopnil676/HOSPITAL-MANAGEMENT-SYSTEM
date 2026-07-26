# Hospital Patient Records Management System
## Complete Project Documentation

---

## 1. Project Overview

**What is it?**
A command-line hospital management system that handles patient records. It allows medical staff to add, view, search, update, and manage patient information with persistent CSV-based storage.

**Why build it?**
- Demonstrates core Python skills: OOP, file I/O, data structures, error handling
- Shows modular architecture and separation of concerns
- Real-world use case (healthcare records)
- Portfolio-ready project structure

**Tech Stack:**
- **Language:** Python 3
- **Storage:** CSV (simple, portable, no database needed)
- **Design Pattern:** Modular (separate files for different concerns)

---

## 2. Architecture & Design Philosophy

### Separation of Concerns
The project is split into 4 independent modules, each with a single responsibility:

```
hospital_system/
├── main.py              → Entry point & menu system
├── patient.py           → Data model & utilities
├── file_handler.py      → CSV persistence
├── operations.py        → Business logic
├── data.csv             → Persistent storage
└── README.md
```

**Why this structure?**
- **Maintainable:** Changes in one module don't break others
- **Testable:** Each module can be tested independently
- **Scalable:** Easy to add new features
- **Professional:** Mimics real-world software architecture

### Key Design Patterns

**1. Data Model (patient.py)**
The `create_patient()` function encapsulates patient object creation. Any change to patient schema happens in one place.

**2. Utility Functions (patient.py)**
Helper functions for common operations:
- `find_patient_by_id()` — Lookup single patient
- `find_patients_by_keyword()` — Search multiple patients
- `display_patient()` — Formatted output
- `display_patients_table()` — Table view

**3. File Abstraction (file_handler.py)**
All CSV operations are isolated. If you later switch to a database, only this module changes.

**4. Business Logic (operations.py)**
Every user-facing operation (add, update, delete) imports functions from other modules and orchestrates them. This is the "glue" that brings everything together.

---

## 3. Detailed Module Breakdown

### Module 1: `patient.py` — Data Model & Display

**Purpose:** Define what a patient is and how to display patients.

**Functions:**

#### `create_patient(patient_id, name, age, gender, disease, doctor, status="Admitted")`
Creates a patient dictionary.
```python
patient = create_patient(1, "Rajesh", 45, "M", "Hypertension", "Dr. Singh")
# Returns: {
#   "id": 1,
#   "name": "Rajesh",
#   "age": "45",
#   "gender": "M",
#   "disease": "Hypertension",
#   "doctor": "Dr. Singh",
#   "status": "Admitted"
# }
```
**Why encapsulate?** If patient structure changes (add email, phone, etc.), change only this function.

#### `find_patient_by_id(patients, patient_id)`
Searches a patient list for a specific ID.
```python
patient = find_patient_by_id(patients, 5)
if patient:
    print(f"Found: {patient['name']}")
else:
    print("Not found")
```
Returns the patient dict or `None`.

#### `find_patients_by_keyword(patients, keyword)`
Searches by ID (exact match) or name (substring match).
```python
results = find_patients_by_keyword(patients, "rajesh")
# Returns list of all patients with "rajesh" in name (case-insensitive)

results = find_patients_by_keyword(patients, "5")
# Returns list with patient ID=5 (if exists)
```

#### `display_patient(patient)`
Prints a single patient's details formatted nicely.
```python
display_patient(patient)
# Output:
# ID: 1
# Name: Rajesh Kumar
# Age: 45
# Gender: M
# Disease: Hypertension
# Doctor: Dr. Singh
# Status: Admitted
```

#### `display_patients_table(patients)`
Prints all patients in a formatted table.
```
ID   Name           Age  Sex  Disease        Doctor         Status    
1    Rajesh Kumar   45   M    Hypertension   Dr. Singh      Admitted
2    Priya Sharma   32   F    Diabetes       Dr. Patel      Admitted
```

---

### Module 2: `file_handler.py` — CSV Persistence

**Purpose:** Load and save patient data to CSV file.

**Key Concept:** The CSV file is the "database." Every time data changes, we write the entire updated list back to the file.

#### `load_patients()`

**What it does:**
1. Check if CSV file exists
2. If not, return empty list with starting ID = 1
3. If yes, read every row from CSV
4. Convert each row to a patient dict
5. Track the highest ID seen
6. Return list of patients + next available ID

**Line-by-line breakdown:**

```python
def load_patients():
    patients = []  # Empty list to fill
    
    if not os.path.exists(PATIENTS_FILE):
        return patients, 1  # No file yet, start fresh with ID=1
```
If file doesn't exist (first run), return empty list and ID=1.

```python
    try:
        with open(PATIENTS_FILE, "r", newline="") as f:
```
Open file in read mode. `newline=""` is a CSV best practice (handles line endings properly).

```python
            reader = csv.DictReader(f, fieldnames=FIELDNAMES)
            next(reader, None)  # Skip header if it exists
```
`DictReader` reads the CSV and converts each row to a dictionary. The column names are taken from `FIELDNAMES`.

Example: CSV row `1,Rajesh,45,M,Hypertension,Dr. Singh,Admitted` becomes:
```python
{
    "id": "1",
    "name": "Rajesh",
    "age": "45",
    ...
}
```

`next(reader, None)` skips the first row (which is the header: id, name, age, ...).

```python
            max_id = 0
            for row in reader:
                if row and row.get("id"):
```
Loop through each row. Check that row exists and has an "id" field.

```python
                    try:
                        patient = create_patient(
                            patient_id=int(row["id"]),  # Convert "1" → 1
                            name=row["name"],
                            age=row["age"],
                            ...
                        )
                        patients.append(patient)
                        max_id = max(max_id, int(row["id"]))
```
For each valid row:
- Convert ID from string to int
- Create patient dict using `create_patient()`
- Add to list
- Update `max_id` if this ID is higher

**Why track max_id?** To ensure the next new patient gets a unique ID. If highest ID is 35, next patient gets ID 36.

```python
                    except (ValueError, KeyError):
                        continue  # Skip malformed rows
```
If a row has bad data (invalid ID, missing field), skip it instead of crashing.

```python
            next_id = max_id + 1
            return patients, next_id
```
Return the patient list + the next available ID.

```python
    except Exception as e:
        print(f"Error loading patients: {e}\n")
        return patients, 1  # If something goes wrong, return empty list + ID=1
```

---

#### `save_patients(patients)`

**What it does:**
Takes the patient list and writes it to CSV file.

```python
def save_patients(patients):
    try:
        with open(PATIENTS_FILE, "w", newline="") as f:  # "w" = write mode (overwrites)
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()  # Write the header row: id,name,age,...
            writer.writerows(patients)  # Write each patient as a CSV row
    except Exception as e:
        print(f"Error saving patients: {e}\n")
```

**Step-by-step:**
1. Open file in write mode (overwrites if exists)
2. Create a `DictWriter` (converts dicts → CSV rows)
3. `writeheader()` writes the column names
4. `writerows(patients)` writes each patient dict as a CSV row

**Important:** This function is called every time data changes (add, update, delete). The CSV is always in sync with the in-memory list.

---

### Module 3: `operations.py` — Business Logic

**Purpose:** Implement all user-facing operations (add, view, search, update, discharge, delete).

Each function:
- Takes the patients list (and `next_id` if needed)
- Modifies the list or displays data
- Calls `save_patients()` if data changed
- Returns updated `next_id` (for add operation)

#### `add_patient(patients, next_id)`

**Flow:**
1. Ask user for name, age, gender, disease, doctor
2. Create patient dict with auto-incrementing ID
3. Append to list
4. Save to CSV
5. Return next_id + 1

```python
def add_patient(patients, next_id):
    name = input("Enter patient name: ").strip()
    age = input("Enter patient age: ").strip()
    gender = input("Enter gender (M/F/O): ").strip().upper()
    disease = input("Enter disease/diagnosis: ").strip()
    doctor = input("Enter assigned doctor: ").strip()

    patient = create_patient(next_id, name, age, gender, disease, doctor)
    patients.append(patient)
    save_patients(patients)  # Write to CSV immediately
    
    print(f"Patient added successfully! ID: {patient['id']}\n")
    return next_id + 1  # Next ID for next patient
```

**Example execution:**
```
Enter patient name: Amit Singh
Enter patient age: 50
Enter gender (M/F/O): M
Enter disease/diagnosis: Asthma
Enter assigned doctor: Dr. Reddy

→ Created patient with ID 36 (next_id incremented)
→ Written to CSV
→ next_id is now 37 for next addition
```

#### `view_patients(patients)`

**Flow:**
1. Check if patients list is empty
2. If empty, say so
3. If not, display formatted table

```python
def view_patients(patients):
    if not patients:
        print("No patient records found.\n")
        return
    
    display_patients_table(patients)  # Call utility from patient.py
```

#### `search_patient(patients)`

**Flow:**
1. Ask user for ID or name
2. Find matching patients
3. Display each result

```python
def search_patient(patients):
    keyword = input("Enter Patient ID or Name to search: ").strip()
    results = find_patients_by_keyword(patients, keyword)  # Utility from patient.py
    
    if not results:
        print("No matching patient found.\n")
        return

    for p in results:
        display_patient(p)  # Utility from patient.py
    print()
```

**Example:**
```
Enter Patient ID or Name to search: rajesh

→ Found 2 patients with "rajesh" in name
→ Display details for each
```

#### `update_patient(patients)`

**Flow:**
1. Ask for patient ID to update
2. Find the patient
3. Ask which fields to change (blank = keep current)
4. Update fields that were entered
5. Save to CSV

```python
def update_patient(patients):
    patient_id = input("Enter Patient ID to update: ").strip()
    
    if not patient_id.isdigit():
        print("Invalid ID.\n")
        return

    patient = find_patient_by_id(patients, int(patient_id))
    
    if not patient:
        print("Patient not found.\n")
        return

    print("Leave field blank to keep current value.")
    name = input(f"Name [{patient['name']}]: ").strip()
    age = input(f"Age [{patient['age']}]: ").strip()
    disease = input(f"Disease [{patient['disease']}]: ").strip()
    doctor = input(f"Doctor [{patient['doctor']}]: ").strip()

    # Only update if user entered something
    if name:
        patient["name"] = name
    if age:
        patient["age"] = age
    if disease:
        patient["disease"] = disease
    if doctor:
        patient["doctor"] = doctor

    save_patients(patients)
    print("Patient record updated.\n")
```

**Example:**
```
Enter Patient ID to update: 5
Name [Priya Sharma]: 
Age [32]: 33
Disease [Diabetes]: 
Doctor [Dr. Patel]: Dr. Kumar

→ Age changed from 32 → 33
→ Doctor changed from Dr. Patel → Dr. Kumar
→ Saved to CSV
```

#### `discharge_patient(patients)`

**Flow:**
1. Ask for patient ID
2. Find patient
3. Set status to "Discharged"
4. Save to CSV

```python
def discharge_patient(patients):
    patient_id = input("Enter Patient ID to discharge: ").strip()
    
    if not patient_id.isdigit():
        print("Invalid ID.\n")
        return

    patient = find_patient_by_id(patients, int(patient_id))
    
    if not patient:
        print("Patient not found.\n")
        return

    patient["status"] = "Discharged"
    save_patients(patients)
    
    print(f"{patient['name']} has been discharged.\n")
```

#### `delete_patient(patients)`

**Flow:**
1. Ask for patient ID
2. Find patient
3. Remove from list
4. Save to CSV

```python
def delete_patient(patients):
    patient_id = input("Enter Patient ID to delete: ").strip()
    
    if not patient_id.isdigit():
        print("Invalid ID.\n")
        return

    patient = find_patient_by_id(patients, int(patient_id))
    
    if not patient:
        print("Patient not found.\n")
        return

    patients.remove(patient)  # Remove from list
    save_patients(patients)  # Write updated list to CSV
    
    print("Patient record deleted.\n")
```

---

### Module 4: `main.py` — Entry Point & Menu

**Purpose:** Start the app and handle user interaction.

```python
def main():
    """Initialize and run the application"""
    patients, next_id = load_patients()  # Load from CSV
    menu(patients, next_id)  # Start menu loop


def menu(patients, next_id):
    """Display menu and handle user choices"""
    while True:
        print("===== Hospital Patient Records =====")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Discharge Patient")
        print("6. Delete Patient")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            next_id = add_patient(patients, next_id)  # Returns updated next_id
        elif choice == "2":
            view_patients(patients)
        elif choice == "3":
            search_patient(patients)
        elif choice == "4":
            update_patient(patients)
        elif choice == "5":
            discharge_patient(patients)
        elif choice == "6":
            delete_patient(patients)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
```

**Key points:**
- `load_patients()` reads CSV and gets patients + next_id
- Menu loop continues until user picks "Exit"
- Each operation updates `patients` list
- After each operation, loop continues (user back to menu)
- If user picks "Add Patient", `next_id` is updated and passed back to menu

---

## 4. Complete Execution Flow

**User runs:** `python main.py`

```
Step 1: main() executes
    ↓
Step 2: load_patients() called
    → Opens data.csv (if exists)
    → Reads all 35 patient rows
    → Converts to patient dicts
    → Returns: patients=[...35 patients...], next_id=36
    ↓
Step 3: menu(patients, next_id) called
    → Infinite loop starts
    ↓
Step 4: Display menu options 1-7
    ↓
Step 5: User enters choice (e.g., "1" for Add)
    ↓
Step 6: Call add_patient(patients, next_id)
    → Ask for name, age, gender, disease, doctor
    → Create patient dict with ID=36
    → Append to patients list
    → Call save_patients(patients)
        → Open data.csv in write mode
        → Write header row
        → Write all 36 patient rows to CSV
    → Print success message
    → Return next_id=37
    ↓
Step 7: Update next_id to 37
    ↓
Step 8: Loop continues, back to Step 4
    ↓
Step 9: User picks option "7" (Exit)
    ↓
Step 10: Break loop, print "Goodbye!", program ends
    → CSV is already saved from last operation
```

---

## 5. Key Features

| Feature | Implementation | Storage |
|---------|----------------|---------|
| **Add Patient** | Auto-incrementing ID based on highest existing | CSV updated immediately |
| **View All** | Formatted table with all fields | From memory (loaded from CSV) |
| **Search** | By ID (exact) or name (substring, case-insensitive) | From memory |
| **Update** | Selective fields (blank = keep current) | CSV updated immediately |
| **Discharge** | Change status from "Admitted" → "Discharged" | CSV updated immediately |
| **Delete** | Remove from list | CSV updated immediately |
| **Persistence** | All changes save to CSV instantly | Never lost between runs |
| **Error Handling** | Invalid input, missing files, corrupted data | Graceful fallback to empty state |

---

## 6. Data Structure

### Patient Dictionary
```python
{
    "id": 1,              # Unique auto-incrementing integer
    "name": "Rajesh",     # String
    "age": "45",          # String (from CSV)
    "gender": "M",        # "M", "F", or "O"
    "disease": "Hypertension",  # String
    "doctor": "Dr. Singh",      # String
    "status": "Admitted"  # "Admitted" or "Discharged"
}
```

### CSV Structure
```
id,name,age,gender,disease,doctor,status
1,Rajesh Kumar,45,M,Hypertension,Dr. Singh,Admitted
2,Priya Sharma,32,F,Diabetes,Dr. Patel,Admitted
3,Amit Verma,58,M,Heart Disease,Dr. Gupta,Discharged
...
```

---

## 7. Error Handling Strategy

**Problem → Solution:**

| Issue | Handled By | Solution |
|-------|-----------|----------|
| CSV file doesn't exist | `load_patients()` | Return empty list, start ID=1 |
| Corrupted/malformed rows | `load_patients()` | Skip bad rows, continue reading |
| Invalid user input (non-digit ID) | Each operation | Validate with `.isdigit()`, ask again |
| Patient ID not found | Each operation | Print "Not found", return to menu |
| CSV write fails | `save_patients()` | Print error, continue (data in memory) |
| Missing fields in CSV | `load_patients()` | Skip row using `try/except` |

---

## 8. Why This Architecture?

### Modular Design Benefits

**1. Single Responsibility**
- `patient.py` = Patient concepts only
- `file_handler.py` = CSV I/O only
- `operations.py` = User interactions only
- `main.py` = Orchestration only

**2. Easy to Test**
```python
# Can test patient.py without touching CSV
patients = [create_patient(1, "Test", 30, "M", "Cold", "Dr. X")]
result = find_patients_by_keyword(patients, "Test")
assert len(result) == 1
```

**3. Easy to Extend**
Want to add a feature like "Update doctor for all patients with disease X"?
- Add function to `operations.py`
- Use existing utilities from `patient.py`
- Call `save_patients()` when done
- Add menu option in `main.py`

**4. Easy to Migrate**
Want to switch from CSV to database?
- Rewrite only `file_handler.py`
- Everything else stays the same
- `load_patients()` and `save_patients()` have same interface

---

## 9. Setup & Usage

### Installation
```bash
# No external dependencies needed (Python built-ins only)
python main.py
```

### First Run
```
CSV file doesn't exist → Create empty
Next ID = 1
Show empty menu
```

### Adding Data
```
1. Choose option 1 (Add Patient)
2. Enter name, age, gender, disease, doctor
3. Data saved to data.csv immediately
4. Next patient gets ID = current_max_id + 1
```

### Persistent Data
```
Session 1: Add 5 patients (IDs 1-5) → Save to CSV
Close program
Session 2: Load program → Load 5 patients from CSV
Add 1 patient → Gets ID 6 (not 1 again)
```

---

## 10. Portfolio Value

**This project demonstrates:**

✅ **OOP Principles**
- Data encapsulation (patient.py)
- Separation of concerns
- DRY (Don't Repeat Yourself)

✅ **File I/O**
- CSV reading/writing
- File existence checks
- Error handling with files

✅ **Data Structures**
- Lists (patient collection)
- Dictionaries (patient records)
- Iteration and searching

✅ **Error Handling**
- Try/except blocks
- Graceful degradation
- User input validation

✅ **Business Logic**
- CRUD operations (Create, Read, Update, Delete)
- Search algorithms
- State management (next_id tracking)

✅ **Professional Practices**
- Modular architecture
- Meaningful function/variable names
- Comments and docstrings
- Consistent code style

**Interview Talking Points:**
- "I designed this with modularity in mind — each module has one job"
- "CSV persistence ensures data survives application restart"
- "Error handling prevents crashes from bad CSV data or invalid input"
- "Easy to extend — adding new features doesn't require rewriting existing code"
- "Could easily migrate to database without changing other modules"

---

## 11. Sample Session

```
===== Hospital Patient Records =====
1. Add Patient
2. View All Patients
3. Search Patient
4. Update Patient
5. Discharge Patient
6. Delete Patient
7. Exit
Choose an option: 2

ID   Name           Age  Sex  Disease        Doctor         Status    
1    Rajesh Kumar   45   M    Hypertension   Dr. Singh      Admitted
2    Priya Sharma   32   F    Diabetes       Dr. Patel      Admitted
...
35   Pranav Misra   41   M    Depression     Dr. Patel      Admitted

===== Hospital Patient Records =====
Choose an option: 1
Enter patient name: Neha Verma
Enter patient age: 28
Enter gender (M/F/O): F
Enter disease/diagnosis: Thyroid
Enter assigned doctor: Dr. Nair
Patient added successfully! ID: 36

===== Hospital Patient Records =====
Choose an option: 3
Enter Patient ID or Name to search: neha

ID: 36
Name: Neha Verma
Age: 28
Gender: F
Disease: Thyroid
Doctor: Dr. Nair
Status: Admitted

===== Hospital Patient Records =====
Choose an option: 7
Goodbye!
```

**Behind the scenes:**
- Added patient with auto-ID 36
- Saved all 36 patients to data.csv
- Searched and found the new patient
- Program ended (data persisted)

---

## Conclusion

This is a **complete, professional project** that shows:
- Understanding of software architecture
- Ability to build maintainable code
- Knowledge of Python fundamentals
- Problem-solving (CSV persistence, ID tracking)
- Real-world thinking (error handling, user experience)

It's **portfolio-ready** and demonstrates skills employers look for in junior developers.
