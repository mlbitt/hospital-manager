import pytest
from datetime import date, time
from src.models import Patient, Doctor, AppointmentStatus, Anamnesis, ExamRequest, MedicalCertificate
from src.system import HospitalSystem

@pytest.fixture
def system():
    return HospitalSystem()

@pytest.fixture
def sample_patient():
    return Patient("p1", "John", 30, "M")

@pytest.fixture
def sample_doctor():
    return Doctor("d1", "Dr. Smith", "Cardiology")

def test_add_patient_success(system, sample_patient):
    system.add_patient(sample_patient)
    assert system.get_patient("p1") == sample_patient

def test_add_patient_duplicate_fail(system, sample_patient):
    system.add_patient(sample_patient)
    with pytest.raises(ValueError, match="already exists"):
        system.add_patient(sample_patient)

def test_get_patient_success(system, sample_patient):
    system.add_patient(sample_patient)
    assert system.get_patient("p1") is not None

def test_get_patient_not_found(system):
    assert system.get_patient("nonexistent") is None

def test_remove_patient_success(system, sample_patient):
    system.add_patient(sample_patient)
    system.remove_patient("p1")
    assert system.get_patient("p1") is None

def test_remove_patient_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.remove_patient("nonexistent")

def test_remove_patient_fail_active_appointment(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    with pytest.raises(ValueError, match="Cannot remove patient with active appointments"):
        system.remove_patient("p1")

def test_add_doctor_success(system, sample_doctor):
    system.add_doctor(sample_doctor)
    assert system.get_doctor("d1") == sample_doctor

def test_add_doctor_duplicate_fail(system, sample_doctor):
    system.add_doctor(sample_doctor)
    with pytest.raises(ValueError, match="already exists"):
        system.add_doctor(sample_doctor)

def test_get_doctor_success(system, sample_doctor):
    system.add_doctor(sample_doctor)
    assert system.get_doctor("d1") is not None

def test_get_doctor_not_found(system):
    assert system.get_doctor("nonexistent") is None

def test_remove_doctor_success(system, sample_doctor):
    system.add_doctor(sample_doctor)
    system.remove_doctor("d1")
    assert system.get_doctor("d1") is None

def test_remove_doctor_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.remove_doctor("nonexistent")

def test_remove_doctor_fail_active_appointment(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    with pytest.raises(ValueError, match="Cannot remove doctor with active appointments"):
        system.remove_doctor("d1")

def test_schedule_appointment_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    app = system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    assert app.status == AppointmentStatus.SCHEDULED

def test_schedule_appointment_duplicate_id_fail(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    with pytest.raises(ValueError, match="already exists"):
        system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 2), time(11, 0))

def test_schedule_appointment_patient_not_found(system, sample_doctor):
    system.add_doctor(sample_doctor)
    with pytest.raises(ValueError, match="Patient with ID p1 not found"):
        system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))

def test_schedule_appointment_doctor_not_found(system, sample_patient):
    system.add_patient(sample_patient)
    with pytest.raises(ValueError, match="Doctor with ID d1 not found"):
        system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))

def test_schedule_appointment_doctor_busy(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    
    # Add another patient to try to book same slot
    p2 = Patient("p2", "Jane", 25, "F")
    system.add_patient(p2)
    
    with pytest.raises(ValueError, match="Doctor is not available at this time"):
        system.schedule_appointment("a2", "p2", "d1", date(2025, 1, 1), time(10, 0))

def test_cancel_appointment_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    system.cancel_appointment("a1")
    assert system.get_appointment("a1").status == AppointmentStatus.CANCELLED

def test_cancel_appointment_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.cancel_appointment("nonexistent")

def test_complete_appointment_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    system.complete_appointment("a1")
    assert system.get_appointment("a1").status == AppointmentStatus.COMPLETED

def test_complete_appointment_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.complete_appointment("nonexistent")

def test_get_appointments_by_patient_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    apps = system.get_appointments_by_patient("p1")
    assert len(apps) == 1
    assert apps[0].appointment_id == "a1"

def test_get_appointments_by_patient_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.get_appointments_by_patient("nonexistent")

def test_get_appointments_by_doctor_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2025, 1, 1), time(10, 0))
    apps = system.get_appointments_by_doctor("d1")
    assert len(apps) == 1
    assert apps[0].appointment_id == "a1"

def test_get_appointments_by_doctor_not_found(system):
    with pytest.raises(ValueError, match="not found"):
        system.get_appointments_by_doctor("nonexistent")

def test_add_anamnesis_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    anamnesis = Anamnesis("a1", "Fever", "Flu")
    system.add_anamnesis(anamnesis)
    assert system.get_anamnesis("a1") == anamnesis

def test_add_anamnesis_appointment_not_found(system):
    anamnesis = Anamnesis("nonexistent", "Fever", "Flu")
    with pytest.raises(ValueError, match="Appointment with ID nonexistent not found"):
        system.add_anamnesis(anamnesis)

def test_add_anamnesis_duplicate(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    system.add_anamnesis(Anamnesis("a1", "Fever", "Flu"))
    with pytest.raises(ValueError, match="already exists"):
        system.add_anamnesis(Anamnesis("a1", "Fever", "Flu"))

def test_add_exam_request_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    req = ExamRequest("r1", "a1", "X-Ray")
    system.add_exam_request(req)
    reqs = system.get_exam_requests_by_appointment("a1")
    assert len(reqs) == 1
    assert reqs[0] == req

def test_add_exam_request_appointment_not_found(system):
    req = ExamRequest("r1", "nonexistent", "X-Ray")
    with pytest.raises(ValueError, match="Appointment with ID nonexistent not found"):
        system.add_exam_request(req)

def test_add_exam_request_duplicate(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    req = ExamRequest("r1", "a1", "X-Ray")
    system.add_exam_request(req)
    with pytest.raises(ValueError, match="already exists"):
        system.add_exam_request(req)

def test_add_medical_certificate_success(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    cert = MedicalCertificate("c1", "a1", 2)
    system.add_medical_certificate(cert)
    certs = system.get_medical_certificates_by_appointment("a1")
    assert len(certs) == 1
    assert certs[0] == cert

def test_add_medical_certificate_appointment_not_found(system):
    cert = MedicalCertificate("c1", "nonexistent", 2)
    with pytest.raises(ValueError, match="Appointment with ID nonexistent not found"):
        system.add_medical_certificate(cert)

def test_add_medical_certificate_duplicate(system, sample_patient, sample_doctor):
    system.add_patient(sample_patient)
    system.add_doctor(sample_doctor)
    system.schedule_appointment("a1", "p1", "d1", date(2023, 1, 1), time(10, 0))
    
    cert = MedicalCertificate("c1", "a1", 2)
    system.add_medical_certificate(cert)
    with pytest.raises(ValueError, match="already exists"):
        system.add_medical_certificate(cert)
