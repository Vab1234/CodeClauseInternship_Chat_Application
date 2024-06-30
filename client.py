import socket
import threading
from tkinter import *
from tkinter import scrolledtext , messagebox

HOST = "127.0.0.1"
PORT = 1234

DARK_GREY =  "#A9A9A9"
MEDIUM_GREY = "#7D7F7C"
OCEAN_BLUE = "#464EBB"
WHITE = "white"
FONT = ("Times New Roman" , 17)
BUTTON_FONT = ("Times New Roman" , 15)
SMALL_FONT = ("Times New Roman" , 13)

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)



root = Tk()
root.geometry("600x600")
root.title("Chat app")
root.resizable(False , False)

def add_message(message):
    msg_box.config(state=NORMAL)
    msg_box.insert(END , message + "\n")
    msg_box.config(state=DISABLED)

def connect():
    try:
        client.connect((HOST , PORT))
        print("Connection successful")
        add_message("[SERVER] Successfully coonnected to the server")
    except:
        messagebox.showerror(f"Unable to connect to server {HOST} and port {PORT}")
        exit(0)

    username = user_text.get()
    if username != "":
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid Username","Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_from_server , args = (client , )).start()

    user_button.config(state=DISABLED)
    user_text.config(state=DISABLED)


def send_message():
    message = msg_text.get()
    if message != "":
        client.sendall(message.encode())
        msg_text.delete(0 , END)
    else:
        messagebox.showerror("Empty message")

root.grid_rowconfigure(0 ,weight=1)
root.grid_rowconfigure(1 ,weight=4)
root.grid_rowconfigure(2 ,weight=1)

# Top Frame

top_frame = Frame(root , height=100 , width=600 , bg= DARK_GREY)
top_frame.grid(row = 0 , column=0 , sticky=NSEW)

middle_frame = Frame(root , height=400 , width=600 , bg= MEDIUM_GREY)
middle_frame.grid(row=1 , column=0 , sticky=NSEW)

bottom_frame = Frame(root , height=100 , width=600 , bg= DARK_GREY)
bottom_frame.grid(row=2 , column=0 , sticky=NSEW)

user_label = Label(top_frame , text = "Enter username" , font = FONT , bg = DARK_GREY , fg= WHITE )
user_label.pack(side = LEFT , padx=10)

user_text = Entry(top_frame , font=FONT , bg=MEDIUM_GREY , fg=WHITE , width=23)
user_text.pack(side= LEFT , padx=5)

user_button = Button(top_frame ,text = "Join Chat" , font=FONT , bg=OCEAN_BLUE , fg=WHITE , command = connect)
user_button.pack(side = LEFT , padx= 15)


# Bottom Frame
msg_text = Entry(bottom_frame , font = FONT , bg= MEDIUM_GREY , fg=WHITE , width=40)
msg_text.pack(side = LEFT , padx = 10)

msg_button = Button(bottom_frame , text = "Send" , font=FONT , bg=OCEAN_BLUE , fg=WHITE , command = send_message)
msg_button.pack(side=LEFT ,padx=10)

# Middle Frame
msg_box = scrolledtext.ScrolledText(middle_frame , font = SMALL_FONT , bg = MEDIUM_GREY , fg = WHITE , width = 67 , height = 27)
msg_box.config(state=DISABLED)
msg_box.pack(side = TOP)



def listen_from_server(client):
    while True:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            username = message.split(" : ")[0]
            content = message.split(" : ")[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Message cannot be empty")




def main():
    root.mainloop()
    
    

if __name__ == '__main__':
    main()