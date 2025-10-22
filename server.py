import socket
import threading
import argparse
from datetime import datetime
import os

def get_local_ip():
    """Automatically detect the local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

class ChatServer:
    def __init__(self, host, port, history_file="./Storage/chat_history.txt"):
        self.host = host
        self.port = port
        self.clients = []
        self.history_file = history_file
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Make sure file exists
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                f.write("")

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients, daemon=True).start()

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
            self.send_history(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def send_history(self, conn):
        """Send saved conversation history to a newly connected client."""
        try:
            with open(self.history_file, "r") as f:
                history = f.read().strip()
            if history:
                conn.sendall(history.encode('utf-8') + b'\n')
        except:
            pass

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8').strip()
                timestamp = datetime.now().strftime("[%H:%M:%S]")
                full_msg = f"{timestamp} {msg}"
                print(full_msg)
                self.save_message(full_msg)
                self.broadcast(full_msg)
        except ConnectionResetError:
            pass
        finally:
            print(f"Connection closed: {addr}")
            conn.close()
            self.clients = [(c, a) for (c, a) in self.clients if c != conn]

    def broadcast(self, message, sender=None):
        """Send message to all connected clients."""
        message_with_newline = message.rstrip() + '\n'  # ensure exactly one newline
        for conn, _ in self.clients:
            try:
                conn.sendall(message_with_newline.encode('utf-8'))
            except:
                pass


    def save_message(self, message):
        """Append message to the history file."""
        with open(self.history_file, "a") as f:
            f.write(message.rstrip() + "\n")

    def shutdown(self):
        print("Shutting down server.")
        for conn, _ in self.clients:
            try:
                conn.close()
            except:
                pass
        self.sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Chat Server with History")
    parser.add_argument("host", nargs="?", default=None, help="Host IP address (optional)")
    parser.add_argument("port", nargs="?", type=int, default=5000, help="Port (default: 5000)")
    args = parser.parse_args()

    host = args.host or get_local_ip()
    port = args.port

    server = ChatServer(host, port)
    server.start()
