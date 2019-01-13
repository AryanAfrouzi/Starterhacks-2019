from Tkinter import *
from time import *
import math
import sys
import socket
import threading
import requests
import random
import time

mybytemail = 'cristian@bmail.com'

fields=("To", "Subject", "Message")

c = 0

emails=[]
buttons=[]
    


#get the entries in the field
def fetch(entries):
    for entry in entries:  
        field=entry[0]
        text=entry[1]
        print('%s: "%s"' % (field, text))

#Enter the entries to the console
def makeform(root, fields):
    entries=[]
    for field in fields:
        width=30
        if field=="Message":
            row=Frame(root)
            textvar = StringVar()
            row.pack()
            label=Label(row, width=width, text=field, anchor=W, background="LightCyan3")
            entry=Text(row)

            
            entry.place(x=10, y=10, height=50, width=40)
            label.pack()
            entry.pack()
            entries.append((field, entry, textvar))
            
        else:
            row=Frame(root)
            row.configure(background="LightCyan3")
            textvar = StringVar()
            label=Label(row, width=width, text=field, anchor=W, background="LightCyan3")
            entry=Entry(row, textvariable=textvar)
            row.pack()
            label.pack()
            entry.pack()
            entries.append((field, entry, textvar))
    return entries

def clear(root):
    pass # clear text boxes
        
        
#Send function
def sendm(entry):
    global mybytemail
    message = entry[2][1].get("1.0",END)
    subject = entry[1][1].get()
    destinationEmail = entry[0][1].get()
    data = (mybytemail+"|&|"+destinationEmail+"|&|"+subject+"|&|"+message).encode()
    
    unSampledIPlist = requests.get('https://byte-mail-backend.appspot.com/iplist').text.split(', ')

    if len(unSampledIPlist) > 6:
        ipList = random.sample(unSampledIPlist, 6)+"127.0.0.1"
    else:
        ipList = unSampledIPlist[:]

    for each in ipList:
        unSampledIPlist.remove(each)

    for ip in ipList:
        if ip != '':
            print('sending to '+str(ip))
            try:
                send(data, ip)
            except:
                print('failed')
                try:
                    rand = random.sample(unSampledIPlist, 1)
                    unSampledIPlist.remove(rand)
                    ipList.append(rand)
                except:
                    pass
    print('Done forwarding.')

prdata = []
    
def send(data, address):
    s = socket.socket()
    s.settimeout(5)
    s.connect((address, 11219))
    s.send(data)

def forwardThread():
    global prdata, mybytemail, emails
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 11219))
    s.listen(5)
    while True:
        client, address = s.accept()
        print("Connection established with "+str(address))
        data = client.recv(1024)
        if data not in prdata:
            print("Data received, proceeding to forward..")
            print("Data = "+str(data.decode()))
            if data.split('|&|')[1] == mybytemail:
                emails.append([data.split('|&|')[0], data.split('|&|')[2], data.split('|&|')[3]])
            else:
                unSampledIPlist = requests.get('https://byte-mail-backend.appspot.com/iplist').text.split(', ')

                try:
                    unSampledIPlist.remove(address[0])
                except:
                    pass

                if len(unSampledIPlist) > 6:
                    ipList = random.sample(unSampledIPlist, 6)+"127.0.0.1"
                else:
                    ipList = unSampledIPlist[:]
                
                for each in ipList:
                    unSampledIPlist.remove(each)

                for ip in ipList:
                    if ip != '':
                        print('sending to '+str(ip))
                        try:
                            send(data, ip)
                        except:
                            print('failed')
                            try:
                                rand = random.sample(unSampledIPlist, 1)
                                unSampledIPlist.remove(rand)
                                ipList.append(rand)
                            except:
                                pass
                print('Done forwarding.')

def keepRegistered():
    global prdata
    while True:
        requests.post('https://byte-mail-backend.appspot.com/addip')
        time.sleep(270)
        prdata = []
        
def home():
    pass
        
def mailInbox():
    global c

    inboxWindow = Toplevel(root)
    inboxWindow.title("Inbox")
    width = 400
    height = 400
    inboxWindow.geometry('%sx%s' % (width, height))
    
    canvas = Canvas(inboxWindow, bg="LightCyan3")
    canvas.pack(expand=YES, fill=BOTH)
    
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=canvas.yview)

    
    for i in range (len(emails)):

        j = emails[i]
        a=emails.index(j)
        print(j)
        canvas.create_rectangle(2, a*100+2, width-3, (a+1)*100+2, outline="turquoise3", width=5)
        canvas.create_text(100, (((a)*100+2)+(((a+1)*100)+2))/2, text="From: " + j[0] + "\n" + "Subject: " + j[1], font=("Verdana", 20), anchor=W)

    for email in emails:
        button = Button(canvas, text="View Mail", anchor=E, command=lambda email=email: readMail(email))
        button.pack(pady=37)
        if c==1:
            break

def readMail():
    global c
    mailWindow = Toplevel(root)
    mailWindow.geometry("400x400")
    mailWindow.title("Message")

    mail = Text(mailWindow, height=35, width=150)

    scroll = Scrollbar(mailWindow, command=mail.yview)
    mail.configure(yscrollcommand=scroll.set)

    mail.tag_configure("font1", font=("Verdana", 30))
    mail.tag_configure("font2", font=("Verdana", 30))
    mail.tag_configure("font3", font=("Verdana", 15))

    mail.config(state=NORMAL)

    to = mail.insert(END, "From: " + email[0] + "\n\n", "font1")
    subject = mail.insert(END, "Subject: " + email[1] + "\n\n", "font2")
    message = mail.insert(END, "Message:" + "\n" + email[2], "font3")

    mail.config(state=DISABLED)

    mail.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)

    print("RM: ", email)
    c+=1


if __name__ == '__main__':

   t1 = threading.Thread(target=forwardThread)
   t1.start()

   t2 = threading.Thread(target=keepRegistered)
   t2.start()

   root = Tk()

   width2 = 400
   height2 = 400
   root.geometry('%sx%s' % (width2, height2))
   root.configure(background="LightCyan3")

   #creation of an instance
   #app = Window(root)

   top = Frame(root)
   top.pack(side=TOP)
   top.configure(background="LightCyan3")
   
   bottom = Frame(root)
   bottom.pack(side=BOTTOM)
   bottom.configure(background="LightCyan3")

   byteMail = Label(text="BYTE-MAIL", font=("Verdana", 25, "bold"), background="LightCyan3", anchor=W, justify=LEFT)
   byteMail.pack(in_=top, pady=5)
   byteMail.place(bordermode=OUTSIDE)

   button1 = Button(root, text="Mail Inbox", background="light blue", command=mailInbox)
   button1.pack(in_=top, side=LEFT, padx=15, pady=10)
   
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   button2 = Button(root, text="Send", background="yellow", command=(lambda e=ents: sendm(e)))
   button2.pack(in_=top, side=LEFT, padx=5, pady=5)
   root.mainloop()
