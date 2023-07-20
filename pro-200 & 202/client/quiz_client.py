import socket
from threading import Thread
from tkinter import *

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address='127.0.0.1'
port= 4000

client.connect((ip_address,port))

print("Connected with the server !")

class GUI:   
    def __init__(self):
       self.Window=Tk()
       self.Window.withdraw()
       self.login=Toplevel()
       self.login.title("Login")
       self.login.resizable(width=False,height=False)
       self.login.configure(width=500,height=300)
       self.pls=Label(self.login,text="Login to continue",justify=CENTER,font=("Cambria",14),bd=2)
       self.pls.place(relheight=0.15,relx=0.3,rely=0.07)
       self.labelName=Label(self.login,text="Name: ",font=("Cambria",14),bd=1)
       self.labelName.place(relheight=0.2,relx=0.2,rely=0.2)
       self.entryName=Entry(self.login,font=("Cambria",14),bd=1)
       self.entryName.place(relheight=0.12,relwidth=0.4,relx=0.35,rely=0.2)
       self.entryName.focus()
       self.goButton=Button(self.login,text="Continue",command=lambda:self.goAhead(self.entryName.get()))
       self.goButton.place(relx=0.4,rely=0.55)
       self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        #self.name=name
        self.layout(name)
        rcv=Thread(target=self.receive)
        rcv.start()

    def showText(self,message):
        self.textContent.config(state=NORMAL)
        self.textContent.insert(END,message+"\n\n")
        self.textContent.config(state=DISABLED)
        self.textContent.see(END)

    def write(self):
        self.textContent.config(state=DISABLED)
        while True:
            message=(f"{self.name}:{self.message}")
            client.send(message.encode('utf-8'))
            self.showText(message)
            break

    def sendButton(self,message):
        self.textContent.config(state=DISABLED)
        self.message=message
        self.textEntry.delete(0,END)
        send=Thread(target=self.write)
        send.start()


    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("Quiz")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="#38060f")
        self.labelTopic=Label(self.Window,bg="white",fg="white",text=self.name,font="Cambria",pady=5)
        self.labelTopic.place(relwidth=1)
        self.line=Label(self.Window,width=450,bg="black")
        self.line.place(relwidth=1,rely=0.07,relheight=0.01)
        self.textContent=Text(self.Window,width=20,height=2,bg="#38060f",fg="#f4a4a4")
        self.textContent.place(relwidth=1,rely=0.08,relheight=0.745)
        self.labelBottom=Label(self.Window,bg="#a83038",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        self.textEntry=Entry(self.labelBottom,bg="#a83038",fg="#f4a4a4",font="Cambria")
        self.textEntry.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.textEntry.focus()
        self.textButton=Button(self.labelBottom,text="GO",font="Cambria",width=30,bg="#38060f",fg="White",command=lambda:self.sendButton(self.textEntry.get()))
        self.textButton.place(relx=0.77,rely=0.008,relwidth=0.24,relheight=0.06)
        self.textContent.config(cursor="arrow")
        scrollbar=Scrollbar(self.textContent)
        scrollbar.place(relheight=1,relx=0.96)
        scrollbar.config(command=self.textContent.yview)
        self.textContent.config(state=DISABLED)
        

    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showText(message)
            except:
                print("An error occured !")
                client.close()
                break

   

   
"""
def write():
    while True:
        message='{}:{}'.format(nickname,input(''))
        client.send(message.encode('utf-8'))

receive_thread=Thread(target=receive)
receive_thread.start()
write_thread=Thread(target=write)
write_thread.start()"""

g=GUI()