import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("CHAT")
        self.win.configure(bg="snow")

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, width=50, bg="snow")
        self.text_area.grid(column=0, row=1, padx=5, pady=5, sticky="nw")
        self.text_area.config(state="disabled", font=('Calibri', 16,))

        self.clients_area = tkinter.Text(self.win, width=13, bg="snow")
        self.clients_area.grid(column=1, row=0, rowspan=5, padx=5, pady=5, sticky="ns")
        self.clients_area.config(state="disabled", font=('Calibri', 16))

        self.msg_label = tkinter.Label(self.win, text="Сообщение:", bg="snow")
        self.msg_label.config(font=('Calibri', 18, "bold"))
        self.msg_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")

        self.input_area = tkinter.Text(self.win, width=55, height=5, bg="snow")
        self.input_area.config(font=('Calibri', 15))
        self.input_area.grid(column=0, row=3, padx=5, pady=5, sticky="sw")

        self.send_button = tkinter.Button(self.win, text="Отправить", command=self.write)
        self.send_button.config(font=('Calibri', 14))
        self.send_button.grid(column=0, row=4, padx=5, pady=5, sticky="s")

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
        self.clients_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            if self.gui_done:
                try:
                    message = self.sock.recv(1024).decode("utf-8")
                    if message == 'NICK':
                        self.sock.send(self.nickname.encode('utf-8'))
                    elif '[USERS]' in message:
                        clients_list = message[7:]
                        self.clients_area.config(state="normal")
                        self.clients_area.delete('1.0', 'end')
                        self.clients_area.insert('end', clients_list)
                        self.clients_area.yview('end')
                        self.clients_area.config(state="disabled")
                    else:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
                except ConnectionAbortedError:
                    break
                except:
                    print("Error")
                    self.sock.close()
                    break


client = Client(HOST, PORT)
