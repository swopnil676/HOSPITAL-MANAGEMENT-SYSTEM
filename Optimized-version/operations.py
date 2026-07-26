from patient import (
    create_patient,
    find_patient_by_id,
    find_patients_by_keyword,
    display_patient,
    display_patients_table,
)
from file_handler import save_patients


def add_patient(patients, next_id):
    """Add a new patient"""
    name = input("Enter patient name: ").strip()
    age = input("Enter patient age: ").strip()
    gender = input("Enter gender (M/F/O): ").strip().upper()
    disease = input("Enter disease/diagnosis: ").strip()
    doctor = input("Enter assigned doctor: ").strip()

    patient = create_patient(next_id, name, age, gender, disease, doctor)
    patients.append(patient)
    save_patients(patients)
    
    print(f"Patient added successfully! ID: {patient['id']}\n")
    return next_id + 1


def view_patients(patients):
    """Display all patients"""
    if not patients:
        print("No patient records found.\n")
        return
    
    display_patients_table(patients)


def search_patient(patients):
    """Search for a patient"""
    if not patients:
        print("No patient records found.\n")
        return

    keyword = input("Enter Patient ID or Name to search: ").strip()
    results = find_patients_by_keyword(patients, keyword)

    if not results:
        print("No matching patient found.\n")
        return

    for p in results:
        display_patient(p)
    print()


def update_patient(patients):
    """Update patient information"""
    if not patients:
        print("No patient records found.\n")
        return

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


def discharge_patient(patients):
    """Discharge a patient"""
    if not patients:
        print("No patient records found.\n")
        return

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


def delete_patient(patients):
    """Delete a patient record"""
    if not patients:
        print("No patient records found.\n")
        return

    patient_id = input("Enter Patient ID to delete: ").strip()

    if not patient_id.isdigit():
        print("Invalid ID.\n")
        return

    patient = find_patient_by_id(patients, int(patient_id))

    if not patient:
        print("Patient not found.\n")
        return

    patients.remove(patient)
    save_patients(patients)
    
    print("Patient record deleted.\n")