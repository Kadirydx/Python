import socket
import threading

HOST = input("HOST?(def:127.0.0.1) :") 
PORT = 12345        

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = ""
# Sunucuya bağlanma
def connect_to_server():
    try:
        client_socket.connect((HOST, PORT))
        print(f"Sunucuya bağlanıldı: {HOST}:{PORT}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        exit()

# Kullanıcıdan mesaj alıp sunucuya gönderme
def send_message():
    while True:
        message = input(f"{nickname}: ")  # Kullanıcıdan mesaj alırken formatı nickname: mesaj şeklinde tutuyoruz
        if message.lower() == 'exit':
            client_socket.close()
            print("Bağlantı kapatıldı.")
            break
        # Mesajı gönderirken başına nickname ekliyoruz
        full_message = f"{nickname}: {message}"
        client_socket.send(full_message.encode('utf-8'))


def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message) 
            else:
                print("Sunucu ile bağlantı kesildi.")
                break
        except:
            print("Mesaj alınırken bir hata oluştu.")
            break

# Bağlantıyı başlatma
def start_client():
    global nickname
    connect_to_server()

    # Nickname alma
    nickname = input("Adınızı girin: ")

    # Nickname'i sunucuya gönderme
    client_socket.send(nickname.encode('utf-8'))

    # Kullanıcıdan mesaj alma ve sunucudan mesaj alma işlemlerini paralel çalıştırmak için 
    threading.Thread(target=send_message, daemon=True).start()  # Kullanıcıdan mesaj al
    threading.Thread(target=receive_message, daemon=True).start()  # Sunucudan mesaj al

    # İşlemlerin devam etmesi için ana  çalışması gerekiyor
    while True:
        pass

if __name__ == "__main__":
    start_client()
