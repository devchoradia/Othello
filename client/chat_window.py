import tkinter as tk
from client.chat_client import ChatClient

class ChatWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.title('Chat')

        # chat window
        self.chat_box = tk.Text(self)
        self.chat_box.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.chat_box.configure(state='disable')

        # send button
        self.message_frame = tk.Frame(self)
        self.message_frame.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.message_label = tk.Label(self.message_frame, text='Message:')
        self.message_label.pack(side=tk.LEFT, padx=5)
        self.message_entry = tk.Entry(self.message_frame, width=80)
        self.message_entry.pack(side=tk.LEFT, padx=2)
        self.send_button = tk.Button(self.message_frame, text='Send', command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.client = ChatClient()
        self.client.set_observer(self)
        self.client.connect(username)

    def send_message(self):
        text = self.message_entry.get()
        self.client.send_message(text)
        self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, f'{message.text}\n')
        self.chat_box.configure(state='disabled')

    def close_window(self):
        self.client.disconnect()
        self.master.destroy()
