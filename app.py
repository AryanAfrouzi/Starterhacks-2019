    width = 400
    height =400
    inboxWindow.geometry('%sx%s' % (width, height))

    canvas = Canvas(inboxWindow, bg="white")
    canvas.pack(expand=YES, fill=BOTH)

    for email in emails:
        buttons.append(0)
        a=emails.index(email)
        canvas.create_rectangle(2, (emails.index(email))*100+2, width-3, ((emails.index(email)+1)*100)+2, outline="red", width=1)
        canvas.create_text(100, (((emails.index(email))*100+2)+(((emails.index(email)+1)*100)+2))/2, text="From: " + email[0] + "\n" + "Subject: " + email[1], font=("Helvetica", 20), anchor=W)
        buttons[a] = Button(canvas, text="View Mail", anchor=E, command=readMail)
        buttons[a].pack(pady=37)

def readMail():
    mailWindow = Toplevel(root)
    mailWindow.geometry("400x400")

    label = Label(mailWindow, text=emails[2])
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
