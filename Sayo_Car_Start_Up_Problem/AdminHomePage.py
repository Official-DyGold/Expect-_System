import random
import string
from tkinter import *
import tkinter.messagebox as MessageBox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

app = Tk()
app.title("Car Start Up Diagnosis System")
app.geometry('900x500')
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
        MessageBox.showerror("Error", str(e))
        return None


def logout():
    reply = MessageBox.askyesno('Admin Logout', 'Are you sure you want to logout')
    if reply:
        app.destroy()


def fetch_homepage():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data")
        total_rows = cursor.fetchone()[0]
        time_of_use.config(text=total_rows)
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data WHERE response = 'Satisfied'")
        total_rows = cursor.fetchone()[0]
        time_satisfied.config(text=total_rows)
        cursor.execute("SELECT COUNT(*) FROM user_rersponse_data WHERE response = 'Not Satisfied'")
        total_rows = cursor.fetchone()[0]
        time_not_satisfied.config(text=total_rows)
        cursor.execute("SELECT COUNT(*) FROM users")
        total_rows = cursor.fetchone()[0]
        total_user.config(text=total_rows)
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


adminframeheader = Frame(app, width='880', height='40', background='white')
adminframeheader.place(x=10, y=10)
adminframe = Frame(app, width='880', height='420', background='white')
adminframe.place(x=10, y=70)


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


adminhomeconnectorframe = Frame(adminframe, width='40', height='20', background='darkblue')
adminhomeconnectorframe.place(x=230, y=37)
adminhome = Button(adminframe, width='20', border='0', text='Home Page', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                   activebackground='white', activeforeground='darkblue', command=switch1)
adminhome.place(x=30, y=30)
adminhomeframe = Frame(adminframe, width='620', height='400', background='darkblue')
adminhomeframe.place(x=250, y=10)
data = Label(adminhomeframe, text='Total time of Use', font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
data.place(x=80, y=50)
time_of_use = Label(adminhomeframe, font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
time_of_use.place(x=180, y=90)
timesatisfied = Label(adminhomeframe, text='Total time Satisfied', font=('Microsoft Yahei Ui Light', 20), fg='white',
                      bg='darkblue')
timesatisfied.place(x=350, y=50)
time_satisfied = Label(adminhomeframe, font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
time_satisfied.place(x=450, y=90)
timenotsatisfied = Label(adminhomeframe, text='Time Not Satisfied', font=('Microsoft Yahei Ui Light', 20), fg='white',
                         bg='darkblue')
timenotsatisfied.place(x=80, y=240)
time_not_satisfied = Label(adminhomeframe, font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
time_not_satisfied.place(x=180, y=280)
totaluser = Label(adminhomeframe, text='Total User', font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
totaluser.place(x=350, y=240)
total_user = Label(adminhomeframe, font=('Microsoft Yahei Ui Light', 20), fg='white', bg='darkblue')
total_user.place(x=450, y=280)


def savefault():
    fault_id = faultid.get()
    fault_name = faultname.get()
    fault_cause = faultcause.get()
    fault_solution = faultsolution.get()

    if (fault_id == "" or fault_name == "" or fault_solution == "" or fault_id == 'Fault ID Number' or
            fault_name == 'Fault Name' or fault_solution == 'Fault Solution' or fault_cause == "" or
            fault_cause == 'Fault Cause'):
        erroruser.config(text="All Fields are required", fg='red', bg='darkblue')
        erroruser.place(x=60, y=250)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("select * from car_fault where faultname='" + faultname.get() + "'")
            rows = cursor.fetchall()
            if rows:
                erroruser.config(text="Fault Name already exist", fg='red', bg='darkblue')
                erroruser.place(x=60, y=250)

                faultid.delete(0, 'end')
                faultname.delete(0, 'end')
                faultcause.delete(0, 'end')
                faultsolution.delete(0, 'end')
                faultid.insert(0, 'Fault ID Number')
                faultname.insert(0, 'Fault Name')
                faultcause.insert(0, 'Fault Cause')
                faultsolution.insert(0, 'Fault Solution')
            else:
                cursor.execute(
                    "insert into car_fault (faultid, faultname, faultcause, faultsolution) "
                    "VALUES (%s, %s, %s, %s)", (fault_id, fault_name, fault_cause, fault_solution,))
                conn.commit()

                erroruser.config(text="Car Fault saved", fg='green', bg='darkblue')
                erroruser.place(x=60, y=250)

                faultid.delete(0, 'end')
                faultname.delete(0, 'end')
                faultcause.delete(0, 'end')
                faultsolution.delete(0, 'end')
                faultid.insert(0, 'Fault ID Number')
                faultname.insert(0, 'Fault Name')
                faultcause.insert(0, 'Fault Cause')
                faultsolution.insert(0, 'Fault Solution')

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def searchfault():
    fault_id = faultid.get()
    if fault_id == "" or fault_id == "Fault ID Number":
        letter = 'CFT'
        number = ''.join(random.choices(string.digits, k=3))
        randomid = letter + number
        faultid.delete(0, 'end')
        faultid.insert(0, randomid)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("select * from car_fault where faultid='" + faultid.get() + "'")
            rows = cursor.fetchall()

            if rows:
                faultname.delete(0, 'end')
                faultcause.delete(0, 'end')
                faultsolution.delete(0, 'end')
                for row in rows:
                    faultname.insert(0, row[2])
                    faultcause.insert(0, row[3])
                    faultsolution.insert(0, row[4])
            else:
                erroruser.config(text="Fault ID does not exist", fg='red', bg='darkblue')
                erroruser.place(x=60, y=250)

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def updatefault():
    fault_id = faultid.get()
    fault_name = faultname.get()
    fault_cause = faultcause.get()
    fault_solution = faultsolution.get()

    if (fault_id == "" or fault_name == "" or fault_solution == "" or fault_id == 'Fault ID Number' or
            fault_name == 'Fault Name' or fault_solution == 'Fault Solution' or fault_cause == "" or
            fault_cause == 'Fault Cause'):
        erroruser.config(text="All Fields are required or click on search botton", fg='red', bg='darkblue')
        erroruser.place(x=60, y=250)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "Update car_fault SET faultname = %s, faultcause = %s, faultsolution = %s WHERE faultid = %s",
                (fault_name, fault_cause, fault_solution, fault_id))
            conn.commit()

            erroruser.config(text="Car Fault Updated", fg='green', bg='darkblue')
            erroruser.place(x=60, y=250)

            faultid.delete(0, 'end')
            faultname.delete(0, 'end')
            faultcause.delete(0, 'end')
            faultsolution.delete(0, 'end')
            faultid.insert(0, 'Fault ID Number')
            faultname.insert(0, 'Fault Name')
            faultcause.insert(0, 'Fault Cause')
            faultsolution.insert(0, 'Fault Solution')

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def deletefault():
    fault_id = faultid.get()
    fault_name = faultname.get()
    fault_cause = faultcause.get()
    fault_solution = faultsolution.get()
    if (fault_id == "Fault ID Number" or fault_id == ""):
        erroruser.config(text="Fault ID field most not be empty", fg='red', bg='darkblue')
        erroruser.place(x=60, y=250)

    elif (fault_name == "" or fault_solution == "" or
          fault_name == 'Fault Name' or fault_solution == 'Fault Solution' or fault_cause == "" or
          fault_cause == 'Fault Cause'):
        erroruser.config(text="Click on search button before deleting", fg='red', bg='darkblue')
        erroruser.place(x=60, y=250)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            reply2 = MessageBox.askyesno('Delete Car Fault', 'Are you sure you want to delete this car '
                                                             'fault')
            if reply2:
                cursor.execute("DELETE FROM car_fault WHERE faultid = '" + faultid.get() + "'")
                conn.commit()

            faultid.delete(0, 'end')
            faultname.delete(0, 'end')
            faultcause.delete(0, 'end')
            faultsolution.delete(0, 'end')
            faultid.insert(0, 'Fault ID Number')
            faultname.insert(0, 'Fault Name')
            faultcause.insert(0, 'Fault Cause')
            faultsolution.insert(0, 'Fault Solution')
            # show()
            erroruser.config(text="Car Fault deleted successfully", fg='green', bg='darkblue')
            erroruser.place(x=60, y=250)

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def switch2():
    adminhomeframe.place_forget()
    adminhomeconnectorframe.place_forget()
    admincarfaultframe.place(x=250, y=10)
    admincarfaultconnectorframe.place(x=230, y=127)
    manageuserframe.place_forget()
    manageruserconnectorframe.place_forget()
    dataframe.place_forget()
    dataconnectorframe.place_forget()


admincarfaultconnectorframe = Frame(adminframe, width='40', height='20', background='darkblue')
admincarfault = Button(adminframe, width='20', border='0', text='Car Fault', fg='white', bg='darkblue',
                       font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                       activebackground='white', activeforeground='darkblue', command=switch2)
admincarfault.place(x=30, y=120)
admincarfaultframe = Frame(adminframe, width='620', height='400', background='darkblue')


def on_enter(e):
    erroruser.place_forget()
    faultidframe.config(bg='white')
    if faultid.get() == 'Fault ID Number':
        faultid.delete(0, 'end')


def on_leave(e):
    faultidframe.config(bg='gray')
    if faultid.get() == '':
        faultid.insert(0, 'Fault ID Number')


faultid = Entry(admincarfaultframe, width=60, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11))
faultid.place(x=60, y=20)
faultid.insert(0, 'Fault ID Number')
faultid.bind("<FocusIn>", on_enter)
faultid.bind("<FocusOut>", on_leave)
faultidframe = Frame(admincarfaultframe, width=482, height=2, bg='gray')
faultidframe.place(x=60, y=45)


def on_enter(e):
    erroruser.place_forget()
    faultnameframe.config(bg='white')
    if faultname.get() == 'Fault Name':
        faultname.delete(0, 'end')


def on_leave(e):
    faultnameframe.config(bg='gray')
    if faultname.get() == '':
        faultname.insert(0, 'Fault Name')


faultname = Entry(admincarfaultframe, width=60, fg="black", border=0, bg='white', font=('Microsoft Yahei Ui Light', 11))
faultname.place(x=60, y=85)
faultname.insert(0, 'Fault Name')
faultname.bind("<FocusIn>", on_enter)
faultname.bind("<FocusOut>", on_leave)
faultnameframe = Frame(admincarfaultframe, width=482, height=2, bg='gray')
faultnameframe.place(x=60, y=110)


def on_enter(e):
    erroruser.place_forget()
    faultcauseframe.config(bg='white')
    if faultcause.get() == 'Fault Cause':
        faultcause.delete(0, 'end')


def on_leave(e):
    faultcauseframe.config(bg='gray')
    if faultcause.get() == '':
        faultcause.insert(0, 'Fault Cause')


faultcause = Entry(admincarfaultframe, width=60, fg="black", border=0, bg='white',
                   font=('Microsoft Yahei Ui Light', 11))
faultcause.place(x=60, y=150)
faultcause.insert(0, 'Fault Cause')
faultcause.bind("<FocusIn>", on_enter)
faultcause.bind("<FocusOut>", on_leave)
faultcauseframe = Frame(admincarfaultframe, width=482, height=2, bg='gray')
faultcauseframe.place(x=60, y=175)


def on_enter(e):
    erroruser.place_forget()
    faultsolutionframe.config(bg='white')
    if faultsolution.get() == 'Fault Solution':
        faultsolution.delete(0, 'end')


def on_leave(e):
    faultsolutionframe.config(bg='gray')
    if faultsolution.get() == '':
        faultsolution.insert(0, 'Fault Solution')


faultsolution = Entry(admincarfaultframe, width=60, fg="black", border=0, bg='white',
                      font=('Microsoft Yahei Ui Light', 11))
faultsolution.place(x=60, y=215)
faultsolution.insert(0, 'Fault Solution')
faultsolution.bind("<FocusIn>", on_enter)
faultsolution.bind("<FocusOut>", on_leave)
faultsolutionframe = Frame(admincarfaultframe, width=482, height=2, bg='gray')
faultsolutionframe.place(x=60, y=240)

erroruser = Label(admincarfaultframe, font=("Microsoft Yahei Ui Light", 8, 'bold'))

savefaultbuttom = Button(admincarfaultframe, width='20', border='0', text='Save Fault', fg='white', bg='gray',
                         font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                         activebackground='white', activeforeground='darkblue', command=savefault)
savefaultbuttom.place(x=60, y=280)
updatefaultbuttom = Button(admincarfaultframe, width='20', border='0', text='Update Fault', fg='white', bg='gray',
                           font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                           activebackground='white', activeforeground='darkblue', command=updatefault)
updatefaultbuttom.place(x=337, y=280)
deletefaultbuttom = Button(admincarfaultframe, width='20', border='0', text='Delete Fault', fg='white', bg='gray',
                           font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                           activebackground='white', activeforeground='darkblue', command=deletefault)
deletefaultbuttom.place(x=60, y=325)
searchfaultbutton = Button(admincarfaultframe, width='20', border='0', text='Search/Generate ID', fg='white', bg='gray',
                           font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                           activebackground='white', activeforeground='darkblue', command=searchfault)
searchfaultbutton.place(x=337, y=325)


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


def saveuser():
    car_model = carmodel.get()
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
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)
    else:
        password_length = len(pas_word)
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
                conn = connect_to_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM users WHERE username='" + username.get() + "'")
                    rows = cursor.fetchall()
                    if rows:
                        errorlabel.config(text="User already exist", fg='red',
                                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
                        errorlabel.place(x=60, y=220)

                        modelversion.delete(0, 'end')
                        carowner.delete(0, 'end')
                        platenumber.delete(0, 'end')
                        email.delete(0, 'end')
                        username.delete(0, 'end')
                        password.delete(0, 'end')
                        conpassword.delete(0, 'end')
                        modelversion.set('Car Model')
                        carowner.insert(0, "Car owner's name")
                        platenumber.insert(0, 'Car Plate Number')
                        email.insert(0, 'Email')
                        username.insert(0, 'Username')
                        password.insert(0, 'Password')
                        conpassword.insert(0, 'Password')
                    else:
                        cursor.execute(
                            "INSERT INTO users (car, carmodel, carowner, platenumber, email, username, password) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)", (car_model, model_version, car_owner,
                                                                    plate_number, e_mail, user_name, pas_word))
                        conn.commit()

                        errorlabel.config(text="User saved successfully", fg='green',
                                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
                        errorlabel.place(x=60, y=220)

                        modelversion.delete(0, 'end')
                        carowner.delete(0, 'end')
                        platenumber.delete(0, 'end')
                        email.delete(0, 'end')
                        username.delete(0, 'end')
                        password.delete(0, 'end')
                        conpassword.delete(0, 'end')
                        modelversion.set('Car Model')
                        carowner.insert(0, "Car owner's name")
                        platenumber.insert(0, 'Car Plate Number')
                        email.insert(0, 'Email')
                        username.insert(0, 'Username')
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
                              font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
            errorlabel.place(x=60, y=220)


def searchuser():
    user_name = username.get()
    if (user_name == "Username" or user_name == ""):
        errorlabel.config(text="Username field most not be empty", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users where username='" + username.get() + "'")
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
                                  font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
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
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)
    else:
        password_length = len(pas_word)
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
                conn = connect_to_db()
                cursor = conn.cursor()
                try:

                    cursor.execute(
                        ("Update users SET carmodel = %s, carowner = %s, platenumber = %s, email = %s, "
                         "password = %s WHERE username = %s"), (model_version, car_owner, plate_number, e_mail,
                                                                pas_word, user_name))
                    conn.commit()

                    errorlabel.config(text="User details Updated", fg='green',
                                      font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
                    errorlabel.place(x=60, y=220)

                    modelversion.delete(0, 'end')
                    carowner.delete(0, 'end')
                    platenumber.delete(0, 'end')
                    email.delete(0, 'end')
                    username.delete(0, 'end')
                    password.delete(0, 'end')
                    conpassword.delete(0, 'end')
                    modelversion.set('Car Model')
                    carowner.insert(0, "Car owner's name")
                    platenumber.insert(0, 'Car Plate Number')
                    email.insert(0, 'Email')
                    username.insert(0, 'Username')
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
                              font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
            errorlabel.place(x=60, y=220)


def deleteuser():
    model_version = modelversion.get()
    car_owner = carowner.get()
    plate_number = platenumber.get()
    e_mail = email.get()
    user_name = username.get()
    if (user_name == "Username" or user_name == ""):
        errorlabel.config(text="Username field most not be empty", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)

    elif (model_version == "" or model_version == "Car model" or car_owner == "" or car_owner == "Car owner's name" or
          plate_number == '' or plate_number == 'Car Plate Number' or e_mail == "" or
          e_mail == 'Email'):
        errorlabel.config(text="Click on search button before deleting", fg='red',
                          font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
        errorlabel.place(x=60, y=220)
    else:
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            reply3 = MessageBox.askyesno('Delete User', 'Are you sure you want to delete this users '
                                                        'details')
            if reply3:
                cursor.execute("DELETE FROM users WHERE username = '" + username.get() + "'")
                conn.commit()

            modelversion.delete(0, 'end')
            carowner.delete(0, 'end')
            platenumber.delete(0, 'end')
            email.delete(0, 'end')
            username.delete(0, 'end')
            password.delete(0, 'end')
            conpassword.delete(0, 'end')
            modelversion.set('Car Model')
            carowner.insert(0, "Car owner's name")
            platenumber.insert(0, 'Car Plate Number')
            email.insert(0, 'Email')
            username.insert(0, 'Username')
            password.insert(0, 'Password')
            conpassword.insert(0, 'Password')

            errorlabel.config(text="User details deleted successfully", fg='green',
                              font=("Microsoft Yahei Ui Light", 12), bg='darkblue')
            errorlabel.place(x=60, y=220)

        except Error as e:
            MessageBox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def switch3():
    adminhomeframe.place_forget()
    adminhomeconnectorframe.place_forget()
    admincarfaultframe.place_forget()
    admincarfaultconnectorframe.place_forget()
    manageuserframe.place(x=250, y=10)
    manageruserconnectorframe.place(x=230, y=217)
    dataframe.place_forget()
    dataconnectorframe.place_forget()


manageruserconnectorframe = Frame(adminframe, width='40', height='20', background='darkblue')
manageuser = Button(adminframe, width='20', border='0', text='Manage User', fg='white', bg='darkblue',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='white', activeforeground='darkblue', command=switch3)
manageuser.place(x=30, y=210)
manageuserframe = Frame(adminframe, width='620', height='400', background='darkblue')

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


def on_enter(e):
    usernameframe.config(bg='white')
    if username.get() == "Username":
        username.delete(0, 'end')


def on_leave(e):
    usernameframe.config(bg='gray')
    if username.get() == '':
        username.insert(0, "Username")


username = Entry(manageuserframe, width=29, fg="black", border=0, bg='white',
                 font=('Microsoft Yahei Ui Light', 11))
username.place(x=330, y=135)
username.insert(0, "Username")
username.bind("<FocusIn>", on_enter)
username.bind("<FocusOut>", on_leave)
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

saveuser = Button(manageuserframe, width='20', border='0', text='Save User', fg='white', bg='gray',
                  font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                  activebackground='white', activeforeground='darkblue', command=saveuser)
saveuser.place(x=60, y=260)
updateuser = Button(manageuserframe, width='20', border='0', text='Update User', fg='white', bg='gray',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='white', activeforeground='darkblue', command=updateuser)
updateuser.place(x=337, y=260)
deleteuser = Button(manageuserframe, width='20', border='0', text='Delete User', fg='white', bg='gray',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='red', activeforeground='white', command=deleteuser)
deleteuser.place(x=60, y=330)
searchuser = Button(manageuserframe, width='20', border='0', text='Search User', fg='white', bg='gray',
                    font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                    activebackground='white', activeforeground='darkblue', command=searchuser)
searchuser.place(x=337, y=330)


def fetch_user_history():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM user_rersponse_data")
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
    history = fetch_user_history()
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

        wrapped_user_response = wrap_text(f"User: {record[6]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"User ({record[6]}) Responses: {record[7]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        listbox.insert(END, "")
        serial_number += 1


def fetch_user_history_satisfied():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM user_rersponse_data WHERE response = 'Satisfied'")
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def display_user_history_satisfied():
    history = fetch_user_history_satisfied()
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

        wrapped_user_response = wrap_text(f"User: {record[6]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"User ({record[6]}) Responses: {record[7]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        listbox.insert(END, "")
        serial_number += 1


def fetch_user_history_not_satisfied():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM user_rersponse_data WHERE response = 'Not Satisfied'")
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def display_user_history_not_satisfied():
    history = fetch_user_history_not_satisfied()
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

        wrapped_user_response = wrap_text(f"User: {record[6]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"User ({record[6]}) Responses: {record[7]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        listbox.insert(END, "")
        serial_number += 1


def fetch_user_history_no_satisfied():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM user_rersponse_data WHERE response = 'No Response'")
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def wrap_text_no_satisfied(text, width):
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


def display_user_history_no_satisfied():
    history = fetch_user_history_no_satisfied()
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

        wrapped_user_response = wrap_text(f"User: {record[6]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"User ({record[6]}) Responses: {record[7]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        listbox.insert(END, "")
        serial_number += 1


def fetch_user_history_user():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        MessageBox.showerror("Error", str(e))
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def display_user_history_user():
    history = fetch_user_history_user()
    serial_number = 1
    listbox.delete(0, END)

    for record in history:
        listbox.insert(END, f"Serial Number: {serial_number}")

        wrapped_fault_cause = wrap_text(f"Car: {record[1]}", width=65)
        for line in wrapped_fault_cause:
            listbox.insert(END, line)

        wrapped_fault_solution = wrap_text(f"Car Model: {record[2]}", width=65)
        for line in wrapped_fault_solution:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"Car Owner: {record[3]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"Plate Number: {record[4]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"Email: {record[5]}", width=65)
        for line in wrapped_user_response:
            listbox.insert(END, line)

        wrapped_user_response = wrap_text(f"Username: {record[6]}", width=65)
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


dataconnectorframe = Frame(adminframe, width='40', height='20', background='darkblue')
data = Button(adminframe, width='20', border='0', text='Report(User Data)', fg='white', bg='darkblue',
              font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
              activebackground='white', activeforeground='darkblue', command=switch4)
data.place(x=30, y=300)
dataframe = Frame(adminframe, width='620', height='400', background='darkblue')
listbox = Listbox(dataframe, width=54, height=13, bg="gray", fg='white', font=("Microsoft Yahei Ui Light", 14, 'bold'))
listbox.place(x=10, y=10)
scrollbar = Scrollbar(dataframe, command=listbox.yview)
scrollbar.place(x=590, y=10, height=listbox.winfo_reqheight())
listbox.config(yscrollcommand=scrollbar.set)
all = Button(dataframe, width='12', border='0', text='All Data', fg='white', bg='darkblue',
             font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID,
             activebackground='white', activeforeground='black', command=display_user_history)
all.place(x=10, y=355)
satisfied = Button(dataframe, width='12', border='0', text='Satisfied', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID,
                   activebackground='white', activeforeground='black', command=display_user_history_satisfied)
satisfied.place(x=140, y=355)
not_satisfied = Button(dataframe, width='12', border='0', text='Not Satisfied', fg='white', bg='darkblue',
                       font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID,
                       activebackground='white', activeforeground='black', command=display_user_history_not_satisfied)
not_satisfied.place(x=260, y=355)
no_satisfied = Button(dataframe, width='12', border='0', text='No Response', fg='white', bg='darkblue',
                      font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID,
                      activebackground='white', activeforeground='black', command=display_user_history_no_satisfied)
no_satisfied.place(x=380, y=355)
user_data = Button(dataframe, width='12', border='0', text='User Data', fg='white', bg='darkblue',
                   font=("Microsoft Yahei Ui Light", 10, 'bold'), cursor="hand2", relief=SOLID,
                   activebackground='white', activeforeground='black', command=display_user_history_user)
user_data.place(x=500, y=355)

logout = Button(adminframe, width='20', border='0', text='Logout', fg='white', bg='darkblue',
                font=("Microsoft Yahei Ui Light", 12, 'bold'), cursor="hand2", relief=SOLID,
                activebackground='red', activeforeground='white', command=logout)
logout.place(x=30, y=370)

fetch_homepage()
errorckeck()
app.mainloop()
