import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from src.models import Patient, Doctor, Anamnesis, ExamRequest, MedicalCertificate
from src.system import HospitalSystem

def print_menu():
    print("\n--- Hospital Management System ---")
    print("1. Add Patient")
    print("2. Add Doctor")
    print("3. Schedule Appointment")
    print("4. List Appointments")
    print("5. Add Anamnesis")
    print("6. Request Exam")
    print("7. Issue Medical Certificate")
    print("8. Exit")
    print("----------------------------------")

def main():
    system = HospitalSystem()
    
    while True:
        print_menu()
        choice = input("Choose an option: ")

        try:
            if choice == '1':
                p_id = input("ID: ")
                name = input("Name: ")
                age = int(input("Age: "))
                gender = input("Gender: ")
                has_insurance_str = input("Has Insurance? (y/n): ").lower()
                has_insurance = has_insurance_str == 'y'
                insurance_name = ""
                if has_insurance:
                    insurance_name = input("Insurance Name: ")
                
                system.add_patient(Patient(p_id, name, age, gender, has_insurance, insurance_name))
                print("Patient added successfully.")

            elif choice == '2':
                d_id = input("ID: ")
                name = input("Name: ")
                specialty = input("Specialty: ")
                system.add_doctor(Doctor(d_id, name, specialty))
                print("Doctor added successfully.")

            elif choice == '3':
                a_id = input("Appointment ID: ")
                p_id = input("Patient ID: ")
                d_id = input("Doctor ID: ")
                date_str = input("Date (YYYY-MM-DD): ")
                time_str = input("Time (HH:MM): ")
                desc = input("Description: ")
                
                app_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                app_time = datetime.strptime(time_str, "%H:%M").time()
                
                system.schedule_appointment(a_id, p_id, d_id, app_date, app_time, desc)
                print("Appointment scheduled successfully.")

            elif choice == '4':
                d_id = input("Doctor ID to filter (or leave empty for all): ")
                if d_id:
                    apps = system.get_appointments_by_doctor(d_id)
                else:
                    apps = system.appointments.values()
                
                for app in apps:
                    print(f"[{app.status.value}] {app.date} {app.time} - Doc: {app.doctor_id} Pat: {app.patient_id}")

            elif choice == '5':
                app_id = input("Appointment ID: ")
                symptoms = input("Symptoms: ")
                diagnosis = input("Diagnosis: ")
                system.add_anamnesis(Anamnesis(app_id, symptoms, diagnosis))
                print("Anamnesis added successfully.")

            elif choice == '6':
                req_id = input("Request ID: ")
                app_id = input("Appointment ID: ")
                exam_name = input("Exam Name: ")
                desc = input("Description: ")
                system.add_exam_request(ExamRequest(req_id, app_id, exam_name, desc))
                print("Exam requested successfully.")

            elif choice == '7':
                cert_id = input("Certificate ID: ")
                app_id = input("Appointment ID: ")
                days = int(input("Days: "))
                desc = input("Description: ")
                system.add_medical_certificate(MedicalCertificate(cert_id, app_id, days, desc))
                print("Medical Certificate issued successfully.")

            elif choice == '8':
                print("Exiting...")
                break
            
            else:
                print("Invalid option.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
