from datetime import datetime


class Patient:
    """Patient data model"""
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
        """Convert to dictionary for CSV storage"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "disease": self.disease,
            "doctor": self.doctor,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        """Create Patient from dictionary"""
        p = Patient(
            patient_id=data["id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            disease=data["disease"],
            doctor=data["doctor"],
            status=data.get("status", "Admitted")
        )
        return p


def create_patient(patient_id, name, age, gender, disease, doctor, status="Admitted"):
    """Create a patient object (legacy function for compatibility)"""
    return Patient(patient_id, name, age, gender, disease, doctor, status)


def find_patient_by_id(patients, patient_id):
    """Find a patient by ID"""
    for p in patients:
        pid = p.id if isinstance(p, Patient) else p["id"]
        if pid == patient_id:
            return p
    return None


def find_patients_by_keyword(patients, keyword):
    """Search patients by ID or name"""
    results = []
    
    for p in patients:
        pid = p.id if isinstance(p, Patient) else p["id"]
        pname = p.name if isinstance(p, Patient) else p["name"]
        
        if keyword.isdigit() and pid == int(keyword):
            results.append(p)
        elif keyword.lower() in pname.lower():
            results.append(p)
    
    return results


def display_patient(patient):
    """Display single patient details"""
    if isinstance(patient, Patient):
        print(f"\nID: {patient.id}")
        print(f"Name: {patient.name}")
        print(f"Age: {patient.age}")
        print(f"Gender: {patient.gender}")
        print(f"Disease: {patient.disease}")
        print(f"Doctor: {patient.doctor}")
        print(f"Status: {patient.status}")
    else:
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
        if isinstance(p, Patient):
            print("{:<5}{:<15}{:<5}{:<5}{:<15}{:<15}{:<10}".format(
                p.id, p.name, p.age, p.gender,
                p.disease, p.doctor, p.status))
        else:
            print("{:<5}{:<15}{:<5}{:<5}{:<15}{:<15}{:<10}".format(
                p["id"], p["name"], p["age"], p["gender"],
                p["disease"], p["doctor"], p["status"]))
    print()