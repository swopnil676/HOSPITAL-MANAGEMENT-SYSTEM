import sys
from file_handler import load_patients
from operations import (
    add_patient,
    view_patients,
    search_patient,
    update_patient,
    discharge_patient,
    delete_patient,
)


def menu(patients, next_id):
    """Display menu and handle user choices (CLI mode)"""
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
            next_id = add_patient(patients, next_id)
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


def main_cli():
    """Initialize and run CLI application"""
    patients, next_id = load_patients()
    menu(patients, next_id)


def main_gui():
    """Initialize and run GUI application"""
    import tkinter as tk
    from gui import HospitalGUI
    
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()


if __name__ == "__main__":
    # Check if user wants CLI or GUI
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI mode
        main_cli()
    else:
        # Run GUI mode (default)
        main_gui()