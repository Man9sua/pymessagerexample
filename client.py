import socket
import threading
from tkinter import Tk, Text, Entry, Button, END, simpledialog
from tkinter.ttk import Style

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Чат")

        #интерфейско
        style = Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TText", font=("Arial", 11))

        
        self.nickname = simpledialog.askstring("Никнейм", "Введите ваш никнейм:")
        if not self.nickname:
            self.nickname = "Аноним"

        # chatspace
        self.chat_area = Text(self.root, state="disabled", width=50, height=20, wrap="word", bg="#f9f9f9", fg="#333")
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # textspace
        self.message_entry = Entry(self.root, width=40, font=("Arial", 12))
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        # 'send' button
        self.send_button = Button(self.root, text="Отправить", command=self.send_message, bg="#4caf50", fg="white")
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        #connecting new client to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 5555))

        self.running = True
        threading.Thread(target=self.receive_messages).start()

        # Приветственное сообщение
        self.client_socket.send(f"{self.nickname} присоединился к чату.".encode("utf-8"))

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            formatted_message = f"{self.nickname}: {message}"
            self.client_socket.send(formatted_message.encode("utf-8"))
            self.message_entry.delete(0, END)
            self.update_chat_area(formatted_message, from_me=True)

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                self.update_chat_area(message, from_me=False)
            except:
                self.running = False
                self.client_socket.close()
                break

    def update_chat_area(self, message, from_me):
        self.chat_area.config(state="normal")
        self.chat_area.insert(END, (f"Вы: {message.split(':', 1)[1]}" if from_me else message) + "\n")
        self.chat_area.see(END)
        self.chat_area.config(state="disabled")
        self.save_to_history(message)

    def save_to_history(self, message):
        with open("chat_history.txt", "a", encoding="utf-8") as history_file:
            history_file.write(message + "\n")

    def close_connection(self):
        self.running = False
        self.client_socket.send(f"{self.nickname} покинул чат.".encode("utf-8"))
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.close_connection)
    root.mainloop()
