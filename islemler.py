from backend.arac import Arac
from backend.kontrol import bos_deger_kontrolu, tarih_format_kontrolu
from backend.hesaplama import gun_sayisi_hesapla


def arac_ekle(araclar, plaka, marka, model, gunluk_ucret):
    for arac in araclar:
        if arac["plaka"] == plaka:
            raise ValueError("Bu plakaya ait araç zaten kayıtlı.")

    yeni_arac = Arac(plaka, marka, model, gunluk_ucret)
    araclar.append(yeni_arac.sozluk())


def arac_sil(araclar, plaka):
    for arac in araclar:
        if arac["plaka"] == plaka:
            if arac["durum"] == "kirada":
                raise ValueError("Kirada olan araç silinemez.")
            araclar.remove(arac)
            return
    raise ValueError("Araç bulunamadı.")


def arac_duzenle(araclar, plaka, yeni_model=None, yeni_gunluk_ucret=None, yeni_durum=None):
    for arac in araclar:
        if arac["plaka"] == plaka:

            if yeni_model is not None:
                if bos_deger_kontrolu(yeni_model):
                    raise ValueError("Model boş olamaz.")
                arac["model"] = yeni_model

            if yeni_gunluk_ucret is not None:
                try:
                    yeni_gunluk_ucret = float(yeni_gunluk_ucret)
                except:
                    raise ValueError("Günlük ücret sayısal olmalıdır.")
                if yeni_gunluk_ucret <= 0:
                    raise ValueError("Günlük ücret sıfırdan büyük olmalıdır.")
                arac["gunluk_ucret"] = yeni_gunluk_ucret

            if yeni_durum is not None:
                if yeni_durum not in ["müsait", "kirada", "bakımda"]:
                    raise ValueError("Geçersiz durum.")
                arac["durum"] = yeni_durum
                if yeni_durum != "kirada":
                    arac["kiralayan"] = None
                    arac["baslangic_tarihi"] = None
                    arac["bitis_tarihi"] = None
            return

    raise ValueError("Araç bulunamadı.")


def arac_kirala(araclar, plaka, musteri, baslangic, bitis):
    if bos_deger_kontrolu(musteri) or bos_deger_kontrolu(baslangic) or bos_deger_kontrolu(bitis):
        raise ValueError("Boş alan bırakılmamalıdır.")

    if not tarih_format_kontrolu(baslangic) or not tarih_format_kontrolu(bitis):
        raise ValueError("Tarih formatı GG/AA/YYYY olmalıdır.")

    for arac in araclar:
        if arac["plaka"] == plaka:

            if arac["durum"] == "kirada":
                raise ValueError("Araç zaten kirada.")

            gun = gun_sayisi_hesapla(baslangic, bitis)
            toplam_ucret = gun * arac["gunluk_ucret"]

            arac["durum"] = "kirada"
            arac["kiralayan"] = musteri
            arac["baslangic_tarihi"] = baslangic
            arac["bitis_tarihi"] = bitis

            return toplam_ucret

    raise ValueError("Araç bulunamadı.")


def arac_iade_et(araclar, plaka):
    for arac in araclar:
        if arac["plaka"] == plaka:
            if arac["durum"] != "kirada":
                raise ValueError("Araç zaten müsait.")
            arac["durum"] = "müsait"
            arac["kiralayan"] = None
            arac["baslangic_tarihi"] = None
            arac["bitis_tarihi"] = None
            return
    raise ValueError("Araç bulunamadı.")