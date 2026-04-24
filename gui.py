from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QApplication,
    QGroupBox, QHeaderView, QComboBox,
    QDialog, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QDate

from backend.islemler import (
    arac_ekle,
    arac_sil,
    arac_duzenle,
    arac_kirala,
    arac_iade_et
)

RENK_ARKAPLAN = "#cbd5e1"
RENK_PANEL = "#ffffff"
RENK_YAZI = "#1e293b"
RENK_KENARLIK = "#94a3b8"
RENK_BTN_MAVI = "#2563eb"
RENK_BTN_YESIL = "#10b981"
RENK_BTN_KIRMIZI = "#ef4444"
RENK_BTN_TURUNCU = "#f59e0b"

class RentalDialog(QDialog):
    def __init__(self, plaka, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Araç Kirala: {plaka}")
        self.resize(450, 280)
        
        self.setStyleSheet(f"background-color: {RENK_PANEL}; color: {RENK_YAZI}; font-size: 14px;")

        layout = QFormLayout(self)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Müşteri Adı Soyadı")
        self.customer_name.setStyleSheet(f"border: 1px solid {RENK_KENARLIK}; padding: 8px; border-radius: 4px; min-height: 30px;")
        
        self.start_date = QLineEdit()
        self.start_date.setPlaceholderText("GG/AA/YYYY")
        self.start_date.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        self.start_date.setStyleSheet(f"border: 1px solid {RENK_KENARLIK}; padding: 8px; border-radius: 4px; min-height: 30px;")
        
        self.end_date = QLineEdit()
        self.end_date.setPlaceholderText("GG/AA/YYYY")
        self.end_date.setStyleSheet(f"border: 1px solid {RENK_KENARLIK}; padding: 8px; border-radius: 4px; min-height: 30px;")
        
        layout.addRow("Müşteri:", self.customer_name)
        layout.addRow("Başlangıç:", self.start_date)
        layout.addRow("Bitiş:", self.end_date)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        ok_btn = buttons.button(QDialogButtonBox.Ok)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        
        btn_style = f"padding: 10px 25px; font-weight: bold; border-radius: 6px; font-size: 14px;"
        ok_btn.setStyleSheet(f"background-color: {RENK_BTN_MAVI}; color: white; {btn_style}")
        cancel_btn.setStyleSheet(f"background-color: {RENK_KENARLIK}; color: white; {btn_style}")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return {
            "musteri": self.customer_name.text(),
            "baslangic": self.start_date.text(),
            "bitis": self.end_date.text()
        }

class CarRentalApp(QMainWindow):
    def __init__(self, araclar):
        super().__init__()
        self.araclar = araclar
        self.setWindowTitle("Araç Kiralama Sistemi")
        self.setWindowState(Qt.WindowMaximized)

        self.setStyleSheet(f"""
            QMainWindow, QWidget#centralWidget {{ background-color: {RENK_ARKAPLAN}; }}
            QGroupBox {{ 
                background-color: {RENK_PANEL}; 
                border: 2px solid {RENK_KENARLIK}; 
                border-radius: 12px; 
                margin-top: 25px; 
                font-weight: bold; 
                color: {RENK_YAZI};
                font-size: 16px;
            }}
            QGroupBox::title {{ subcontrol-origin: padding; left: 12px; top: 12px; }}
            QLabel {{ color: {RENK_YAZI}; font-weight: bold; font-size: 15px; }}
            QLineEdit, QComboBox {{ 
                background-color: {RENK_PANEL}; 
                border: 1px solid {RENK_KENARLIK}; 
                border-radius: 6px; 
                padding: 8px; 
                color: {RENK_YAZI};
                font-size: 14px;
                min-height: 30px;
            }}
            QTableWidget {{ 
                background-color: {RENK_PANEL}; 
                border: 1px solid {RENK_KENARLIK}; 
                gridline-color: {RENK_KENARLIK}; 
                color: {RENK_YAZI};
                font-size: 20px;
            }}
            QHeaderView::section {{ background-color: {RENK_KENARLIK}; font-weight: bold; border: none; padding: 10px; font-size: 14px; }}
            QPushButton {{ 
                color: white; 
                font-weight: bold; 
                border-radius: 8px; 
                padding: 12px 30px; 
                border: none; 
                font-size: 15px;
                min-width: 110px;
            }}
            QMessageBox QPushButton {{
                color: black;
            }}
        """)

        self._arayuz_olustur()
        self.tabloyu_doldur()

    # ------------------ ARAYÜZ ------------------

    def _arayuz_olustur(self):
        cw = QWidget()
        cw.setObjectName("centralWidget")
        self.setCentralWidget(cw)
        
        main_layout = QVBoxLayout(cw)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # --- Giriş Alanları ---
        box_ekle = QGroupBox("Yeni Araç Ekle")
        layout_ekle = QHBoxLayout(box_ekle)
        layout_ekle.setContentsMargins(25, 40, 25, 25)

        self.in_plate = QLineEdit()
        self.in_plate.setPlaceholderText("34ABC123")
        self.in_brand = QLineEdit()
        self.in_brand.setPlaceholderText("Marka")
        self.in_model = QLineEdit()
        self.in_model.setPlaceholderText("Model")
        self.in_price = QLineEdit()
        self.in_price.setPlaceholderText("1500")

        self.btn_add = QPushButton("Ekle")
        self.btn_add.setStyleSheet(f"background-color: {RENK_BTN_YESIL};")
        self.btn_add.clicked.connect(self.arac_ekle_gui)

        layout_ekle.addWidget(QLabel("Plaka:"))
        layout_ekle.addWidget(self.in_plate)
        layout_ekle.addWidget(QLabel("Marka:"))
        layout_ekle.addWidget(self.in_brand)
        layout_ekle.addWidget(QLabel("Model:"))
        layout_ekle.addWidget(self.in_model)
        layout_ekle.addWidget(QLabel("Ücret:"))
        layout_ekle.addWidget(self.in_price)
        layout_ekle.addWidget(self.btn_add)

        main_layout.addWidget(box_ekle)

        box_filtre = QGroupBox("Filtreleme")
        layout_filtre = QHBoxLayout(box_filtre)
        layout_filtre.setContentsMargins(25, 40, 25, 25)

        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["Hepsi", "Müsait", "Kirada", "Bakımda"])
        self.combo_filter.currentTextChanged.connect(self.filtre_uygula)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Plaka veya Marka Ara...")
        self.search_input.textChanged.connect(self.filtre_uygula)

        layout_filtre.addWidget(QLabel("Durum:"))
        layout_filtre.addWidget(self.combo_filter)
        layout_filtre.addWidget(QLabel("Arama:"))
        layout_filtre.addWidget(self.search_input)

        main_layout.addWidget(box_filtre)

        # --- Tablo ---
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["Plaka", "Marka", "Model", "Durum", "Ücret", "Müşteri", "Tarih"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.setEditTriggers(QTableWidget.DoubleClicked)
        self.tablo.itemChanged.connect(self.arac_duzenle_gui)
        main_layout.addWidget(self.tablo)

        # --- Butonlar ---
        layout_btn = QHBoxLayout()
        layout_btn.setSpacing(20)

        self.btn_rent = QPushButton("Kiralama Başlat")
        self.btn_rent.setStyleSheet(f"background-color: {RENK_BTN_MAVI};")
        self.btn_rent.clicked.connect(self.arac_kirala_gui)

        self.btn_return = QPushButton("İade Et")
        self.btn_return.setStyleSheet(f"background-color: {RENK_BTN_TURUNCU};")
        self.btn_return.clicked.connect(self.arac_iade_gui)

        self.btn_delete = QPushButton("Araç Sil")
        self.btn_delete.setStyleSheet(f"background-color: {RENK_BTN_KIRMIZI};")
        self.btn_delete.clicked.connect(self.arac_sil_gui)

        layout_btn.addWidget(self.btn_rent)
        layout_btn.addWidget(self.btn_return)
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_delete)

        main_layout.addLayout(layout_btn)

    # ------------------ TABLO ------------------

    def tabloyu_doldur(self, veri_listesi=None):
        liste = veri_listesi if veri_listesi is not None else self.araclar
        self.tablo.setRowCount(len(liste))

        for satir, arac in enumerate(liste):
            tarih = f"{arac['baslangic_tarihi']} - {arac['bitis_tarihi']}" if arac.get("baslangic_tarihi") else ""
            
            self.tablo.setItem(satir, 0, QTableWidgetItem(arac["plaka"]))
            self.tablo.setItem(satir, 1, QTableWidgetItem(arac["marka"]))
            self.tablo.setItem(satir, 2, QTableWidgetItem(arac["model"]))
            self.tablo.setItem(satir, 3, QTableWidgetItem(arac["durum"]))
            self.tablo.setItem(satir, 4, QTableWidgetItem(str(arac["gunluk_ucret"]) + " TL"))
            self.tablo.setItem(satir, 5, QTableWidgetItem(arac.get("kiralayan") or "-"))
            self.tablo.setItem(satir, 6, QTableWidgetItem(tarih))

    def secili_plaka(self):
        satir = self.tablo.currentRow()
        if satir == -1:
            raise ValueError("Lütfen işlem yapmak için tablodan bir araç seçiniz.")
        return self.tablo.item(satir, 0).text()

    def filtre_uygula(self):
        durum = self.combo_filter.currentText()
        aranan = self.search_input.text().lower()
        filtrelenen = []

        for arac in self.araclar:
            durum_ok = (durum == "Hepsi") or (arac["durum"].lower() == durum.lower())
            metin_ok = not aranan or (aranan in arac["plaka"].lower() or aranan in arac["marka"].lower())
            
            if durum_ok and metin_ok:
                filtrelenen.append(arac)
        
        self.tabloyu_doldur(filtrelenen)

    # ------------------ GUI → BACKEND ------------------

    def arac_ekle_gui(self):
        try:
            arac_ekle(self.araclar, self.in_plate.text(), self.in_brand.text(), self.in_model.text(), self.in_price.text())
            for i in [self.in_plate, self.in_brand, self.in_model, self.in_price]: i.clear()
            self.tabloyu_doldur()
            self.filtre_uygula()
            QMessageBox.information(self, "Başarılı", "Araç eklendi.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def arac_sil_gui(self):
        try:
            plaka = self.secili_plaka()
            if QMessageBox.question(self, "Onay", f"{plaka} silinsin mi?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                arac_sil(self.araclar, plaka)
                self.tabloyu_doldur()
                self.filtre_uygula()
                QMessageBox.information(self, "Başarılı", "Araç silindi.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def arac_iade_gui(self):
        try:
            plaka = self.secili_plaka()
            arac_iade_et(self.araclar, plaka)
            self.tabloyu_doldur()
            self.filtre_uygula()
            QMessageBox.information(self, "Başarılı", "Araç iade alındı.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def arac_kirala_gui(self):
        try:
            plaka = self.secili_plaka()
            arac = next((a for a in self.araclar if a["plaka"] == plaka), None)
            if arac and arac["durum"] == "kirada":
                QMessageBox.warning(self, "Hata", "Bu araç zaten kirada!")
                return

            dialog = RentalDialog(plaka, self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                ucret = arac_kirala(self.araclar, plaka, data["musteri"], data["baslangic"], data["bitis"])
                self.tabloyu_doldur()
                self.filtre_uygula()
                QMessageBox.information(self, "Başarılı", f"Kiralama Tamamlandı.\nTutar: {ucret} TL")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def arac_duzenle_gui(self, item):
        row = item.row()
        col = item.column()
        yeni_deger = item.text()

        plaka_item = self.tablo.item(row, 0)
        if not plaka_item:
            return
        plaka = plaka_item.text()

        try:
            self.tablo.itemChanged.disconnect(self.arac_duzenle_gui)

            if col == 2:  # Model
                arac_duzenle(self.araclar, plaka, yeni_model=yeni_deger)
            elif col == 3:  # Durum
                arac_duzenle(self.araclar, plaka, yeni_durum=yeni_deger.lower())
            elif col == 4:  # Ücret
                yeni_ucret = yeni_deger.replace(" TL", "").strip()
                arac_duzenle(self.araclar, plaka, yeni_gunluk_ucret=yeni_ucret)
                self.tabloyu_doldur()
                self.filtre_uygula()
            else:
                pass

        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
            self.tabloyu_doldur()
            self.filtre_uygula()
        finally:
            self.tablo.itemChanged.connect(self.arac_duzenle_gui)