import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000, nickname='User'):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # GUI setup
        self.root = tk.Tk()
        self.root.title(f"Chat Client – {self.nickname}")
        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', wrap='word')
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)
        self.input_field = tk.Entry(self.root)
        self.input_field.pack(padx=10, pady=(0,10), fill='x')
        self.input_field.bind("<Return>", self.send_message_event)
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0,10))

    def start(self):
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print(f"Unable to connect: {e}")
            return
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.display_message(message)
            except ConnectionResetError:
                break
        self.sock.close()
        self.root.quit()

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        msg = self.input_field.get().strip()
        if msg:
            full_msg = f"{self.nickname}: {msg}"
            try:
                self.sock.sendall(full_msg.encode('utf-8'))
                self.input_field.delete(0, tk.END)
            except:
                pass

    def on_close(self):
        try:
            self.sock.close()
        except:
            pass
        self.root.quit()

if __name__ == "__main__":
    # you can take nickname input etc.
    nickname = input("Enter your nickname: ")
    host = input("Enter server host [127.0.0.1]: ") or '127.0.0.1'
    port_str = input("Enter server port [5000]: ") or '5000'
    port = int(port_str)
    client = ChatClient(host=host, port=port, nickname=nickname)
    client.start()