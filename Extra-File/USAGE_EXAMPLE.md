# Hospital Management System — Complete Usage Example

## Setup & Run

**1. Create project directory:**
```bash
mkdir hospital_system
cd hospital_system
```

**2. Files to create:**
```
hospital_system/
├── main.py
├── patient.py
├── file_handler.py
├── operations.py
├── gui.py
└── patients.csv (auto-generated on first run)
```

---

## Example 1: Starting with GUI

### Step 1: Start the Application (GUI Mode)

```bash
$ python main.py
```

**Result:** A window opens with the title "Hospital — Patient Record System"

```
┌─────────────────────────────────────────────────────────────────┐
│ Hospital Patient Records        02:45:30 PM                     │
│ MANAGEMENT SYSTEM               Mon, 26 Jul 2026                │
│                                 Admitted: 5  Discharged: 0      │
│                                 Total: 5                         │
├─────────────────────────────────────────────────────────────────┤
│ 🔍 Search by name or patient ID…  ＋ Add Patient                │
│ ALL  ADMITTED  DISCHARGED                                        │
├─────────────────────────────────────────────────────────────────┤
│ ID    Name           Age  Sex  Diagnosis      Doctor     Status  │
├─────────────────────────────────────────────────────────────────┤
│ 001   Rajesh Kumar   45   M    Hypertension   Dr. Singh  Admit…  │
│ 002   Priya Sharma   32   F    Diabetes       Dr. Patel  Admit…  │
│ 003   Amit Verma     58   M    Heart Disease  Dr. Gupta  Disch…  │
│ 004   Sneha Das      27   F    Migraine       Dr. Nair   Admit…  │
│ 005   Vikram Singh   50   M    Asthma         Dr. Reddy  Admit…  │
├─────────────────────────────────────────────────────────────────┤
│ Edit  Discharge  Delete  Clear All Records      [Ready]         │
└─────────────────────────────────────────────────────────────────┘
```

---

### Step 2: Add a New Patient (GUI)

**Action:** Click "＋ Add Patient" button

**Dialog appears:**
```
┌──────────────────────────────┐
│ Admit New Patient            │
├──────────────────────────────┤
│ Full name                    │
│ ┌──────────────────────────┐ │
│ │                          │ │ ← Type: Mohammad Ali
│ └──────────────────────────┘ │
│ Age                          │
│ ┌──────────────────────────┐ │
│ │ 35                       │ │ ← Type: 35
│ └──────────────────────────┘ │
│ Gender                       │
│ ┌──────────────────────────┐ │
│ │ M (dropdown)             │ │ ← Select: M
│ └──────────────────────────┘ │
│ Diagnosis                    │
│ ┌──────────────────────────┐ │
│ │ Fever                    │ │ ← Type: Fever
│ └──────────────────────────┘ │
│ Assigned doctor              │
│ ┌──────────────────────────┐ │
│ │ Dr. Ahmed Khan           │ │ ← Type: Dr. Ahmed Khan
│ └──────────────────────────┘ │
│ ┌──────┐ ┌──────────────────┐ │
│ │Cancel│ │  Save Patient    │ │
│ └──────┘ └──────────────────┘ │
└──────────────────────────────┘
```

**Action:** Fill form and click "Save Patient"

**Result:** 
- Dialog closes
- Table refreshes with new patient
- Status message shows: "Patient added — ID #006"
- Statistics update: "Admitted: 6"
- Data saved to `patients.csv`

**Table now shows:**
```
│ 001   Rajesh Kumar     45   M    Hypertension   Dr. Singh       Admitted  │
│ 002   Priya Sharma     32   F    Diabetes       Dr. Patel       Admitted  │
│ 003   Amit Verma       58   M    Heart Disease  Dr. Gupta       Discharged│
│ 004   Sneha Das        27   F    Migraine       Dr. Nair        Admitted  │
│ 005   Vikram Singh     50   M    Asthma         Dr. Reddy       Admitted  │
│ 006   Mohammad Ali     35   M    Fever          Dr. Ahmed Khan  Admitted  │ ← NEW
```

---

### Step 3: Search for a Patient (GUI)

**Action:** Type in search box "priya"

**Result:** Table filters to show only matching patients:
```
│ 002   Priya Sharma     32   F    Diabetes       Dr. Patel       Admitted  │
```

**Action:** Clear search, type "3" (to search by ID)

**Result:** Shows patient ID 003:
```
│ 003   Amit Verma       58   M    Heart Disease  Dr. Gupta       Discharged│
```

---

### Step 4: Click Filter Chip "DISCHARGED"

**Action:** Click the chip labeled "DISCHARGED"

**Result:** Table shows only discharged patients:
```
│ 003   Amit Verma       58   M    Heart Disease  Dr. Gupta       Discharged│
│ Stats update: Admitted: 5  Discharged: 1  Total: 6
```

**Action:** Click "ALL" chip to show all patients again

---

### Step 5: Edit a Patient (GUI)

**Action:** Double-click on "Rajesh Kumar" row (or select + click Edit)

**Dialog opens:**
```
┌──────────────────────────────────────┐
│ Edit Record — ID #001                │
├──────────────────────────────────────┤
│ Full name                            │
│ ┌──────────────────────────────────┐ │
│ │ Rajesh Kumar                     │ │
│ └──────────────────────────────────┘ │
│ Age                                  │
│ ┌──────────────────────────────────┐ │
│ │ 45                               │ │ ← Change to: 46
│ └──────────────────────────────────┘ │
│ Gender                               │
│ ┌──────────────────────────────────┐ │
│ │ M                                │ │
│ └──────────────────────────────────┘ │
│ Diagnosis                            │
│ ┌──────────────────────────────────┐ │
│ │ Hypertension                     │ │ ← Change to: Stage 2 Hypertension
│ └──────────────────────────────────┘ │
│ Assigned doctor                      │
│ ┌──────────────────────────────────┐ │
│ │ Dr. Singh                        │ │ ← Change to: Dr. Sharma
│ └──────────────────────────────────┘ │
│ ┌──────┐ ┌──────────────────────────┐ │
│ │Cancel│ │  Update Record           │ │
│ └──────┘ └──────────────────────────┘ │
└──────────────────────────────────────┘
```

**Action:** 
- Change Age: 45 → 46
- Change Diagnosis: "Hypertension" → "Stage 2 Hypertension"
- Change Doctor: "Dr. Singh" → "Dr. Sharma"
- Click "Update Record"

**Result:**
- Dialog closes
- Table refreshes with updated data
- Status: "Patient record updated."
- CSV file updated

**Table shows:**
```
│ 001   Rajesh Kumar   46   M    Stage 2 Hypertension   Dr. Sharma  Admitted  │
```

---

### Step 6: Discharge a Patient (GUI)

**Action:** Select "Vikram Singh" row and click "Discharge" button

**Confirmation dialog:**
```
┌─────────────────────────────────┐
│ Discharge patient?              │
├─────────────────────────────────┤
│ Mark Vikram Singh as discharged?│
├─────────────────────────────────┤
│      [No]       [Yes]           │
└─────────────────────────────────┘
```

**Action:** Click "Yes"

**Result:**
- Status changes to "Discharged"
- Discharged time is recorded
- Stats update: "Admitted: 4  Discharged: 2"
- CSV saved
- Status message: "Vikram Singh has been discharged."

**Table shows:**
```
│ 005   Vikram Singh   50   M    Asthma         Dr. Reddy  Discharged  │
                                                             ↑
                                                        Status changed
```

---

### Step 7: Delete a Patient (GUI)

**Action:** Select a patient and click "Delete" button

**Confirmation dialog:**
```
┌──────────────────────────────────────────┐
│ Delete record?                           │
├──────────────────────────────────────────┤
│ Permanently delete Sneha Das's record?   │
│ This can't be undone.                    │
├──────────────────────────────────────────┤
│        [No]           [Yes]              │
└──────────────────────────────────────────┘
```

**Action:** Click "Yes"

**Result:**
- Patient removed from table
- Stats update: "Total: 5"
- CSV file updated
- Status: "Patient record deleted."

**Table now shows 5 patients (Sneha Das is gone):**
```
│ 001   Rajesh Kumar     46   M    Stage 2 Hypertension   Dr. Sharma    Admitted   │
│ 002   Priya Sharma     32   F    Diabetes               Dr. Patel     Admitted   │
│ 003   Amit Verma       58   M    Heart Disease          Dr. Gupta     Discharged │
│ 005   Vikram Singh     50   M    Asthma                 Dr. Reddy     Discharged │
│ 006   Mohammad Ali     35   M    Fever                  Dr. Ahmed Khan Admitted  │
```

---

### Step 8: Close GUI

**Action:** Close the window (click X button)

**Result:**
- All data is saved in `patients.csv`
- GUI closes
- Data persists for next session

---

## Example 2: Switch to CLI Mode

### Step 1: Run CLI

```bash
$ python main.py --cli
```

**Result:**
```
===== Hospital Patient Records =====
1. Add Patient
2. View All Patients
3. Search Patient
4. Update Patient
5. Discharge Patient
6. Delete Patient
7. Exit
Choose an option: 
```

---

### Step 2: View All Patients (CLI)

```
Choose an option: 2
```

**Output:**
```
ID   Name               Age  Sex  Disease                    Doctor         Status
---  ---                ---  ---  -------                    ------         ------
001  Rajesh Kumar       46   M    Stage 2 Hypertension       Dr. Sharma     Admitted
002  Priya Sharma       32   F    Diabetes                   Dr. Patel      Admitted
003  Amit Verma         58   M    Heart Disease              Dr. Gupta      Discharged
005  Vikram Singh       50   M    Asthma                     Dr. Reddy      Discharged
006  Mohammad Ali       35   M    Fever                      Dr. Ahmed Khan Admitted
```

**Note:** 
- All GUI changes are visible (age 46, new doctor, new patient Mohammad Ali)
- Patient 004 (Sneha Das) is gone (deleted in GUI)
- Data is consistent between GUI and CLI!

---

### Step 3: Search Patient (CLI)

```
Choose an option: 3
Enter Patient ID or Name to search: mohammad
```

**Output:**
```
ID: 6
Name: Mohammad Ali
Age: 35
Gender: M
Disease: Fever
Doctor: Dr. Ahmed Khan
Status: Admitted
```

---

### Step 4: Add Patient (CLI)

```
Choose an option: 1
Enter patient name: Fatima Khan
Enter patient age: 28
Enter gender (M/F/O): F
Enter disease/diagnosis: Asthma
Enter assigned doctor: Dr. Bilal Ahmed
Patient added successfully! ID: 7
```

**Result:** New patient added with auto-incremented ID (7, not 1)

---

### Step 5: View Again (CLI)

```
Choose an option: 2
```

**Output:**
```
ID   Name               Age  Sex  Disease                    Doctor           Status
---  ---                ---  ---  -------                    ------           ------
001  Rajesh Kumar       46   M    Stage 2 Hypertension       Dr. Sharma       Admitted
002  Priya Sharma       32   F    Diabetes                   Dr. Patel        Admitted
003  Amit Verma         58   M    Heart Disease              Dr. Gupta        Discharged
005  Vikram Singh       50   M    Asthma                     Dr. Reddy        Discharged
006  Mohammad Ali       35   M    Fever                      Dr. Ahmed Khan   Admitted
007  Fatima Khan        28   F    Asthma                     Dr. Bilal Ahmed  Admitted ← NEW
```

---

### Step 6: Exit CLI

```
Choose an option: 7
Goodbye!
```

---

## Example 3: Back to GUI (Data Persistence)

### Step 1: Run GUI Again

```bash
$ python main.py
```

**Result:** GUI loads with all data preserved:
```
│ 001   Rajesh Kumar     46   M    Stage 2 Hypertension   Dr. Sharma      Admitted   │
│ 002   Priya Sharma     32   F    Diabetes               Dr. Patel       Admitted   │
│ 003   Amit Verma       58   M    Heart Disease          Dr. Gupta       Discharged │
│ 005   Vikram Singh     50   M    Asthma                 Dr. Reddy       Discharged │
│ 006   Mohammad Ali     35   M    Fever                  Dr. Ahmed Khan  Admitted   │
│ 007   Fatima Khan      28   F    Asthma                 Dr. Bilal Ahmed Admitted   │ ← Added in CLI
```

**Statistics:**
- Admitted: 4 (Rajesh, Priya, Mohammad, Fatima)
- Discharged: 2 (Amit, Vikram)
- Total: 6

---

## Example 4: The patients.csv File

After all operations, `patients.csv` looks like:

```csv
id,name,age,gender,disease,doctor,status
1,Rajesh Kumar,46,M,Stage 2 Hypertension,Dr. Sharma,Admitted
2,Priya Sharma,32,F,Diabetes,Dr. Patel,Admitted
3,Amit Verma,58,M,Heart Disease,Dr. Gupta,Discharged
5,Vikram Singh,50,M,Asthma,Dr. Reddy,Discharged
6,Mohammad Ali,35,M,Fever,Dr. Ahmed Khan,Admitted
7,Fatima Khan,28,F,Asthma,Dr. Bilal Ahmed,Admitted
```

**Key observations:**
- ID sequence: 1, 2, 3, 5, 6, 7 (4 is missing = deleted)
- All edits saved (Rajesh's age and doctor)
- Status preserved (Discharged for Amit and Vikram)
- Both GUI and CLI operations recorded

---

## Summary: Data Flow

```
┌─────────────┐
│  GUI Mode   │  Add Mohammad Ali (ID 6)
│  python main.py
└────────┬────┘
         │
         ├→ Save to patients.csv
         │
         ↓
┌─────────────────┐
│ patients.csv    │  File updated with ID 6
└────────┬────────┘
         │
         ├→ Load from file
         │
         ↓
┌─────────────┐
│  CLI Mode   │  View: Mohammad Ali shows in list
│  python main.py --cli │  Add Fatima Khan (ID 7)
└────────┬────┘
         │
         ├→ Save to patients.csv
         │
         ↓
┌─────────────────┐
│ patients.csv    │  File updated with ID 7
└────────┬────────┘
         │
         ├→ Load from file
         │
         ↓
┌─────────────┐
│  GUI Mode   │  View: Both Mohammad (6) and Fatima (7) show
│  python main.py
└─────────────┘
```

---

## Key Takeaways

✅ **Dual interface** — Use GUI or CLI, both work with same data
✅ **Data persistence** — Changes in GUI visible in CLI and vice versa
✅ **Auto-increment IDs** — New patients always get unique IDs
✅ **Real-time updates** — Statistics and tables always current
✅ **Timestamps** — Admitted and discharged times tracked automatically
✅ **Professional UI** — Dark theme, search, filter, sorting
✅ **Modular code** — Easy to extend with new features

---

## Common Scenarios

### Scenario 1: Hospital Staff Uses GUI All Day
```bash
$ python main.py
→ GUI opens
→ Add/Edit/Discharge patients throughout the day
→ All changes auto-save
→ Close at end of day (data persisted)
→ Next day: $ python main.py → All data loaded
```

### Scenario 2: Need Quick CLI Access
```bash
$ python main.py --cli
→ Fast terminal access for viewing/adding patients
→ No GUI overhead
→ Same data as GUI
```

### Scenario 3: Backup & Migrate Data
```
1. CLI displays all patients: python main.py --cli → option 2
2. Copy patients.csv to another location
3. Export to Excel/PDF (can add feature)
4. Move to different machine/database
```

### Scenario 4: Large Data Import
```
1. Create patients.csv with 1000s of records (script-generated)
2. Run GUI: $ python main.py
3. All data loads automatically
4. GUI scales efficiently
```

---

## Next Time You Run The System

The data will **always be there**, persistent and correct, no matter which mode you use.

**Try it yourself!** Follow Example 1 → 2 → 3 and see the seamless data flow.
