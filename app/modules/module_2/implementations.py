from .base import AppointmentBase
import random
from datetime import datetime, timedelta

class RoutineAppointment(AppointmentBase):
    """
    Rutin kontroller için kullanılan alt sınıf.
    Genellikle standart muayeneler ve periyodik kontrolleri kapsar.
    """
    def __init__(self, appointment_id, patient_id, doctor_name, date_time, checkup_type="General"):
        # Base sınıfın başlatıcısını çağırıyoruz
        super().__init__(appointment_id, patient_id, doctor_name, date_time)
        self._checkup_type = checkup_type # Örn: Dahiliye, Göz, KBB
        self._notes = "" # Rutin notlar için boş alan

    # --- Abstract Metotların Override Edilmesi (Zorunlu) ---
    
    def calculate_priority(self):
        """
        Rutin randevuların önceliğini hesaplar.
        Rutin işlemler düşük önceliklidir (Seviye: 1).
        """
        return 1

    def get_estimated_duration(self):
        """
        Tahmini muayene süresini döndürür.
        Rutin muayeneler standart olarak 15 dakika sürer.
        """
        return 15

    # --- Sınıfa Özel Metotlar ve Kapsülleme ---

    @property
    def checkup_type(self):
        return self._checkup_type

    @checkup_type.setter
    def checkup_type(self, value):
        if value:
            self._checkup_type = value
        else:
            print("Hata: Muayene türü boş olamaz.")

    def add_note(self, note):
        """Doktorun muayene ile ilgili not eklemesini sağlar."""
        self._notes += f"{note}; "


class EmergencyAppointment(AppointmentBase):
    """
    Acil durumlar için kullanılan alt sınıf.
    Yüksek öncelik seviyesine sahiptir.
    """
    def __init__(self, appointment_id, patient_id, doctor_name, date_time, severity_level):
        # Acil durumlar otomatik olarak "Urgent" statüsünde başlar
        super().__init__(appointment_id, patient_id, doctor_name, date_time, status="Urgent")
        self._severity_level = severity_level # 1 ile 10 arası şiddet
        self._triage_code = self._assign_triage_code()

    def _assign_triage_code(self):
        """Aciliyet seviyesine göre triyaj (renk) kodu atar."""
        if self._severity_level >= 8:
            return "RED" # Çok acil
        elif self._severity_level >= 5:
            return "YELLOW" # Orta acil
        else:
            return "GREEN" # Az acil

    # --- Abstract Metotların Override Edilmesi ---

    def calculate_priority(self):
        """
        Acil randevular şiddet seviyesine (severity_level) göre öncelik alır.
        En az 5, en çok 10 döner.
        """
        # Base priority 5, üzerine severity eklenir (max 10 olacak şekilde)
        priority = 5 + (self._severity_level / 2)
        return min(int(priority), 10)

    def get_estimated_duration(self):
        """Acil durumlar belirsizdir ancak ortalama 45 dk ayrılır."""
        return 45

    # --- Getter / Setter ---
    
    @property
    def severity_level(self):
        return self._severity_level