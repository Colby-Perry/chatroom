import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.clients = []  # list of (conn, addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients, daemon=True).start()
        # keep main thread alive
        while True:
            cmd = input()
            if cmd.lower() == 'quit':
                break
        self.shutdown()

    def accept_clients(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"New connection from {addr}")
            self.clients.append((conn, addr))
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                self.broadcast(message, sender=conn)
        except ConnectionResetError:
            pass
        finally:
            print(f"Connection closed: {addr}")
            conn.close()
            self.clients = [(c,a) for (c,a) in self.clients if c != conn]

    def broadcast(self, message, sender=None):
        for conn, addr in self.clients:
            if conn != sender:
                try:
                    conn.sendall(message.encode('utf-8'))
                except:
                    pass

    def shutdown(self):
        print("Shutting down server.")
        for conn, addr in self.clients:
            try:
                conn.close()
            except:
                pass
        self.sock.close()

if __name__ == "__main__":
    server = ChatServer(host='10.0.0.219', port=5000)
    server.start()
