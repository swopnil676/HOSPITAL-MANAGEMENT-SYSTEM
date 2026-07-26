import csv
import os
from patient import Patient

PATIENTS_FILE = "A:\CODING\ADVANCED PYTHON FOR MASTERY\Python Projects\PRO LEVEL SYSTEM\Hospital Management System\GUI-version\patients.csv"
FIELDNAMES = ["id", "name", "age", "gender", "disease", "doctor", "status"]


def load_patients():
    """Load patients from CSV file"""
    patients = []
    
    if not os.path.exists(PATIENTS_FILE):
        return patients, 1
    
    try:
        with open(PATIENTS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f, fieldnames=FIELDNAMES)
            next(reader, None)  # Skip header if it exists
            
            max_id = 0
            for row in reader:
                if row and row.get("id"):
                    try:
                        patient = Patient(
                            patient_id=int(row["id"]),
                            name=row["name"],
                            age=row["age"],
                            gender=row["gender"],
                            disease=row["disease"],
                            doctor=row["doctor"],
                            status=row["status"]
                        )
                        patients.append(patient)
                        max_id = max(max_id, int(row["id"]))
                    except (ValueError, KeyError):
                        continue
            
            next_id = max_id + 1
            return patients, next_id
    
    except Exception as e:
        print(f"Error loading patients: {e}\n")
        return patients, 1


def save_patients(patients):
    """Save patients to CSV file"""
    try:
        with open(PATIENTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            
            # Convert Patient objects to dicts for CSV
            rows = []
            for p in patients:
                if isinstance(p, Patient):
                    rows.append(p.to_dict())
                else:
                    rows.append(p)
            
            writer.writerows(rows)
    except Exception as e:
        print(f"Error saving patients: {e}\n")