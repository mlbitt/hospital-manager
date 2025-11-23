from typing import List, Optional
from datetime import date, time
from src.models import Patient, Doctor, Appointment, AppointmentStatus, Anamnesis, ExamRequest, MedicalCertificate

class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}
        self.anamneses = {}
        self.exam_requests = {}
        self.medical_certificates = {}

    def add_patient(self, patient: Patient):
        if patient.patient_id in self.patients:
            raise ValueError(f"Patient with ID {patient.patient_id} already exists")
        self.patients[patient.patient_id] = patient

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        return self.patients.get(patient_id)

    def remove_patient(self, patient_id: str):
        if patient_id not in self.patients:
            raise ValueError(f"Patient with ID {patient_id} not found")
        # Check for active appointments
        for app in self.appointments.values():
            if app.patient_id == patient_id and app.status == AppointmentStatus.SCHEDULED:
                raise ValueError("Cannot remove patient with active appointments")
        del self.patients[patient_id]

    def add_doctor(self, doctor: Doctor):
        if doctor.doctor_id in self.doctors:
            raise ValueError(f"Doctor with ID {doctor.doctor_id} already exists")
        self.doctors[doctor.doctor_id] = doctor

    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        return self.doctors.get(doctor_id)

    def remove_doctor(self, doctor_id: str):
        if doctor_id not in self.doctors:
            raise ValueError(f"Doctor with ID {doctor_id} not found")
        # Check for active appointments
        for app in self.appointments.values():
            if app.doctor_id == doctor_id and app.status == AppointmentStatus.SCHEDULED:
                raise ValueError("Cannot remove doctor with active appointments")
        del self.doctors[doctor_id]

    def schedule_appointment(self, appointment_id: str, patient_id: str, doctor_id: str, app_date: date, app_time: time, description: str = "") -> Appointment:
        if appointment_id in self.appointments:
            raise ValueError(f"Appointment with ID {appointment_id} already exists")
        if patient_id not in self.patients:
            raise ValueError(f"Patient with ID {patient_id} not found")
        if doctor_id not in self.doctors:
            raise ValueError(f"Doctor with ID {doctor_id} not found")
        
        # Check doctor availability
        for app in self.appointments.values():
            if (app.doctor_id == doctor_id and 
                app.date == app_date and 
                app.time == app_time and 
                app.status == AppointmentStatus.SCHEDULED):
                raise ValueError("Doctor is not available at this time")

        appointment = Appointment(appointment_id, patient_id, doctor_id, app_date, app_time, AppointmentStatus.SCHEDULED, description)
        self.appointments[appointment_id] = appointment
        return appointment

    def cancel_appointment(self, appointment_id: str):
        if appointment_id not in self.appointments:
            raise ValueError(f"Appointment with ID {appointment_id} not found")
        self.appointments[appointment_id].cancel()

    def complete_appointment(self, appointment_id: str):
        if appointment_id not in self.appointments:
            raise ValueError(f"Appointment with ID {appointment_id} not found")
        self.appointments[appointment_id].complete()

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        return self.appointments.get(appointment_id)

    def get_appointments_by_patient(self, patient_id: str) -> List[Appointment]:
        if patient_id not in self.patients:
            raise ValueError(f"Patient with ID {patient_id} not found")
        return [app for app in self.appointments.values() if app.patient_id == patient_id]

    def get_appointments_by_doctor(self, doctor_id: str) -> List[Appointment]:
        if doctor_id not in self.doctors:
            raise ValueError(f"Doctor with ID {doctor_id} not found")
        return [app for app in self.appointments.values() if app.doctor_id == doctor_id]

    def add_anamnesis(self, anamnesis: Anamnesis):
        if anamnesis.appointment_id not in self.appointments:
             raise ValueError(f"Appointment with ID {anamnesis.appointment_id} not found")
        
        if anamnesis.appointment_id in self.anamneses:
             raise ValueError(f"Anamnesis for appointment {anamnesis.appointment_id} already exists")
        
        self.anamneses[anamnesis.appointment_id] = anamnesis

    def get_anamnesis(self, appointment_id: str) -> Optional[Anamnesis]:
        return self.anamneses.get(appointment_id)

    def add_exam_request(self, request: ExamRequest):
        if request.request_id in self.exam_requests:
             raise ValueError(f"Exam request with ID {request.request_id} already exists")
        if request.appointment_id not in self.appointments:
             raise ValueError(f"Appointment with ID {request.appointment_id} not found")
        
        self.exam_requests[request.request_id] = request

    def get_exam_requests_by_appointment(self, appointment_id: str) -> List[ExamRequest]:
        return [req for req in self.exam_requests.values() if req.appointment_id == appointment_id]

    def add_medical_certificate(self, certificate: MedicalCertificate):
        if certificate.certificate_id in self.medical_certificates:
             raise ValueError(f"Certificate with ID {certificate.certificate_id} already exists")
        if certificate.appointment_id not in self.appointments:
             raise ValueError(f"Appointment with ID {certificate.appointment_id} not found")
        
        self.medical_certificates[certificate.certificate_id] = certificate

    def get_medical_certificates_by_appointment(self, appointment_id: str) -> List[MedicalCertificate]:
        return [cert for cert in self.medical_certificates.values() if cert.appointment_id == appointment_id]
