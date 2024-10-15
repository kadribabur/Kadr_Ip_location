import sys
import socket
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class IPTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Pencere ayarları
        self.setWindowTitle('IP Tracker')
        self.setGeometry(100, 100, 400, 500)

        # Layout oluşturma
        layout = QVBoxLayout()
        
        # IP girişi için etiket ve giriş kutusu
        self.ip_label = QLabel('IP Adresi Girin (Boş bırakılırsa yerel IP kullanılır):')
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('Örneğin: 8.8.8.8')
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)

        # Takip butonu
        self.track_button = QPushButton('IP\'yi Takip Et')
        self.track_button.clicked.connect(self.track_ip)
        layout.addWidget(self.track_button)

        # Sonuçları göstermek için metin kutusu
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def track_ip(self):
        ip = self.ip_input.text().strip()
        if ip == "":
            try:
                ip = socket.gethostbyname(socket.gethostname())
            except socket.gaierror:
                QMessageBox.critical(self, "Hata", "Yerel IP adresi alınamadı.")
                return

        # IP bilgilerini çekme
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            ip_response = response.json()

            if ip_response["status"] == "fail":
                QMessageBox.warning(self, "Hata", f"IP bilgileri alınamadı: {ip_response.get('message', 'Bilinmeyen hata')}")
                return

            # IP detaylarını oluşturma
            ip_details = (
                f"<b>IP:</b> {ip_response.get('query', 'N/A')}<br>"
                f"<b>Ülke:</b> {ip_response.get('country', 'N/A')}<br>"
                f"<b>Ülke Kodu:</b> {ip_response.get('countryCode', 'N/A')}<br>"
                f"<b>Bölge:</b> {ip_response.get('regionName', 'N/A')}<br>"
                f"<b>Şehir:</b> {ip_response.get('city', 'N/A')}<br>"
                f"<b>Posta Kodu:</b> {ip_response.get('zip', 'N/A')}<br>"
                f"<b>Zaman Dilimi:</b> {ip_response.get('timezone', 'N/A')}<br>"
                f"<b>ISP:</b> {ip_response.get('isp', 'N/A')}<br>"
                f"<b>Organizasyon:</b> {ip_response.get('org', 'N/A')}<br>"
                f"<b>AS:</b> {ip_response.get('as', 'N/A')}<br>"
                f"<b>Enlem:</b> {ip_response.get('lat', 'N/A')}<br>"
                f"<b>Boylam:</b> {ip_response.get('lon', 'N/A')}<br>"
            )

            self.result_text.setHtml(ip_details)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Hata", f"IP bilgileri alınırken bir hata oluştu: {e}")

def main():
    app = QApplication(sys.argv)
    tracker = IPTracker()
    tracker.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
