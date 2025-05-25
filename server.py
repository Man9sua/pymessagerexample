import socket
import threading

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client_socket, client_address):
    print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {client_address} подключился.")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"[{client_address}] {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    print(f"[ОТКЛЮЧЕНО] {client_address} отключился.")
    clients.remove(client_socket)
    disconnect_message = f"Пользователь {client_address} отключился.".encode("utf-8")
    broadcast(disconnect_message, None)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(5)
    print("[ЗАПУСК] Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[АКТИВНЫЕ ПОДКЛЮЧЕНИЯ] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
