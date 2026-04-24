from PyQt5.QtWidgets import QApplication
from backend.dosya import verileri_yukle, verileri_kaydet
from gui import CarRentalApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    araclar = verileri_yukle()
    pencere = CarRentalApp(araclar)
    pencere.show()

    app.exec_()
    verileri_kaydet(araclar)