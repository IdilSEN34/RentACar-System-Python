from datetime import datetime


def bos_deger_kontrolu(deger):
    return deger is None or str(deger).strip() == ""


def tarih_format_kontrolu(tarih):
    try:
        datetime.strptime(tarih, "%d/%m/%Y")
        return True
    except ValueError: # Sadece değer hatalarında False döner
        return False
    