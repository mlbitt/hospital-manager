import pytest
from datetime import date, time
from src.models import Patient, Doctor, Appointment, AppointmentStatus, Anamnesis, ExamRequest, MedicalCertificate

# Patient Tests
def test_patient_creation_success():
    p = Patient("1", "John", 30, "M")
    assert p.patient_id == "1"
    assert p.name == "John"
    assert p.age == 30
    assert p.has_insurance is False

def test_patient_creation_with_insurance_success():
    p = Patient("1", "John", 30, "M", True, "HealthPlus")
    assert p.has_insurance is True
    assert p.insurance_name == "HealthPlus"

def test_patient_creation_fail_insurance_without_name():
    with pytest.raises(ValueError, match="Insurance name cannot be empty"):
        Patient("1", "John", 30, "M", True, "")

def test_patient_creation_fail_empty_id():
    with pytest.raises(ValueError, match="Patient ID cannot be empty"):
        Patient("", "John", 30, "M")

def test_patient_creation_fail_empty_name():
    with pytest.raises(ValueError, match="Patient name cannot be empty"):
        Patient("1", "", 30, "M")

def test_patient_creation_fail_negative_age():
    with pytest.raises(ValueError, match="Age cannot be negative"):
        Patient("1", "John", -1, "M")

# Doctor Tests
def test_doctor_creation_success():
    d = Doctor("1", "Dr. Smith", "Cardiology")
    assert d.doctor_id == "1"
    assert d.name == "Dr. Smith"
    assert d.specialty == "Cardiology"

def test_doctor_creation_fail_empty_id():
    with pytest.raises(ValueError, match="Doctor ID cannot be empty"):
        Doctor("", "Dr. Smith", "Cardiology")

def test_doctor_creation_fail_empty_name():
    with pytest.raises(ValueError, match="Doctor name cannot be empty"):
        Doctor("1", "", "Cardiology")

def test_doctor_creation_fail_empty_specialty():
    with pytest.raises(ValueError, match="Specialty cannot be empty"):
        Doctor("1", "Dr. Smith", "")

# Appointment Tests
def test_appointment_creation_success():
    app = Appointment("1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    assert app.status == AppointmentStatus.SCHEDULED

def test_appointment_cancel_success():
    app = Appointment("1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    app.cancel()
    assert app.status == AppointmentStatus.CANCELLED

def test_appointment_cancel_fail_if_completed():
    app = Appointment("1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    app.complete()
    with pytest.raises(ValueError, match="Cannot cancel a completed appointment"):
        app.cancel()

def test_appointment_complete_success():
    app = Appointment("1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    app.complete()
    assert app.status == AppointmentStatus.COMPLETED

def test_appointment_complete_fail_if_cancelled():
    app = Appointment("1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    app.cancel()
    with pytest.raises(ValueError, match="Cannot complete a cancelled appointment"):
        app.complete()

# Anamnesis Tests
def test_anamnesis_creation_success():
    a = Anamnesis("a1", "Headache", "Migraine")
    assert a.appointment_id == "a1"
    assert a.symptoms == "Headache"

def test_anamnesis_creation_fail_empty_appointment_id():
    with pytest.raises(ValueError, match="Appointment ID cannot be empty"):
        Anamnesis("", "Headache", "Migraine")

def test_anamnesis_creation_fail_empty_symptoms():
    with pytest.raises(ValueError, match="Symptoms cannot be empty"):
        Anamnesis("a1", "", "Migraine")

# ExamRequest Tests
def test_exam_request_creation_success():
    e = ExamRequest("r1", "a1", "Blood Test")
    assert e.request_id == "r1"
    assert e.exam_name == "Blood Test"

def test_exam_request_creation_fail_empty_id():
    with pytest.raises(ValueError, match="Request ID cannot be empty"):
        ExamRequest("", "a1", "Blood Test")

def test_exam_request_creation_fail_empty_exam_name():
    with pytest.raises(ValueError, match="Exam name cannot be empty"):
        ExamRequest("r1", "a1", "")

def test_exam_request_creation_fail_empty_appointment_id():
    with pytest.raises(ValueError, match="Appointment ID cannot be empty"):
        ExamRequest("r1", "", "Blood Test")

# MedicalCertificate Tests
def test_medical_certificate_creation_success():
    c = MedicalCertificate("c1", "a1", 3)
    assert c.days == 3

def test_medical_certificate_creation_fail_negative_days():
    with pytest.raises(ValueError, match="Days must be positive"):
        MedicalCertificate("c1", "a1", -1)

def test_medical_certificate_creation_fail_empty_appointment_id():
    with pytest.raises(ValueError, match="Appointment ID cannot be empty"):
        MedicalCertificate("c1", "", 3)

def test_medical_certificate_creation_fail_empty_id():
    with pytest.raises(ValueError, match="Certificate ID cannot be empty"):
        MedicalCertificate("", "a1", 3)
