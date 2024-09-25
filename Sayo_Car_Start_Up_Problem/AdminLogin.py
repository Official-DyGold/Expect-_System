
from tkinter import *
import tkinter.messagebox as MessageBox
import os
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

app = Tk()
app.title("Car Start Up Diagnosis System")
app.geometry('500x550')
app.configure(border="1", background='darkblue')


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sayo_car_start_up"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        MessageBox.showerror("Error", e)
        return None

def adminlogin():
    admin_username = adminusername.get()
    admin_password = adminpassword.get()

    conn = connect_to_db()
    cursor = conn.cursor()

    if (admin_username == "" or
            admin_password == ""):
        loginlabel.config(text="All Fields are required", fg='red', font=("bold"))
    elif (admin_username == "Username" or
        admin_password == "Password"):
        loginlabel.config(text="All Fields are required", fg='red', font=("bold"))
    elif (admin_username == "" or
        admin_password == "Password"):
        loginlabel.config(text="All Fields are required", fg='red', font=("bold"))
    elif (admin_username == "Username" or
        admin_password == ""):
        loginlabel.config(text="All Fields are required", fg='red', font=("bold"))
    else:
        try:
            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s",
                           (admin_username, admin_password))
            user = cursor.fetchone()

            if user:
                app.destroy()
                os.system('AdminHomePage.py')
            else:
                loginlabel.config(text="Username or Password incorrect", fg='red', font=("bold"))
        except Error as e:
            MessageBox.showerror("Error", e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def backbutton():
    app.destroy()

def load_Admin_Icon(image_path):
    image = Image.open(image_path)
    image = image.resize((140, 140))
    background_image = ImageTk.PhotoImage(image)

    canvas = Canvas(adminframe, width=140, height=140, bg="white")
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.image = background_image

    return canvas


image_path = "background\\icon.png"


homelabel = Label(app, text="ADMIN LOGIN SECTION", fg='white', bg='darkblue',
                  font=("Microsoft Yahei Ui Light", 20, 'bold'))
homelabel.place(x=90, y=30)

adminframe = Frame(app, width='400', height='450', background='white')
adminframe.place(x=50, y=80)
adminframeheader = Frame(adminframe, width='390', height='40', background='darkblue')
adminframeheader.place(x=5, y=6)
adminlabel = Label(adminframeheader, text="Admin Login", fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 15, 'bold'))
adminlabel.place(x=3, y=3)
canvas = load_Admin_Icon(image_path).place(x=130, y=75)
loginlabel = Label(adminframe, text="*Please Keg in your valid username and password", fg='darkblue', bg='white',
                   font=("Microsoft Yahei Ui Light", 8))
loginlabel.place(x=30, y=230)


def on_enter(e):
    loginlabel.config(text="*Please Keg in your valid username and password", fg='darkblue', font=("Microsoft Yahei Ui Light", 8))
    if adminusername.get() == 'Username':
        adminusername.delete(0, 'end')


def on_leave(e):
    if adminusername.get() == '':
        adminusername.insert(0, 'Username')


adminusername = Entry(adminframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11))
adminusername.place(x=30, y=265)
adminusername.insert(0, 'Username')
adminusername.bind("<FocusIn>", on_enter)
adminusername.bind("<FocusOut>", on_leave)
Frame(adminframe, width=340, height=2, bg='darkblue').place(x=30, y=300)

def on_enter(e):
    loginlabel.config(text="*Please Keg in your valid username and password", fg='darkblue',
                      font=("Microsoft Yahei Ui Light", 8))
    if adminpassword.get() == 'Password':
        adminpassword.delete(0, 'end')


def on_leave(e):
    if adminpassword.get() == '':
        adminpassword.insert(0, 'Password')


adminpassword = Entry(adminframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11), show='*')
adminpassword.place(x=30, y=330)
adminpassword.insert(0, 'Password')
adminpassword.bind("<FocusIn>", on_enter)
adminpassword.bind("<FocusOut>", on_leave)
Frame(adminframe, width=340, height=2, bg='darkblue').place(x=30, y=365)
adminlogin = Button(adminframe, width='37', border='0', text='Admin Login', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), command=adminlogin, cursor="hand2", relief=SOLID)
adminlogin.place(x=30, y=385)
back = Button(adminframeheader,  border='0', text='Back Homepage', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), command=backbutton, cursor="hand2", relief=SOLID)
back.place(x=260, y=5)

app.mainloop()
