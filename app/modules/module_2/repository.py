from datetime import datetime

class AppointmentRepository:
    """
    Randevu verilerinin yönetildiği Repository sınıfı.
    Bu sınıf, verileri geçici hafızada (RAM) bir liste içinde tutarak 
    sanki bir veri tabanıymış gibi davranır.
    
    Yöntem: In-Memory Database (Liste Tabanlı)
    """

    def __init__(self):
        """
        Repository başlatıldığında boş bir veri listesi oluşturulur.
        """
        # Veri tabanı simülasyonu için boş liste
        self._storage = []
        
        # Loglama amaçlı (debug için)
        print("AppointmentRepository başlatıldı: Veri tabanı hazır.")

    def save(self, appointment):
        """
        Bir randevu nesnesini 'veri tabanına' (listeye) kaydeder veya günceller.
        
        Args:
            appointment (AppointmentBase): Kaydedilecek randevu nesnesi.
        """
        # Eğer aynı ID'ye sahip bir kayıt varsa, onu güncelle (önce sil, sonra ekle)
        existing_appt = self.find_by_id(appointment.appointment_id)
        if existing_appt:
            self._storage.remove(existing_appt)
            print(f"LOG: Randevu ID {appointment.appointment_id} güncellendi.")
        
        # Yeni kaydı ekle
        self._storage.append(appointment)
        print(f"LOG: Randevu ID {appointment.appointment_id} sisteme kaydedildi.")

    def find_by_id(self, appointment_id):
        """
        ID numarasına göre randevu arar.
        
        Args:
            appointment_id (int): Aranacak randevunun ID'si.
            
        Returns:
            AppointmentBase nesnesi veya None.
        """
        for app in self._storage:
            if app.appointment_id == appointment_id:
                return app
        return None

    def delete(self, appointment_id):
        """
        ID numarasına göre randevuyu sistemden siler.
        
        Args:
            appointment_id (int): Silinecek randevunun ID'si.
        """
        appointment = self.find_by_id(appointment_id)
        if appointment:
            self._storage.remove(appointment)
            print(f"LOG: Randevu ID {appointment_id} silindi.")
            return True
        else:
            print(f"Hata: Silinecek randevu ID {appointment_id} bulunamadı.")
            return False

    def list_all(self):
        """
        Sistemdeki tüm randevuları listeler.
        
        Returns:
            list: Tüm randevu nesnelerinin listesi.
        """
        return self._storage

    def list_by_doctor(self, doctor_name):
        """
        Belirli bir doktora ait tüm randevuları filtreler.
        
        Args:
            doctor_name (str): Doktorun adı.
            
        Returns:
            list: O doktora ait randevuların listesi.
        """
        result = []
        for app in self._storage:
            # Büyük/küçük harf duyarlılığını kaldırmak için lower() kullanıldı
            if app.doctor_name.lower() == doctor_name.lower():
                result.append(app)
        return result

    def filter_by_date(self, target_date):
        """
        Belirli bir tarihteki randevuları getirir.
        
        Args:
            target_date (str): Aranacak tarih (Format: YYYY-MM-DD).
            
        Returns:
            list: O güne ait randevular.
        """
        filtered_list = []
        for app in self._storage:
            # app.date_time formatı "YYYY-MM-DD HH:MM" olduğu için
            # startswith ile sadece gün kısmını kontrol ediyoruz.
            if str(app.date_time).startswith(target_date):
                filtered_list.append(app)
        
        return filtered_list

    def filter_by_status(self, status):
        """
        Durumuna göre (Örn: 'Pending', 'Urgent') randevuları filtreler.
        """
        return [app for app in self._storage if app.status == status]

    def count(self):
        """
        Sistemdeki toplam kayıtlı randevu sayısını döner.
        """
        return len(self._storage)