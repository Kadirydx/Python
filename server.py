import socket
import threading

HOST = input("HOST?(def:127.0.0.1) :") 
PORT = 12345       

# Bağlantıları ve kullanıcı adlarını saklayacağız
clients = {}  # {nickname: socket} şeklinde bir sözlük
nicknames = set()  # Alınan nicknameleri burada tutacağız

def handle_client(client_socket, client_address):
    try:
        # Nickname alındı
        nickname = client_socket.recv(1024).decode('utf-8')
        
        # Aynı nickname daha önce kullanılmışsa, bağlantıyı kes
        if nickname in nicknames:
            client_socket.send("Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.".encode('utf-8'))
            client_socket.close()
            return
        else:
            # Yeni kullanıcı adı ekleniyor
            nicknames.add(nickname)
            clients[client_socket] = nickname
            print(f"{nickname} bağlandı.")

        # Kullanıcıya  mesaj
        client_socket.send(f"Hoş geldiniz {nickname}!".encode('utf-8'))

        # Diğer tüm kullanıcılara yeni kullanıcıyı duyur
        broadcast(f"{nickname} katıldı.", client_socket)

        # Kullanıcıdan gelen mesajları alıp, tüm kullanıcılara ilet
        while True:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{nickname}: {message.decode('utf-8')}", client_socket)
            else:
                # Bağlantı kesildiyse
                break

        # Bağlantı kesildiğinde
        remove_client(client_socket)

    except Exception as e:
        print(f"Hata: {e}")
        remove_client(client_socket)

# Bağlantıdan kullanıcıyı çıkartma
def remove_client(client_socket):
    nickname = clients.pop(client_socket, None)
    if nickname:
        nicknames.remove(nickname)
        broadcast(f"{nickname} çıkış yaptı.", client_socket)
        client_socket.close()

# Tüm kullanıcılara mesaj gönderme
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:  # Mesajı göndereni hariç tut
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Sunucu başlatma
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Sunucu {HOST}:{PORT} üzerinde çalışıyor...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} bağlandı.")

        # Yeni bir iş  başlatıyoruz, her bir istemci için
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
