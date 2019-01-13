from Tkinter import *
from time import *
import math
import sys
import socket
import threading
import requests
import random
import time

mybytemail = 'test@bmail'

fields=("To", "Subject", "Message")

emails=[]
buttons=[]

for email in emails:
    buttons.append(0)


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
            label=Label(row, width=width, text=field, anchor=W)
            entry=Text(row)

            
            entry.place(x=10, y=10, height=50, width=40)
            label.pack()
            entry.pack()
            entries.append((field, entry, textvar))
            
        else:
            row=Frame(root)
            textvar = StringVar()
            label=Label(row, width=width, text=field, anchor=W)
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
    global buttons
    
    inboxWindow = Toplevel(root)
    width = 400
    height =400
    inboxWindow.geometry('%sx%s' % (width, height))
    
    canvas = Canvas(inboxWindow, bg="white")
    canvas.pack(expand=YES, fill=BOTH)
    
    for email in emails:
        
        a=emails.index(email)
        canvas.create_rectangle(2, (emails.index(email))*100+2, width-3, ((emails.index(email)+1)*100)+2, outline="red", width=1)
        canvas.create_text(100, (((emails.index(email))*100+2)+(((emails.index(email)+1)*100)+2))/2, text="From: " + email[0] + "\n" + "Subject: " + email[1], font=("Helvetica", 20), anchor=W)
        buttons[a] = Button(canvas, text="View Mail", anchor=E, command=readMail)
        button.pack(pady=37)

def readMail():
    mailWindow = Toplevel(root)
    mailWindow.geometry("400x400")

    label = Label(mailWindow, text=email[2])
    label.pack()


if __name__ == '__main__':

   t1 = threading.Thread(target=forwardThread)
   t1.start()

   t2 = threading.Thread(target=keepRegistered)
   t2.start()

   root = Tk()

   width2 = 400
   height2 = 400
   root.geometry('%sx%s' % (width2, height2))

   #creation of an instance
   #app = Window(root)

   top = Frame(root)
   top.pack(side=TOP)
   
   bottom = Frame(root)
   bottom.pack(side=BOTTOM)

   Label(text="Welcome to Byte-Mail, an All-Secure Messaging Platform", font=("Helvetica", 30)).pack(in_=top, pady=5)

   button1 = Button(root, text="Mail Inbox", background="yellow", command=mailInbox)
   button1.pack(in_=top, side=LEFT, padx=5, pady=5)
   
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   button2 = Button(root, text="Send", background="yellow", command=(lambda e=ents: sendm(e)))
   button2.pack(in_=top, side=LEFT, padx=5, pady=5)
   root.mainloop()
