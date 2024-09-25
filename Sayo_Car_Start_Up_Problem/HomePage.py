from tkinter import *
import os
import datetime
from PIL import Image, ImageTk

app = Tk()
app.title("Car Start Up Diagnosis System")
app.geometry('1000x500')
app.configure(border="1")
first = StringVar()
date = datetime.datetime.now().date()


def AdminLogin():
    os.system('AdminLogin.py')


def UserLogin():
    os.system('UserLogin.py')


def GuestPage():
    os.system('GuestUser.py')


def set_background(image_path):
    image = Image.open(image_path)
    image = image.resize((1000, 500))
    background_image = ImageTk.PhotoImage(image)

    canvas = Canvas(app, width=1000, height=500)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.image = background_image

    return canvas


image_path = "background\\background.jpg"

canvas = set_background(image_path)

homepageframe = Frame(app, width='300', height='300', background='white')
homepageframe.place(x=600, y=150)
homepageframeheader = Frame(homepageframe, width='290', height='40', background='darkblue')
homepageframeheader.place(x=5, y=6)
homelabel = Label(app, text="CAR START UP DIAGNOSIS SYSTEM", fg='white', bg='darkblue',
                  font=("Microsoft Yahei Ui Light", 20, 'bold'))
homelabel.place(x=250, y=40)
welcomelabel = Label(homepageframeheader, text="How may we help you?", fg='white', bg='darkblue',
                     font=("Microsoft Yahei Ui Light", 10, 'bold'))
welcomelabel.place(x=3, y=3)
welcomelabel = Label(homepageframe, text="Please Login in as either Admin or user", fg='black', bg='white',
                     font=("Microsoft Yahei Ui Light", 10, 'bold'), )
welcomelabel.place(x=10, y=60)
adminlogin = Button(homepageframe, width='31', border='0', text='Admin Login', fg='white', bg='darkblue',
                    font=("Microsoft Yahei Ui Light", 10, 'bold'), command=AdminLogin, cursor="hand2", relief=SOLID)
adminlogin.place(x=8, y=100)
userlogin = Button(homepageframe, width='31', border='0', text='User Login', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), command=UserLogin, cursor="hand2", relief=SOLID)
userlogin.place(x=8, y=145)
guestlabel = Label(homepageframe, text="Guest user", fg='black', bg='white',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), )
guestlabel.place(x=10, y=220)
guestuser = Button(homepageframe, width='31', border='0', text='---> Click to use the system', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID, command=GuestPage)
guestuser.place(x=8, y=255)

app.mainloop()
