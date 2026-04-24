from backend.kontrol import bos_deger_kontrolu


class Arac:
    def __init__(self, plaka, marka, model, gunluk_ucret,
                 durum="müsait", kiralayan=None,
                 baslangic_tarihi=None, bitis_tarihi=None):

        if bos_deger_kontrolu(plaka) or bos_deger_kontrolu(marka) or bos_deger_kontrolu(model):
            raise ValueError("Tüm alanlar doldurulmalıdır.")

        try:
            gunluk_ucret = float(gunluk_ucret)
        except ValueError: # Sadece dönüştürme hatasını yakalar
            raise ValueError("Günlük ücret sayısal bir değer olmalıdır (Örn: 1500.50).")

        if gunluk_ucret <= 0:
            raise ValueError("Günlük ücret sıfırdan büyük olmalıdır.")

        if durum not in ["müsait", "kirada", "bakımda"]:
            raise ValueError("Geçersiz araç durumu.")

        self.plaka = plaka
        self.marka = marka
        self.model = model
        self.gunluk_ucret = gunluk_ucret
        self.durum = durum
        self.kiralayan = kiralayan
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi

    def sozluk(self):
        return {
            "plaka": self.plaka,
            "marka": self.marka,
            "model": self.model,
            "gunluk_ucret": self.gunluk_ucret,
            "durum": self.durum,
            "kiralayan": self.kiralayan,
            "baslangic_tarihi": self.baslangic_tarihi,
            "bitis_tarihi": self.bitis_tarihi
        }