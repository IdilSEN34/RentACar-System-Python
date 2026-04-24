from datetime import datetime


def gun_sayisi_hesapla(baslangic, bitis):
    try:
        b1 = datetime.strptime(baslangic, "%d/%m/%Y")
        b2 = datetime.strptime(bitis, "%d/%m/%Y")
    except ValueError: # Yanlış format veya geçersiz tarih (örn: 31 Şubat) durumu
        raise ValueError("Tarih formatı hatalı veya geçersiz tarih girildi. Lütfen GG/AA/YYYY formatını kullanın.")

    if b2 < b1:
        raise ValueError("Bitiş tarihi başlangıçtan önce olamaz")

    return (b2 - b1).days + 1