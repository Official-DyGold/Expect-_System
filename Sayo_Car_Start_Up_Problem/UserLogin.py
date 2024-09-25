from tkinter import *
import os
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox as MessageBox

app = Tk()
app.title("Car Start Up Diagnosis System")
app.geometry('500x550')
app.configure(border="1", background='white')


def backbutton():
    app.destroy()


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
        MessageBox.showerror("Error", str(e))
        return None


def adminlogin():
    admin_username = adminusername.get()
    admin_password = adminpassword.get()
    conn = connect_to_db()
    cursor = conn.cursor()

    if (admin_username == "" or
            admin_password == ""):
        loginlabel.config(text="All Fields are required", fg='red', font="bold")
    elif (admin_username == "Username" or
          admin_password == "Password"):
        loginlabel.config(text="All Fields are required", fg='red', font="bold")
    elif (admin_username == "" or
          admin_password == "Password"):
        loginlabel.config(text="All Fields are required", fg='red', font="bold")
    elif (admin_username == "Username" or
          admin_password == ""):
        loginlabel.config(text="All Fields are required", fg='red', font="bold")

    else:
        try:
            cursor.execute("SELECT username, password FROM users WHERE username = %s AND password = %s",
                           (admin_username, admin_password))
            user = cursor.fetchone()

            if user:
                with open("user_details.txt", "w") as file:
                    file.write(admin_username)

                app.destroy()
                os.system('UserHomePage.py')
            else:
                loginlabel.config(text="Username or Password incorrect", fg='red', font="bold")
        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def load_Admin_Icon(image_path):
    image = Image.open(image_path)
    image = image.resize((140, 140))
    background_image = ImageTk.PhotoImage(image)

    canvas = Canvas(adminframe, width=140, height=140)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.image = background_image

    return canvas


image_path = "background\\icon.png"

homelabel = Label(app, text="USER LOGIN SECTION", fg='darkblue', bg='white',
                  font=("Microsoft Yahei Ui Light", 20, 'bold'))
homelabel.place(x=90, y=30)

adminframe = Frame(app, width='400', height='450', background='white')
adminframe.place(x=50, y=80)
adminframeheader = Frame(adminframe, width='390', height='40', background='darkblue')
adminframeheader.place(x=5, y=6)
adminlabel = Label(adminframeheader, text="User Login", fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 15, 'bold'))
adminlabel.place(x=3, y=3)
load_Admin_Icon(image_path).place(x=130, y=75)
loginlabel = Label(adminframe, text="*Please Key in your valid username and password", fg='darkblue', bg='white',
                   font=("Microsoft Yahei Ui Light", 8))
loginlabel.place(x=30, y=230)


def on_enter(e):
    loginlabel.config(text="*Please Keg in your valid username and password", fg='darkblue',
                      font=("Microsoft Yahei Ui Light", 8))
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


adminpassword = Entry(adminframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11),
                      show='*')
adminpassword.place(x=30, y=330)
adminpassword.insert(0, 'Password')
adminpassword.bind("<FocusIn>", on_enter)
adminpassword.bind("<FocusOut>", on_leave)
Frame(adminframe, width=340, height=2, bg='darkblue').place(x=30, y=365)
adminlogin = Button(adminframe, width='18', border='0', text='User Login', fg='white', bg='darkblue',
                    font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID, command=adminlogin)
adminlogin.place(x=30, y=385)


def switch1():
    adminframe.place_forget()
    userframe.place(x=50, y=80)


user_register = Button(adminframe, width='18', border='0', text='Register', fg='white', bg='darkblue',
                       font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID, command=switch1)
user_register.place(x=200, y=385)
back = Button(adminframeheader, border='0', text='Back Homepage', fg='white', bg='darkblue',
              font=("Microsoft Yahei Ui Light", 10, 'bold'), command=backbutton, cursor="hand2", relief=SOLID)
back.place(x=260, y=5)

#register
def saveuser():
    user_name = userusername.get()
    pas_word = userpassword.get()

    if user_name == "" or user_name == 'Username' or pas_word == "" or pas_word == 'Password':
        userlabel.config(text="All Fields are required", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='white')
    else:
        password_length = len(pas_word)
        if userpassword.get() == userusername.get():
            userlabel.config(text="Username and Password can not be the same", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='white')
        elif password_length > 6:
            if userpassword.get() != userconpassword.get():
                userlabel.config(text="Password and Confirm Password does not match", fg='red',
                                  font=("Microsoft Yahei Ui Light", 12), bg='white')
            else:
                conn = connect_to_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM users WHERE username='" + userusername.get() + "'")
                    rows = cursor.fetchall()
                    if rows:
                        userlabel.config(text="User already exist", fg='red',
                                          font=("Microsoft Yahei Ui Light", 12), bg='white')

                        userusername.delete(0, END)
                        userpassword.delete(0, END)
                        userconpassword.delete(0, END)
                        userusername.insert(0, 'Username')
                        userpassword.insert(0, 'Password')
                        userconpassword.insert(0, 'Password')
                    else:
                        cursor.execute(
                            "INSERT INTO users (username, password) VALUES (%s, %s)", (user_name, pas_word))
                        conn.commit()

                        userlabel.config(text="User saved successfully, Login on the login page", fg='green',
                                          font=("Microsoft Yahei Ui Light", 12), bg='white')

                        userusername.delete(0, END)
                        userpassword.delete(0, END)
                        userconpassword.delete(0, END)
                        userusername.insert(0, 'Username')
                        userpassword.insert(0, 'Password')
                        userconpassword.insert(0, 'Password')

                except Error as e:
                    MessageBox.showerror("Error", str(e))
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

        else:
            userlabel.config(text="Password most be greater than 6", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='white')


userframe = Frame(app, width='400', height='450', background='white')

userframeheader = Frame(userframe, width='390', height='40', background='darkblue')
canvas2 = userframeheader.place(x=5, y=6)
userlabel = Label(userframeheader, text="User Registration", fg='white', bg='darkblue',
                  font=("Microsoft Yahei Ui Light", 15, 'bold'))
userlabel.place(x=3, y=3)
userlabel = Label(userframe, text="*Provide your username and password to register on this system", fg='darkblue',
                  bg='white', font=("Microsoft Yahei Ui Light", 8))
userlabel.place(x=30, y=150)


def on_enter(e):
    userlabel.config(text="*Provide your username and password to register on this system", fg='darkblue',
                      font=("Microsoft Yahei Ui Light", 8))
    if userusername.get() == 'Username':
        userusername.delete(0, 'end')


def on_leave(e):
    if userusername.get() == '':
        userusername.insert(0, 'Username')


userusername = Entry(userframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11))
userusername.place(x=30, y=185)
userusername.insert(0, 'Username')
userusername.bind("<FocusIn>", on_enter)
userusername.bind("<FocusOut>", on_leave)
Frame(userframe, width=340, height=2, bg='darkblue').place(x=30, y=210)


def on_enter(e):
    userlabel.config(text="*Provide your username and password to register on this system", fg='darkblue',
                      font=("Microsoft Yahei Ui Light", 8))
    if userpassword.get() == 'Password':
        userpassword.delete(0, 'end')


def on_leave(e):
    if userpassword.get() == '':
        userpassword.insert(0, 'Password')


userpassword = Entry(userframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11),
                     show='*')
userpassword.place(x=30, y=245)
userpassword.insert(0, 'Password')
userpassword.bind("<FocusIn>", on_enter)
userpassword.bind("<FocusOut>", on_leave)
Frame(userframe, width=340, height=2, bg='darkblue').place(x=30, y=270)

def on_enter(e):
    userlabel.config(text="*Provide your username and password to register on this system", fg='darkblue',
                      font=("Microsoft Yahei Ui Light", 8))
    if userconpassword.get() == 'Password':
        userconpassword.delete(0, 'end')


def on_leave(e):
    if userconpassword.get() == '':
        userconpassword.insert(0, 'Password')


userconpassword = Entry(userframe, width=42, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11),
                     show='*')
userconpassword.place(x=30, y=305)
userconpassword.insert(0, 'Password')
userconpassword.bind("<FocusIn>", on_enter)
userconpassword.bind("<FocusOut>", on_leave)
Frame(userframe, width=340, height=2, bg='darkblue').place(x=30, y=330)


def switch2():
    adminframe.place(x=50, y=80)
    userframe.place_forget()


userlogin = Button(userframe, width='18', border='0', text='Back to Login', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID, command=switch2)
userlogin.place(x=30, y=385)
user_register = Button(userframe, width='18', border='0', text='Register', fg='white', bg='darkblue',
                       font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID, command=saveuser)
user_register.place(x=200, y=385)
userback = Button(userframeheader, border='0', text='Back Homepage', fg='white', bg='darkblue',
                  font=("Microsoft Yahei Ui Light", 10, 'bold'), command=backbutton, cursor="hand2", relief=SOLID)
userback.place(x=260, y=5)

app.mainloop()
