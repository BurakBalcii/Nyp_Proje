from abc import ABC, abstractmethod
from datetime import datetime

# Randevu işlemleri için temel soyut sınıf yapısı
class AppointmentBase(ABC):
    # Toplam randevu sayısını tutan sınıf değişkeni
    _total_appointments = 0

    def __init__(self, appointment_id, patient_id, doctor_name, date_time, status="Pending"):
        """
        AppointmentBase sınıfının yapıcı metodu.
        Tüm özellikleri kapsüllenmiş (private/protected) olarak başlatır.
        """
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._doctor_name = doctor_name
        self._date_time = date_time
        self._status = status