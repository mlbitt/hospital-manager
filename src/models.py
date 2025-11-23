from dataclasses import dataclass
from enum import Enum
from datetime import date, time

class AppointmentStatus(Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    has_insurance: bool = False
    insurance_name: str = ""

    def __post_init__(self):
        if not self.patient_id:
            raise ValueError("Patient ID cannot be empty")
        if not self.name:
            raise ValueError("Patient name cannot be empty")
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if self.has_insurance and not self.insurance_name:
            raise ValueError("Insurance name cannot be empty if patient has insurance")

@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialty: str

    def __post_init__(self):
        if not self.doctor_id:
            raise ValueError("Doctor ID cannot be empty")
        if not self.name:
            raise ValueError("Doctor name cannot be empty")
        if not self.specialty:
            raise ValueError("Specialty cannot be empty")

@dataclass
class Anamnesis:
    appointment_id: str
    symptoms: str
    diagnosis: str
    
    def __post_init__(self):
        if not self.appointment_id:
             raise ValueError("Appointment ID cannot be empty")
        if not self.symptoms:
             raise ValueError("Symptoms cannot be empty")

@dataclass
class ExamRequest:
    request_id: str
    appointment_id: str
    exam_name: str
    description: str = ""
    
    def __post_init__(self):
        if not self.request_id:
             raise ValueError("Request ID cannot be empty")
        if not self.appointment_id:
             raise ValueError("Appointment ID cannot be empty")
        if not self.exam_name:
             raise ValueError("Exam name cannot be empty")

@dataclass
class MedicalCertificate:
    certificate_id: str
    appointment_id: str
    days: int
    description: str = ""

    def __post_init__(self):
        if not self.certificate_id:
             raise ValueError("Certificate ID cannot be empty")
        if not self.appointment_id:
             raise ValueError("Appointment ID cannot be empty")
        if self.days <= 0:
             raise ValueError("Days must be positive")

@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    date: date
    time: time
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    description: str = ""

    def cancel(self):
        if self.status == AppointmentStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed appointment")
        self.status = AppointmentStatus.CANCELLED

    def complete(self):
        if self.status == AppointmentStatus.CANCELLED:
            raise ValueError("Cannot complete a cancelled appointment")
        self.status = AppointmentStatus.COMPLETED
