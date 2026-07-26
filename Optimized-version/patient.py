def create_patient(patient_id, name, age, gender, disease, doctor, status="Admitted"):
    """Create a patient dictionary"""
    return {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "disease": disease,
        "doctor": doctor,
        "status": status,
    }


def find_patient_by_id(patients, patient_id):
    """Find a patient by ID"""
    for p in patients:
        if p["id"] == patient_id:
            return p
    return None


def find_patients_by_keyword(patients, keyword):
    """Search patients by ID or name"""
    results = []
    
    for p in patients:
        if keyword.isdigit() and p["id"] == int(keyword):
            results.append(p)
        elif keyword.lower() in p["name"].lower():
            results.append(p)
    
    return results


def display_patient(patient):
    """Display single patient details"""
    print(f"\nID: {patient['id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Gender: {patient['gender']}")
    print(f"Disease: {patient['disease']}")
    print(f"Doctor: {patient['doctor']}")
    print(f"Status: {patient['status']}")


def display_patients_table(patients):
    """Display all patients in table format"""
    print("\n{:<5}{:<15}{:<5}{:<5}{:<15}{:<15}{:<10}".format(
        "ID", "Name", "Age", "Sex", "Disease", "Doctor", "Status"))
    print("-" * 70)
    
    for p in patients:
        print("{:<5}{:<15}{:<5}{:<5}{:<15}{:<15}{:<10}".format(
            p["id"], p["name"], p["age"], p["gender"],
            p["disease"], p["doctor"], p["status"]))
    print()