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

    # Her yeni nesne üretildiğinde sayacı artırır
        AppointmentBase.increase_total_count()

    # --- Abstract (Soyut) Metotlar ---

    # Randevunun öncelik sırasını hesaplayan soyut metot
    @abstractmethod
    def calculate_priority(self):
        pass

    # Tahmini muayene süresini döndüren soyut metot
    @abstractmethod
    def get_estimated_duration(self):
        pass
 
    # Toplam oluşturulan randevu sayısını artıran sınıf metodu
    @classmethod
    def increase_total_count(cls):
        cls._total_appointments += 1

    # Toplam randevu sayısını döndüren sınıf metodu
    @classmethod
    def get_total_count(cls):
        return cls._total_appointments

    # Girilen tarih formatının doğruluğunu kontrol eden statik metot
    @staticmethod
    def validate_date_format(date_str):
        try:
            # Beklenen format: YYYY-MM-DD HH:MM
            datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False       

# --- Encapsulation (Getter & Setter Metotları) ---
 
    # Appointment ID için getter
    @property
    def appointment_id(self):
        return self._appointment_id

    # Patient ID için getter
    @property
    def patient_id(self):
        return self._patient_id

    # Doctor Name için getter
    @property
    def doctor_name(self):
        return self._doctor_name

    # Doctor Name için setter
    @doctor_name.setter
    def doctor_name(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._doctor_name = value
        else:
            raise ValueError("Doktor adı geçerli bir metin olmalıdır.")

    # Date Time için getter
    @property
    def date_time(self):
        return self._date_time

    # Date Time için setter
    @date_time.setter
    def date_time(self, value):
        if self.validate_date_format(value):
            self._date_time = value
        else:
            print(f"Uyarı: {value} geçersiz format. (Beklenen: YYYY-MM-DD HH:MM)")

    # Status için getter
    @property
    def status(self):
        return self._status

    # Status için setter
    @status.setter
    def status(self, value):
        valid_statuses = ["Pending", "Confirmed", "Cancelled", "Completed", "Urgent"]
        if value in valid_statuses:
            self._status = value
        else:
            print(f"Uyarı: '{value}' geçerli bir statü değil.")

    # Nesnenin string temsili (Debugging için)
    def __str__(self):
        return f"Randevu[{self._appointment_id}]: {self._doctor_name} - {self._date_time} ({self._status})"         