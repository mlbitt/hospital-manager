import pytest
from datetime import date, time
from src.models import Patient, Doctor, AppointmentStatus, Anamnesis, ExamRequest, MedicalCertificate
from src.system import HospitalSystem

def test_integration_full_flow():
    system = HospitalSystem()
    
    # 1. Register Patient with Insurance
    p = Patient("p1", "John Doe", 30, "M", True, "HealthCare Inc.")
    system.add_patient(p)
    
    # 2. Register Doctor
    d = Doctor("d1", "Dr. House", "Diagnostic")
    system.add_doctor(d)
    
    # 3. Schedule Appointment
    app_date = date(2023, 10, 1)
    app_time = time(14, 30)
    system.schedule_appointment("a1", "p1", "d1", app_date, app_time, "Checkup")
    
    # 4. Verify Appointment
    app = system.get_appointment("a1")
    assert app is not None
    assert app.patient_id == "p1"
    assert app.doctor_id == "d1"
    assert app.status == AppointmentStatus.SCHEDULED

    # 5. Add Anamnesis
    system.add_anamnesis(Anamnesis("a1", "Cough and Fever", "Flu"))
    assert system.get_anamnesis("a1").diagnosis == "Flu"

    # 6. Request Exam
    system.add_exam_request(ExamRequest("r1", "a1", "Blood Test"))
    reqs = system.get_exam_requests_by_appointment("a1")
    assert len(reqs) == 1
    assert reqs[0].exam_name == "Blood Test"

    # 7. Issue Certificate
    system.add_medical_certificate(MedicalCertificate("c1", "a1", 3))
    certs = system.get_medical_certificates_by_appointment("a1")
    assert len(certs) == 1
    assert certs[0].days == 3

    # 8. Complete Appointment
    system.complete_appointment("a1")
    assert system.get_appointment("a1").status == AppointmentStatus.COMPLETED

def test_integration_cancellation_flow():
    system = HospitalSystem()
    system.add_patient(Patient("p1", "John", 30, "M"))
    system.add_doctor(Doctor("d1", "Dr. House", "Diagnostic"))
    
    system.schedule_appointment("a1", "p1", "d1", date(2025, 10, 1), time(10, 0))
    
    system.cancel_appointment("a1")
    
    app = system.get_appointment("a1")
    assert app.status == AppointmentStatus.CANCELLED

def test_integration_doctor_availability_flow():
    system = HospitalSystem()
    system.add_patient(Patient("p1", "John", 30, "M"))
    system.add_patient(Patient("p2", "Jane", 25, "F"))
    system.add_doctor(Doctor("d1", "Dr. House", "Diagnostic"))
    
    # Schedule first
    system.schedule_appointment("a1", "p1", "d1", date(2025, 10, 1), time(10, 0))
    
    # Try schedule second at same time (should fail)
    with pytest.raises(ValueError, match="Doctor is not available"):
        system.schedule_appointment("a2", "p2", "d1", date(2025, 10, 1), time(10, 0))
        
    # Schedule third at different time (should success)
    system.schedule_appointment("a3", "p2", "d1", date(2025, 10, 1), time(11, 0))
    
    assert system.get_appointment("a1") is not None
    assert system.get_appointment("a2") is None
    assert system.get_appointment("a3") is not None

def test_integration_patient_history_flow():
    system = HospitalSystem()
    system.add_patient(Patient("p1", "John", 30, "M"))
    system.add_doctor(Doctor("d1", "Dr. House", "Diagnostic"))
    
    system.schedule_appointment("a1", "p1", "d1", date(2025, 10, 1), time(10, 0))
    system.schedule_appointment("a2", "p1", "d1", date(2025, 10, 2), time(10, 0))
    
    apps = system.get_appointments_by_patient("p1")
    assert len(apps) == 2
    ids = [a.appointment_id for a in apps]
    assert "a1" in ids
    assert "a2" in ids

def test_integration_doctor_schedule_flow():
    system = HospitalSystem()
    system.add_patient(Patient("p1", "John", 30, "M"))
    system.add_patient(Patient("p2", "Jane", 25, "F"))
    system.add_doctor(Doctor("d1", "Dr. House", "Diagnostic"))
    
    system.schedule_appointment("a1", "p1", "d1", date(2025, 10, 1), time(10, 0))
    system.schedule_appointment("a2", "p2", "d1", date(2025, 10, 1), time(11, 0))
    
    apps = system.get_appointments_by_doctor("d1")
    assert len(apps) == 2
    ids = [a.appointment_id for a in apps]
    assert "a1" in ids
    assert "a2" in ids
