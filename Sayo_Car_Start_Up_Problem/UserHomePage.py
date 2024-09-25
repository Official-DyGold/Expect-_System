import string
import random
from tkinter import *
import tkinter.messagebox as MessageBox
from tkinter import ttk

import mysql.connector
from mysql.connector import Error

app = Tk()
app.title("Car Start Up Diagnosis System")
app.geometry('900x500')
app.configure(border="1", background='white')


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


def user():
    try:
        with open("user_details.txt", "r") as file:
            user_name = file.read().strip()
            return user_name
    except FileNotFoundError:
        return []


def logout():
    reply = MessageBox.askyesno('User Logout', 'Are you sure you want to logout')
    if reply:
        app.destroy()


user_username = user()
adminframeheader = Frame(app, width='880', height='40', background='darkblue')
adminframeheader.place(x=10, y=10)
timeofuse = Label(adminframeheader, text='Welcome ' + user_username, font=('Microsoft Yahei Ui Light', 20), fg='white',
                  bg='darkblue')
timeofuse.place(x=20, y=2)
adminframe = Frame(app, width='880', height='420', background='darkblue')
adminframe.place(x=10, y=70)


def fetch_homepage():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data WHERE users = %s", (user_username,))
        total_rows = cursor.fetchone()[0]
        time_of_use.config(text=total_rows)
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data WHERE users = %s AND response = 'Satisfied'",
                       (user_username,))
        total_rows = cursor.fetchone()[0]
        time_satisfied.config(text=total_rows)
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data WHERE users = %s AND response = 'Not Satisfied'",
                       (user_username,))
        total_rows = cursor.fetchone()[0]
        time_not_satisfied.config(text=total_rows)
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def switch1():
    adminhomeframe.place(x=250, y=10)
    adminhomeconnectorframe.place(x=230, y=37)
    admincarfaultframe.place_forget()
    admincarfaultconnectorframe.place_forget()
    manageuserframe.place_forget()
    manageruserconnectorframe.place_forget()
    dataframe.place_forget()
    dataconnectorframe.place_forget()
    fetch_homepage()


adminhomeconnectorframe = Frame(adminframe, width='40', height='20', background='white')
adminhomeconnectorframe.place(x=230, y=37)
adminhome = Button(adminframe, width='20', border='0', text='Home Page', fg='darkblue', bg='white',
                   font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                   activebackground='darkblue', activeforeground='white', command=switch1)
adminhome.place(x=30, y=30)
adminhomeframe = Frame(adminframe, width='620', height='400', background='white')
adminhomeframe.place(x=250, y=10)
timeofuse = Label(adminhomeframe, text='Time of Use', font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
timeofuse.place(x=100, y=100)
time_of_use = Label(adminhomeframe, font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
time_of_use.place(x=150, y=140)
timesatisfied = Label(adminhomeframe, text='Time Satisfied', font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
timesatisfied.place(x=350, y=100)
time_satisfied = Label(adminhomeframe,  font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
time_satisfied.place(x=420, y=140)
timenotsatisfied = Label(adminhomeframe, text='Time Not Satisfied', font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
timenotsatisfied.place(x=190, y=240)
time_not_satisfied = Label(adminhomeframe,  font=('Microsoft Yahei Ui Light', 20), fg='black',
                  bg='white')
time_not_satisfied.place(x=290, y=280)

index_use = 0


def fetct_car_problem_details():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM car_fault")
        rows_now = cursor.fetchall()
        fault.config(state='normal')
        faultsolution.config(state='normal')
        userchat.config(state='normal')

        fault.delete("1.0", END)
        faultsolution.delete("1.0", END)
        userchat.delete("1.0", END)
        global index
        index = 1

        row = rows_now[index_use]
        faultidreturn = row[1]
        faultnamereturn = row[2]
        faultcausereture = row[3]
        faultsolutionreturn = row[4]

        faultid.insert(END, f"{faultidreturn}")
        faultname.insert(END, f"Fault Name: {faultnamereturn}")
        fault.insert(END, f"Fault Problem: {faultcausereture}")
        faultsolution.insert(END, f"Fault Solution: {faultsolutionreturn}")
        userchat.insert(END,
                        f"Fault ID: {faultidreturn}\nFault Name: {faultnamereturn}\nFault Problem: {faultcausereture}\nFault Solution: {faultsolutionreturn}\n")

        fault.config(state='disabled')
        faultsolution.config(state='disabled')
        userchat.config(state='disabled')

        userreply.config(text='Please click on Yes if the solution was able to start up your car else '
                              'click no', font=('Microsoft Yahei Ui Light', 10), fg='black',
                         bg='white', wraplength='280', justify='left')

        return index
    except Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def display_data():
    fault.config(state='normal')
    faultsolution.config(state='normal')
    userchat.config(state='normal')
    conn = connect_to_db()
    cursor = conn.cursor()

    global index

    if not userchat.get("1.0", END).strip():
        userreply.config(text='Please click on Start Diagnosis Button', font=('Microsoft Yahei Ui Light', 10), fg='red',
                         bg='white', wraplength='280', justify='left')
        check_state2.set(0)
    else:
        cursor.execute("SELECT * FROM car_fault")
        rows = cursor.fetchall()

        if index < len(rows):
            fault.delete("1.0", END)
            faultsolution.delete("1.0", END)

            row = rows[index]
            faultidreturn1 = row[1]
            faultnamereturn1 = row[2]
            faultcausereture1 = row[3]
            faultsolutionreturn1 = row[4]

            faultid.insert(END, f"{faultidreturn1}")
            faultname.insert(END, f"Fault Name: {faultnamereturn1}")
            fault.insert(END, f"Fault Problem: {faultcausereture1}")
            faultsolution.insert(END, f"Fault Solution: {faultsolutionreturn1}")
            userchat.insert(END,
                            f"\nFault ID: {faultidreturn1}\nFault Name: {faultnamereturn1}\nFault Problem: {faultcausereture1}\n\nFault Solution: {faultsolutionreturn1}\n")

            index += 1
            fault.config(state='disabled')
            faultsolution.config(state='disabled')
            userchat.config(state='disabled')
            check_state2.set(0)
        else:
            fault.delete("1.0", END)
            faultsolution.delete("1.0", END)
            fault.insert(END, f"Expect needed")
            faultsolution.insert(END,
                                 f"Please contact an expect in this field for further diagnosis to get your car start up")
            userchat.insert(END,
                            f"\nPlease contact an expect in this field for further diagnosis to get your car start up")
            fault.config(state='disabled')
            faultsolution.config(state='disabled')
            userchat.config(state='disabled')


index = 1


def switch2():
    adminhomeframe.place_forget()
    adminhomeconnectorframe.place_forget()
    admincarfaultframe.place(x=250, y=10)
    admincarfaultconnectorframe.place(x=230, y=127)
    manageuserframe.place_forget()
    manageruserconnectorframe.place_forget()
    dataframe.place_forget()
    dataconnectorframe.place_forget()


admincarfaultconnectorframe = Frame(adminframe, width='40', height='20', background='white')
admincarfault = Button(adminframe, width='20', border='0', text='Car Fault', fg='darkblue', bg='white',
                       font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                       activebackground='darkblue', activeforeground='white', command=switch2)
admincarfault.place(x=30, y=120)

admincarfaultframe = Frame(adminframe, width='620', height='400', background='white')
faultid = Text()
faultname = Text()
fault = Text(admincarfaultframe, width=30, height=3, wrap=WORD, bg='gray', fg='white',
             font=('Microsoft Yahei Ui Light', 11, 'bold'), cursor='hand2')
fault.tag_configure("center", justify="left")
fault.place(x=20, y=20)
scrollbar = Scrollbar(admincarfaultframe, command=fault.yview)
scrollbar.place(x=290, y=20, height=fault.winfo_reqheight())
fault.config(yscrollcommand=scrollbar.set)

faultsolution = Text(admincarfaultframe, width=30, height=5, wrap=WORD, bg='gray', fg='white',
                     font=('Microsoft Yahei Ui Light', 11, 'bold'), cursor='hand2')
faultsolution.tag_configure("center", justify="left")
faultsolution.place(x=20, y=100)
scrollbar = Scrollbar(admincarfaultframe, command=faultsolution.yview)
scrollbar.place(x=290, y=100, height=faultsolution.winfo_reqheight())
faultsolution.config(yscrollcommand=scrollbar.set)

userchat = Text(admincarfaultframe, width=30, height=15, wrap=WORD, bg='gray', fg='white',
                font=('Microsoft Yahei Ui Light', 11, 'bold'), cursor='hand2')
userchat.tag_configure("left", justify="left")
userchat.tag_configure("right", justify="right")
userchat.place(x=325, y=20)
scrollbar = Scrollbar(admincarfaultframe, command=userchat.yview)
scrollbar.place(x=600, y=20, height=userchat.winfo_reqheight())
userchat.config(yscrollcommand=scrollbar.set)

userreply = Label(admincarfaultframe, text='Please click on Yes if the solution was able to start up your car else '
                                           'click no', font=('Microsoft Yahei Ui Light', 10), fg='black', bg='white',
                  wraplength='280', justify='left')
userreply.place(x=20, y=240)
replylooping = Label(admincarfaultframe, text='Yes', font=('Microsoft Yahei Ui Light', 10), fg='black', bg='white')
replylooping.place(x=20, y=285)

check_state1 = IntVar()


def collect_check1_value():
    faultresponse = check_state1.get()
    if faultresponse == 1:
        conn = connect_to_db()
        cursor = conn.cursor()

        user_username = user()
        try:

            if userchat.get('1.0', END).strip() == "":
                userreply.config(text='No diagnosis in process', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state1.set(0)
            elif (faultid.get('1.0', END).strip() and faultname.get('1.0', END).strip() and
                  fault.get('1.0', END).strip() and faultsolution.get('1.0', END).strip() != ""):

                letter = faultid.get('1.0', END).strip()
                number = ''.join(random.choices(string.digits, k=3))
                randomid = letter + '-' + number
                responseid.delete('1.0', END)
                responseid.insert(END, randomid)

                cursor.execute(
                    "INSERT INTO user_rersponse_data (responseid, faultid, faultname, faultcause, faultsolution, users) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (responseid.get('1.0', END).strip(), faultid.get('1.0', END).strip(),
                     faultname.get('1.0', END).strip(),
                     fault.get('1.0', END).strip(), faultsolution.get('1.0', END).strip(), user_username))
                conn.commit()

                userreply.config(text='Car Fixed: Thank you for using this system',
                                 font=('Microsoft Yahei Ui Light', 10),
                                 fg='green', bg='white', wraplength='280', justify='left')
                check_state1.set(0)
                userchat.config(state='normal')
                userchat.insert(END, f"{user_username}: Car Fixed\n", "right")
                userchat.config(state='disabled')
            else:
                userreply.config(text='Unable to verify response', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state1.set(0)

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


responseid = Text()
checkedyes = Checkbutton(admincarfaultframe, bg='white', variable=check_state1, command=collect_check1_value)
checkedyes.place(x=60, y=285)

check_state2 = IntVar()
replylooping1 = Label(admincarfaultframe, text='No', font=('Microsoft Yahei Ui Light', 10), fg='black', bg='white')
replylooping1.place(x=100, y=285)
checkedno = Checkbutton(admincarfaultframe, bg='white', variable=check_state2, command=display_data)
checkedno.place(x=130, y=285)

start = Button(admincarfaultframe, width='27', border='0', text='Start Diagnosis', fg='darkblue', bg='white',
               font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
               activebackground='darkblue', activeforeground='white', command=fetct_car_problem_details)
start.place(x=18, y=330)

userreply2 = Label(admincarfaultframe, text='Please let us no whether you are '
                                            'satisfied', font=('Microsoft Yahei Ui Light', 10), fg='black',
                   bg='white', wraplength='280', justify='left')
userreply2.place(x=320, y=330)
reply = Label(admincarfaultframe, text='Yes', font=('Microsoft Yahei Ui Light', 10), fg='black', bg='white')
reply.place(x=320, y=365)

check_state3 = IntVar()


def collect_check2_value():
    userresponse = check_state3.get()
    if userresponse == 1:
        conn = connect_to_db()
        cursor = conn.cursor()
        user_username = user()
        response_reply = "Satisfied"

        try:
            if responseid.get('1.0', END).strip() == "":
                userreply.config(text='No diagnosis in process', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state2.set(0)
            elif (faultid.get('1.0', END).strip() and faultname.get('1.0', END).strip() and
                  fault.get('1.0', END).strip() and faultsolution.get('1.0', END).strip() != ""):
                cursor.execute(
                    "Update user_rersponse_data SET response = %s WHERE responseid = %s",
                    (response_reply, responseid.get('1.0', END).strip()))
                conn.commit()
                userreply.config(text='Satisfied', font=('Microsoft Yahei Ui Light', 10),
                                 fg='green', bg='white', wraplength='280', justify='left')
                check_state3.set(0)
                userchat.config(state='normal')
                userchat.insert(END, f"{user_username}: Satisfied\n", "right")
                userchat.config(state='disabled')

            else:
                userreply.config(text='Unable to verify response', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state3.set(0)
        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


checkedyes2 = Checkbutton(admincarfaultframe, bg='white', variable=check_state3, command=collect_check2_value)
checkedyes2.place(x=350, y=365)

check_state4 = IntVar()
reply1 = Label(admincarfaultframe, text='No', font=('Microsoft Yahei Ui Light', 10), fg='black', bg='white')
reply1.place(x=380, y=365)


def collect_check4_value():
    course2name = check_state4.get()
    if course2name == 1:
        conn = connect_to_db()
        cursor = conn.cursor()
        user_username = user()
        response_reply = "Not Satisfied"

        try:
            if responseid.get('1.0', END).strip() == "":
                userreply.config(text='No diagnosis in process', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state2.set(0)
            elif (faultid.get('1.0', END).strip() and faultname.get('1.0', END).strip() and
                  fault.get('1.0', END).strip() and faultsolution.get('1.0', END).strip() != ""):
                cursor.execute(
                    "Update user_rersponse_data SET response = %s WHERE responseid = %s",
                    (response_reply, responseid.get('1.0', END).strip()))
                conn.commit()
                userreply.config(text='Not Satisfied', font=('Microsoft Yahei Ui Light', 10),
                                 fg='green', bg='white', wraplength='280', justify='left')
                check_state3.set(0)
                userchat.config(state='normal')
                userchat.insert(END, f"{user_username}: Not Satisfied\n", "right")
                userchat.config(state='disabled')

            else:
                userreply.config(text='Unable to verify response', font=('Microsoft Yahei Ui Light', 10),
                                 fg='red', bg='white', wraplength='280', justify='left')
                check_state4.set(0)
        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


checkedno2 = Checkbutton(admincarfaultframe, bg='white', variable=check_state4, command=collect_check4_value)
checkedno2.place(x=410, y=365)


def restart():
    fault.config(state='normal')
    faultsolution.config(state='normal')
    userchat.config(state='normal')
    global index

    index = 1

    faultid.delete('1.0', END)
    faultname.delete('1.0', END)
    fault.delete('1.0', END)
    faultsolution.delete('1.0', END)
    userchat.delete('1.0', END)
    responseid.delete('1.0', END)

    fault.config(state='disabled')
    faultsolution.config(state='disabled')
    userchat.config(state='disabled')
    userreply.config(text='Please click on Yes if the solution was able to start up your car else '
                          'click no', font=('Microsoft Yahei Ui Light', 10), fg='black',
                     bg='white', wraplength='280', justify='left')
    return index


Submit = Button(admincarfaultframe, width='10', border='0', text='Restart', fg='darkblue', bg='white',
                font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                activebackground='darkblue', activeforeground='white', command=restart)
Submit.place(x=450, y=362)


def errorckeck():
    Password = password.get()
    password_length = len(Password)
    if password.get() == username.get():
        errorlabel.config(text="Username and Password can not be the same", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)
    elif password_length > 6:
        if password.get() != conpassword.get():
            errorlabel.config(text="Password and Confirm Password does not match", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
            errorlabel.place(x=60, y=220)
        else:
            errorlabel.place_forget()

    else:
        errorlabel.config(text="Password most be greater than 6", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)

    app.after(4000, errorckeck)


def searchuser():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username= %s", (user_username,))
        rows = cursor.fetchall()

        if rows:
            modelversion.delete(0, 'end')
            carowner.delete(0, 'end')
            platenumber.delete(0, 'end')
            email.delete(0, 'end')
            for row in rows:
                modelversion.insert(0, row[2])
                carowner.insert(0, row[3])
                platenumber.insert(0, row[4])
                email.insert(0, row[5])
        else:
            errorlabel.config(text="User does not exist", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='white')
            errorlabel.place(x=60, y=220)

    except Error as e:
        MessageBox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def updateuser():
    model_version = modelversion.get()
    car_owner = carowner.get()
    plate_number = platenumber.get()
    e_mail = email.get()
    user_name = username.get()
    pas_word = password.get()

    if (model_version == "" or model_version == "Car model" or car_owner == "" or car_owner == "Car owner's name" or
            plate_number == '' or plate_number == 'Car Plate Number' or e_mail == "" or
            e_mail == 'Email' or user_name == "" or user_name == 'Username' or pas_word == "" or
            pas_word == 'Password'):
        errorlabel.config(text="All Fields are required", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='white')
        errorlabel.place(x=60, y=220)
    else:
        password_length = len(pas_word)
        if password.get() == username.get():
            errorlabel.config(text="Username and Password can not be the same", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='white')
            errorlabel.place(x=60, y=220)
        elif password_length > 6:
            if password.get() != conpassword.get():
                errorlabel.config(text="Password and Confirm Password does not match", fg='red',
                                  font=("Microsoft Yahei Ui Light", 12), bg='white')
                errorlabel.place(x=60, y=220)
            else:
                errorlabel.place_forget()
                conn = connect_to_db()
                cursor = conn.cursor()
                try:

                    cursor.execute(
                        ("Update users SET carmodel = %s, carowner = %s, platenumber = %s, email = %s, "
                         "password = %s WHERE username = %s"), (model_version, car_owner, plate_number, e_mail,
                                                               pas_word, user_name))
                    conn.commit()

                    errorlabel.config(text="User details Updated", fg='green',
                                      font=("Microsoft Yahei Ui Light", 12), bg='white')
                    errorlabel.place(x=60, y=220)

                    modelversion.delete(0, 'end')
                    carowner.delete(0, 'end')
                    platenumber.delete(0, 'end')
                    email.delete(0, 'end')
                    password.delete(0, 'end')
                    conpassword.delete(0, 'end')
                    modelversion.set('Car Model')
                    carowner.insert(0, "Car owner's name")
                    platenumber.insert(0, 'Car Plate Number')
                    email.insert(0, 'Email')
                    password.insert(0, 'Password')
                    conpassword.insert(0, 'Password')

                except Error as e:
                    MessageBox.showerror("Error", str(e))
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

        else:
            errorlabel.config(text="Password most be greater than 6", fg='red',
                              font=("Microsoft Yahei Ui Light", 12), bg='white')
            errorlabel.place(x=60, y=220)


def switch3():
    adminhomeframe.place_forget()
    adminhomeconnectorframe.place_forget()
    admincarfaultframe.place_forget()
    admincarfaultconnectorframe.place_forget()
    manageuserframe.place(x=250, y=10)
    manageruserconnectorframe.place(x=230, y=217)
    dataframe.place_forget()
    dataconnectorframe.place_forget()


manageruserconnectorframe = Frame(adminframe, width='40', height='20', background='white')
manageuser = Button(adminframe, width='20', border='0', text='Manage User', fg='darkblue', bg='white',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='darkblue', activeforeground='white', command=switch3)
manageuser.place(x=30, y=210)
manageuserframe = Frame(adminframe, width='620', height='400', background='white')

carmodel = Entry(manageuserframe, width=29, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11))
carmodel.place(x=60, y=40)
carmodel.insert(0, 'Camry')
carmodel.config(state=DISABLED)
carmodelframe = Frame(manageuserframe, width=234, height=2, bg='gray')
carmodelframe.place(x=60, y=65)

modelversion = ttk.Combobox(manageuserframe, width=26, font=('Microsoft Yahei Ui Light', 10, 'bold'))
modelversion.place(x=330, y=40)
modelversion.set('Car model')
modelversion['values'] = ('xv 30', 'xv 40', 'xv 50', 'xv 70')


def on_enter(e):
    Carownerframe.config(bg='white')
    if carowner.get() == "Car owner's name":
        carowner.delete(0, 'end')


def on_leave(e):
    Carownerframe.config(bg='gray')
    if carowner.get() == '':
        carowner.insert(0, "Car owner's name")


carowner = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                 font=('Microsoft Yahei Ui Light', 11))
carowner.place(x=60, y=85)
carowner.insert(0, "Car owner's name")
carowner.bind("<FocusIn>", on_enter)
carowner.bind("<FocusOut>", on_leave)
Carownerframe = Frame(manageuserframe, width=234, height=2, bg='gray')
Carownerframe.place(x=60, y=110)


def on_enter(e):
    platenumberframe.config(bg='white')
    if platenumber.get() == "Car Plate Number":
        platenumber.delete(0, 'end')


def on_leave(e):
    platenumberframe.config(bg='gray')
    if platenumber.get() == '':
        platenumber.insert(0, "Car Plate Number")


platenumber = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                    font=('Microsoft Yahei Ui Light', 11))
platenumber.place(x=330, y=85)
platenumber.insert(0, "Car Plate Number")
platenumber.bind("<FocusIn>", on_enter)
platenumber.bind("<FocusOut>", on_leave)
platenumberframe = Frame(manageuserframe, width=234, height=2, bg='gray')
platenumberframe.place(x=330, y=110)


def on_enter(e):
    emailframe.config(bg='white')
    if email.get() == "Email":
        email.delete(0, 'end')


def on_leave(e):
    emailframe.config(bg='gray')
    if email.get() == '':
        email.insert(0, "Email")


email = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
              font=('Microsoft Yahei Ui Light', 11))
email.place(x=60, y=135)
email.insert(0, "Email")
email.bind("<FocusIn>", on_enter)
email.bind("<FocusOut>", on_leave)
emailframe = Frame(manageuserframe, width=234, height=2, bg='gray')
emailframe.place(x=60, y=160)


username = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                 font=('Microsoft Yahei Ui Light', 11))
username.place(x=330, y=135)
username.insert(0, user_username)
usernameframe = Frame(manageuserframe, width=234, height=2, bg='gray')
usernameframe.place(x=330, y=160)


def on_enter(e):
    passwordframe.config(bg='white')
    if password.get() == "Password":
        password.delete(0, 'end')


def on_leave(e):
    passwordframe.config(bg='gray')
    if password.get() == '':
        password.insert(0, "Password")


password = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                 font=('Microsoft Yahei Ui Light', 11), show='*')
password.place(x=60, y=185)
password.insert(0, "Password")
password.bind("<FocusIn>", on_enter)
password.bind("<FocusOut>", on_leave)
passwordframe = Frame(manageuserframe, width=234, height=2, bg='gray')
passwordframe.place(x=60, y=210)


def on_enter(e):
    conpasswordframe.config(bg='white')
    if conpassword.get() == "Password":
        conpassword.delete(0, 'end')


def on_leave(e):
    conpasswordframe.config(bg='gray')
    if conpassword.get() == '':
        conpassword.insert(0, "Password")


conpassword = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                    font=('Microsoft Yahei Ui Light', 11), show='*')
conpassword.place(x=330, y=185)
conpassword.insert(0, "Password")
conpassword.bind("<FocusIn>", on_enter)
conpassword.bind("<FocusOut>", on_leave)
conpasswordframe = Frame(manageuserframe, width=234, height=2, bg='gray')
conpasswordframe.place(x=330, y=210)

errorlabel = Label(manageuserframe, text="", fg='darkblue', bg='white',
                   font=("Microsoft Yahei Ui Light", 8))


updateuser = Button(manageuserframe, width='50', border='0', text='Update User', fg='white', bg='gray',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='white', activeforeground='darkblue', command=updateuser)
updateuser.place(x=60, y=260)

searchuser = Button(manageuserframe, width='50', border='0', text='Search User', fg='white', bg='gray',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='white', activeforeground='darkblue', command=searchuser)
searchuser.place(x=60, y=330)


def fetch_user_history(user_username):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM user_rersponse_data WHERE users = %s ", (user_username,))
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def wrap_text(text, width):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= width:
            line += (word + " ")
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines


def display_user_history():
    history = fetch_user_history(user_username)
    serial_number = 1
    listbox.delete(0, END)

    for record in history:
        listbox.insert(END, f"Serial Number: {serial_number}")

        wrapped_fault_cause = wrap_text(f"{record[4]}", width=65)
        for line in wrapped_fault_cause:
            listbox.insert(END, line)

        wrapped_fault_solution = wrap_text(f"{record[5]}", width=65)
        for line in wrapped_fault_solution:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"Your Responses: {record[7]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        listbox.insert(END, "")
        serial_number += 1

def switch4():
    adminhomeframe.place_forget()
    adminhomeconnectorframe.place_forget()
    admincarfaultframe.place_forget()
    admincarfaultconnectorframe.place_forget()
    manageuserframe.place_forget()
    manageruserconnectorframe.place_forget()
    dataconnectorframe.place(x=230, y=307)
    dataframe.place(x=250, y=10)
    display_user_history()


dataconnectorframe = Frame(adminframe, width='40', height='20', background='white')
data = Button(adminframe, width='20', border='0', text='User Report', fg='darkblue', bg='white',
              font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
              activebackground='darkblue', activeforeground='white', command=switch4)
data.place(x=30, y=300)
dataframe = Frame(adminframe, width='620', height='400', background='white')
listbox = Listbox(dataframe, width=54, height=14, bg="gray", fg='white', font=("Microsoft Yahei Ui Light", 14))
listbox.place(x=10, y=10)
scrollbar = Scrollbar(dataframe, command=listbox.yview)
scrollbar.place(x=590, y=10, height=listbox.winfo_reqheight())
listbox.config(yscrollcommand=scrollbar.set)

logout = Button(adminframe, width='20', border='0', text='Logout', fg='darkblue', bg='white',
                font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                activebackground='red', activeforeground='white', command=logout)
logout.place(x=30, y=370)

fault.config(state='disabled')
faultsolution.config(state='disabled')
userchat.config(state='disabled')

fetch_homepage()
display_user_history()
app.mainloop()
