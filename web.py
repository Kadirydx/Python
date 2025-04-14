import http.server
import socketserver
import os

# Betiğin çalıştırıldığı dizini paylaş
os.chdir(os.getcwd())  # Çalıştırılan dizin otomatik olarak ayarlanır

# Port numarasını belirleyin
PORT = 8080

# Sunucu kök dizinini belirlemek ve istekleri yönetmek için özelleştirilmiş bir sınıf
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def send_error(self, code, message=None):
        # Dizin listeleme isteği geldiğinde 404 hatası döndürür
        if code == 403:
            self.send_response(403)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Forbidden access!")
        else:
            super().send_error(code, message)

    def list_directory(self, path):
        # Dizin listelemeyi devre dışı bırakıyoruz
        self.send_error(403)  # Erişim yasaklandı

    def do_GET(self):
        # Belirli dosyalar için özel işlevler
        if self.path == '/':
            self.path = '/index.html'  # Varsayılan dosya
        elif self.path == '/client.py':  # `client.py` dosyasını indirilebilir yapıyoruz
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename=client.py')
            self.end_headers()
            with open('client.py', 'rb') as f:
                self.wfile.write(f.read())
            return
        return super().do_GET()

# Sunucu başlatma
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Sunucu başlatıldı: http://localhost:{PORT}")
    httpd.serve_forever()
