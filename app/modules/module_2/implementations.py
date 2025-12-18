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
    
class OnlineAppointment(AppointmentBase):
    """
    Uzaktan görüntülü görüşme (Tele-Tıp) için kullanılan alt sınıf.
    """
    def __init__(self, appointment_id, patient_id, doctor_name, date_time, platform="Zoom"):
        super().__init__(appointment_id, patient_id, doctor_name, date_time)
        self._platform = platform
        self._meeting_link = self._generate_meeting_link()
        self._is_connection_tested = False

    def _generate_meeting_link(self):
        """Rastgele bir toplantı linki simüle eder."""
        code = random.randint(100000, 999999)
        return f"https://{self._platform.lower()}.com/meet/{code}"

    # --- Abstract Metotların Override Edilmesi ---

    def calculate_priority(self):
        """Online görüşmeler orta önceliklidir (Seviye: 3)."""
        return 3

    def get_estimated_duration(self):
        """Online görüşmeler genelde 20 dakika ile sınırlıdır."""
        return 20

    # --- Özel Metotlar ---

    def test_connection(self):
        """Bağlantı testi simülasyonu."""
        print(f"Bağlantı testi yapılıyor ({self._platform})...")
        self._is_connection_tested = True
        return True
    
    @property
    def meeting_link(self):
        return self._meeting_link


class AppointmentService:
    """
    Randevu süreçlerini yöneten servis sınıfı.
    Repository ile konuşarak kayıt işlemlerini yapar.
    """
    def __init__(self, repository):
        # Dependency Injection: Veri tabanı (repo) dışarıdan verilir
        self.repository = repository

    def create_appointment(self, app_type, **kwargs):
        """
        Yeni bir randevu nesnesi oluşturur ve repository'e kaydeder.
        
        """
        try:
            # Tarih kontrolü (Base class'taki statik metodu kullanıyoruz)
            date_str = kwargs.get('date_time')
            if date_str and not AppointmentBase.validate_date_format(date_str):
                raise ValueError("Tarih formatı hatalı!")

            appointment = None

            # Factory Pattern benzeri yapı
            if app_type == "Routine":
                appointment = RoutineAppointment(**kwargs)
            elif app_type == "Emergency":
                appointment = EmergencyAppointment(**kwargs)
            elif app_type == "Online":
                appointment = OnlineAppointment(**kwargs)
            else:
                print(f"Hata: Bilinmeyen randevu tipi '{app_type}'")
                return None

            # Oluşturulan nesneyi kaydet
            self.repository.save(appointment)
            print(f"Başarılı: Randevu ({appointment.appointment_id}) oluşturuldu.")
            return appointment

        except Exception as e:
            print(f"Randevu oluşturulurken hata: {e}")
            return None

    def cancel_appointment(self, appointment_id):
        """
        Belirtilen ID'li randevuyu iptal eder (Status -> Cancelled).
        """
        app = self.repository.find_by_id(appointment_id)
        if app:
            app.status = "Cancelled"
            print(f"Randevu {appointment_id} iptal edildi.")
        else:
            print("Hata: İptal edilecek randevu bulunamadı.")

    def postpone_appointment(self, appointment_id, days=1):
        """
        Randevuyu belirtilen gün kadar erteler.
        """
        app = self.repository.find_by_id(appointment_id)
        if app:
            try:
                # String tarihi datetime objesine çevir
                current_dt = datetime.strptime(app.date_time, "%Y-%m-%d %H:%M")
                # Gün ekle
                new_dt = current_dt + timedelta(days=days)
                # Tekrar stringe çevirip kaydet
                app.date_time = new_dt.strftime("%Y-%m-%d %H:%M")
                app.status = "Postponed" # Durumu ertelemeye çek
                print(f"Randevu {appointment_id}, {days} gün ertelendi. Yeni tarih: {app.date_time}")
            except ValueError:
                print("Tarih formatı hatası nedeniyle ertelenemedi.")
        else:
            print("Hata: Ertelenecek randevu bulunamadı.")

    def get_appointments_by_doctor(self, doctor_name):
        """Belirli bir doktora ait randevuları listeler."""
        return self.repository.list_by_doctor(doctor_name)    