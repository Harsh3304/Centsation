# Inbuilt Modules
import os
import pathlib
import numpy as np
from datetime import date

# Installed Modules

import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageDraw

file_path = pathlib.Path(__file__).parent.resolve()
path = str(file_path) + "\\Dependencies"

MainScreen_location = str(file_path) + "\\Dependencies\\images\\MainScreen\\"
SearchScreen_location = str(file_path) + "\\Dependencies\\images\\SearchScreen\\"
DepositScreen_location = str(file_path) + "\\Dependencies\\images\\DepositScreen\\"
login_location = str(file_path) + "\\Dependencies\\images\\loginScreen\\"

passcode=input("enter your mysql password:")
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=passcode,
        database="Centsation"
    )

except:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=passcode
    )

cursor = db.cursor()
# Database Creation
cursor.execute("CREATE DATABASE IF NOT EXISTS Centsation")
cursor.execute("USE Centsation")
cursor.execute("""CREATE TABLE IF NOT EXISTS USERNAMES(
               Username         VARCHAR(50)     Primary Key,
               Password         VARCHAR(50)
)""")

def search():
    global SearchLabelImage
    global SearchBG
    global SearchBackButtonImage
    global SearchButtonImage
    searchwindow = Tk()
    searchwindow.title("{}'s Centsation".format(entered_username))
    searchwindow.maxsize(1200, 800)
    searchwindow.minsize(1200, 800)
    searchwindow.geometry("1220x800")
    searchwindow.config(bg="cyan")

    MainLabelImage = PhotoImage(file=MainScreen_location+"label.png")
    SearchBG = PhotoImage(file= SearchScreen_location+"SearchBg.png")
    SearchBackButtonImage = PhotoImage(file= MainScreen_location+"main_back_bt.png")
    DeleteEntryBtImage= PhotoImage(file= MainScreen_location+"delete_bt.png")
    EditEntryBtImage= PhotoImage(file= MainScreen_location+"edit_bt.png")
    SearchButtonImage= PhotoImage(file= SearchScreen_location+"Search_main_bt.png")

    SearchBGLabel = Label(searchwindow, image=SearchBG, bd=0)
    SearchBGLabel.place(x=0, y=0)
    def back():      
        searchwindow.destroy()
        tables()

    def delete_entry(Eid):
        command = "DELETE FROM entries_for_{0} WHERE id=%s".format(entered_username)
        cursor.execute(command)
        db.commit()
        search_mainscreen()

    def edit_entry(Eid, description, amount, user_date):
        searchwindow.destroy()
        if float(amount) >= 0:
            edit_deposit(Eid, description, amount, user_date)
        else:
            edit_withdraw(Eid, description, abs(float(amount)), user_date)

    def searched():
        global search_description
        global amount_max
        global amount_min
        global date_search
    
        search_description = DescriptionEntryBox.get()
        amount_min = AmountMinEntryBox.get()
        amount_max = AmountMaxEntryBox.get()
        date_search = DateEntryBox.get()
        if not search_description:
            messagebox.showinfo("Search", "Please enter a description to search.")
            return
        search_mainscreen()
        ""

    def search_mainscreen():
        global Eid
        style = ttk.Style()
        style.theme_use('clam')

        wrapper1 = LabelFrame(searchwindow, width="700", height="100", background="#161616", bd=0)
        mycanvas = Canvas(wrapper1, background="#161616", borderwidth=0, highlightthickness=0, width=698, height=638)
        mycanvas.pack(side=LEFT, expand=False, padx=0)

        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))
        myframe = Frame(mycanvas)
        myframe.config(bg="#161616")
        mycanvas.create_window((0, 0), window=myframe, anchor="n")

        wrapper1.place(x=114, y=138)
        def OnMouseWheel(event):
            mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

        mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

        # Get values from additional entry fields
        search_description = DescriptionEntryBox.get()
        amount_min = AmountMinEntryBox.get()
        amount_max = AmountMaxEntryBox.get()
        date_search = DateEntryBox.get()

        # Construct the SQL query with parameters
        search_query = "SELECT * FROM entries_for_{0} WHERE 1".format(entered_username)

        params = []

        if search_description:
            search_query += " AND description LIKE %s"
            params.append('%' + search_description + '%')
        if amount_min:
            search_query += " AND amount >= %s"
            params.append(float(amount_min))
        if amount_max:
            search_query += " AND amount <= %s"
            params.append(float(amount_max))
        if date_search:
            search_query += " AND date LIKE %s"
            params.append('%' + date_search + '%')

        cursor.execute(search_query, tuple(params))
        show_entries = cursor.fetchall()

        id_list, user_list, description_list, amount_list, date_list = [], [], [], [], []

        for row in show_entries:
            id_list.append(row[0])
            user_list.append(row[1])
            description_list.append(row[2])
            amount_list.append(row[3])
            date_list.append(row[4])

        total_entries = len(id_list)
        row1, column1 = 0, 0

        for i in range(0, total_entries):
            Eid = id_list[i]
            description = description_list[i]
            amount = amount_list[i]
            user_date = date_list[i]

            label2 = Label(myframe, image=MainLabelImage, bg="#161616", border=0,borderwidth=1)
            label2.grid(row=i, pady=2)

            Amountlabel = Label(myframe, text=amount, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Amountlabel.grid(row=i, sticky=W, padx=105, pady=(0, 43))

            Descriptionlabel = Label(myframe, text=description, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Descriptionlabel.grid(row=i, sticky=W, padx=140, pady=(33, 0))

            Datelabel = Label(myframe, text=user_date, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Datelabel.grid(row=i,sticky=W, padx=(460,10), pady=(1, 43))

            delete_but = Button(myframe, image= DeleteEntryBtImage, relief= FLAT, border=1, bg="#282828", activebackground="#282828", command=lambda: delete_entry(Eid))
            delete_but.grid(row=i, sticky=W, padx=(657,10), pady=(3, 39))

            edit_but = Button(myframe, image= EditEntryBtImage, relief= FLAT, border=0, bg="#282828", activebackground="#282828", command=lambda Eid=Eid, description=description, amount=amount, user_date=user_date: edit_entry(Eid, description, amount, user_date))


            edit_but.grid(row=i, sticky=W, padx=(659,10), pady=(42, 3))

            row1 += 1
     
    DescriptionEntryBox = Entry(searchwindow, relief=FLAT, width="17", font=("Century Gothic", 23), foreground="white", background="#161616")
    DescriptionEntryBox.place(x=850, y=197)

    AmountMinEntryBox= Entry(searchwindow, relief=FLAT, width="17", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountMinEntryBox.place(x=850, y=297)

    AmountMaxEntryBox= Entry(searchwindow, relief=FLAT, width="17", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountMaxEntryBox.place(x=850, y=398)

    DateEntryBox= Entry(searchwindow, relief=FLAT, width="17", font=("Century Gothic", 23), foreground="white", background="#161616")
    DateEntryBox.place(x=850, y=495)

    search_bt = Button(searchwindow, image= SearchButtonImage, relief=FLAT, border=0, bg="#282828", activebackground="#282828", command=searched)
    search_bt.place(x=878, y=580)

    back_bt = Button(searchwindow, image= SearchBackButtonImage, relief=FLAT, border=0, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=1, y=210)


def edit_deposit(Eid, description, amount, user_date):
    global depositBG
    global depositAdd_entry
    global depositBack
    depositwindow = Tk()
    depositwindow.title("Deposit Entry")
    depositwindow.maxsize(540, 610)
    depositwindow.minsize(540, 610)
    depositwindow.geometry("540x610")
    depositwindow.config(bg="black")

    depositBG=PhotoImage(file= DepositScreen_location+"Deposit_BG.png")
    depositAdd_entry=PhotoImage(file= DepositScreen_location+"add_entry_but.png")
    depositBack=PhotoImage(file= DepositScreen_location+"back_but.png")

    DepositBGLabel = Label(depositwindow, image=depositBG, bd=0)
    DepositBGLabel.place(x=0, y=0)

    def add_entry():
        description = DescriptionEntryBox.get()
        amount = AmountEntryBox.get()
        user_date = DateEntryBox.get()
        if not user_date:
            user_date = date.today().strftime("%Y-%m-%d")
        if description == "" and amount == "":
            messagebox.showerror("IMP", "Required field are missing")
        else:
            update_query = "UPDATE entries_for_{0} SET description=%s, amount=%s, date=%s WHERE id=%s".format(entered_username)
            cursor.execute(update_query, (description, amount, user_date, Eid))
            db.commit()
            DescriptionEntryBox.delete(0, "end")
            AmountEntryBox.delete(0, "end")
            DateEntryBox.delete(0, "end")
            

    def back():      
        depositwindow.destroy()
        tables()

    AmountEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountEntryBox.insert(END, amount)
    AmountEntryBox.place(x=39, y=168)

    DescriptionEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DescriptionEntryBox.insert(END, description)
    DescriptionEntryBox.place(x=39, y=282)

    DateEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DateEntryBox.insert(END, user_date)
    DateEntryBox.place(x=39, y=396)

    add_entry_but = Button(depositwindow, image=depositAdd_entry, relief=FLAT, bg="#282828", activebackground="#282828", command=add_entry)
    add_entry_but.place(x=194, y=480)

    back_bt = Button(depositwindow, image=depositBack, relief=FLAT, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=194, y=540)


def edit_withdraw(description, amount, user_date):
    global WithdrawBG
    global WithdrawAdd_entry
    global WithdrawBack
    withdrawwindow = Tk()
    withdrawwindow.title("Withdraw Entry")
    withdrawwindow.maxsize(540, 610)
    withdrawwindow.minsize(540, 610)
    withdrawwindow.geometry("540x610")
    withdrawwindow.config(bg="White")
    WithdrawBG=PhotoImage(file= DepositScreen_location+"Withdraw_BG.png")
    WithdrawAdd_entry=PhotoImage(file= DepositScreen_location+"add_entry_but.png")
    WithdrawBack=PhotoImage(file= DepositScreen_location+"back_but.png")

    WithdrawBGLabel = Label(withdrawwindow, image=WithdrawBG, bd=0)
    WithdrawBGLabel.place(x=0, y=0)

    def add_entry():
        # Pass the required arguments to add_entry
        description = DescriptionEntryBox.get()
        amount = AmountEntryBox.get()
        user_date = DateEntryBox.get()

        if not user_date:
            user_date = date.today().strftime("%Y-%m-%d")
            print(user_date)

        if description == "" and amount == "":
            messagebox.showerror("IMP", "Required field are missing")
        else:
            # Pass the required arguments to the add_entry function
            update_query = "UPDATE entries_for_{0} SET description=%s, amount=%s, date=%s WHERE id=%s".format(entered_username)
            cursor.execute(update_query, (description, amount, user_date, Eid))
            db.commit()
            DescriptionEntryBox.delete(0, "end")
            AmountEntryBox.delete(0, "end")
            DateEntryBox.delete(0, "end")
    def back():
        withdrawwindow.destroy()
        tables()
    

    AmountEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountEntryBox.insert(END, amount)
    AmountEntryBox.place(x=39, y=168)

    DescriptionEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DescriptionEntryBox.insert(END, description)
    DescriptionEntryBox.place(x=39, y=282)

    DateEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DateEntryBox.insert(END, user_date)
    DateEntryBox.place(x=39, y=396)

    add_entry_but = Button(withdrawwindow, image=WithdrawAdd_entry, relief=FLAT, bg="#282828", activebackground="#282828", command=add_entry)
    add_entry_but.place(x=194, y=480)

    back_bt = Button(withdrawwindow, image=WithdrawBack, relief=FLAT, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=194, y=540)




def deposit(description, amount, user_date):
    global depositBG
    global depositAdd_entry
    global depositBack
    depositwindow = Tk()
    depositwindow.title("Deposit Entry")
    depositwindow.maxsize(540, 610)
    depositwindow.minsize(540, 610)
    depositwindow.geometry("540x610")
    depositwindow.config(bg="black")
    depositBG=PhotoImage(file= DepositScreen_location+"Deposit_BG.png")
    depositAdd_entry=PhotoImage(file= DepositScreen_location+"add_entry_but.png")
    depositBack=PhotoImage(file= DepositScreen_location+"back_but.png")

    DepositBGLabel = Label(depositwindow, image=depositBG, bd=0)
    DepositBGLabel.place(x=0, y=0)

    def add_entry():
        description = DescriptionEntryBox.get()
        amount = AmountEntryBox.get()
        user_date = DateEntryBox.get()

        if not user_date:
            user_date = date.today().strftime("%Y-%m-%d")

            
            print(user_date)

        if description == "" and amount == "":
            messagebox.showerror("IMP", "Required field are missing")
        else:
            cursor.execute("INSERT INTO entries_for_{0} (user, description, amount, date) VALUES (%s, %s, %s, %s)".format(entered_username), (entered_username, description, amount, user_date))
            db.commit()
            DescriptionEntryBox.delete(0, "end")
            AmountEntryBox.delete(0, "end")
            DateEntryBox.delete(0, "end")

    def back():      
        depositwindow.destroy()
        tables()

    AmountEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountEntryBox.insert(END, amount)
    AmountEntryBox.place(x=39, y=168)

    DescriptionEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DescriptionEntryBox.insert(END, description)
    DescriptionEntryBox.place(x=39, y=282)

    DateEntryBox = Entry(depositwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DateEntryBox.insert(END, user_date)
    DateEntryBox.place(x=39, y=396)

    add_entry_but = Button(depositwindow, image=depositAdd_entry, relief=FLAT, bg="#282828", activebackground="#282828", command=add_entry)
    add_entry_but.place(x=194, y=480)

    back_bt = Button(depositwindow, image=depositBack, relief=FLAT, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=194, y=540)



def withdraw(description, amount, user_date):
    global WithdrawBG
    global WithdrawAdd_entry
    global WithdrawBack
    withdrawwindow = Tk()
    withdrawwindow.title("Withdraw Entry")
    withdrawwindow.maxsize(540, 610)
    withdrawwindow.minsize(540, 610)
    withdrawwindow.geometry("540x610")
    withdrawwindow.config(bg="White")
    WithdrawBG=PhotoImage(file= DepositScreen_location+"Withdraw_BG.png")
    WithdrawAdd_entry=PhotoImage(file= DepositScreen_location+"add_entry_but.png")
    WithdrawBack=PhotoImage(file= DepositScreen_location+"back_but.png")

    WithdrawBGLabel = Label(withdrawwindow, image=WithdrawBG, bd=0)
    WithdrawBGLabel.place(x=0, y=0)


    def add_entry():
        # Pass the required arguments to add_entry
        description = DescriptionEntryBox.get()
        amount = AmountEntryBox.get()
        user_date = DateEntryBox.get()

        if not user_date:
            user_date = date.today().strftime("%Y-%m-%d")
            print(user_date)

        if description == "" and amount == "":
            messagebox.showerror("IMP", "Required field are missing")
        else:
            # Pass the required arguments to the add_entry function
            cursor.execute("INSERT INTO entries_for_{0} (user, description, amount, date) VALUES (%s, %s, %s, %s)".format(entered_username), (entered_username, description, -abs(float(amount)), user_date))
            db.commit()
            DescriptionEntryBox.delete(0, "end")
            AmountEntryBox.delete(0, "end")
            DateEntryBox.delete(0, "end")
    def back():
        withdrawwindow.destroy()
        tables()
    

    AmountEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    AmountEntryBox.insert(END, amount)
    AmountEntryBox.place(x=39, y=168)

    DescriptionEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DescriptionEntryBox.insert(END, description)
    DescriptionEntryBox.place(x=39, y=282)

    DateEntryBox = Entry(withdrawwindow, relief=FLAT, width="27", font=("Century Gothic", 23), foreground="white", background="#161616")
    DateEntryBox.insert(END, user_date)
    DateEntryBox.place(x=39, y=396)

    add_entry_but = Button(withdrawwindow, image=WithdrawAdd_entry, relief=FLAT, bg="#282828", activebackground="#282828", command=add_entry)
    add_entry_but.place(x=194, y=480)

    back_bt = Button(withdrawwindow, image=WithdrawBack, relief=FLAT, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=194, y=540)


    
def tables():
    global loginwindow
    global entered_username
    global AmountLabel
    global update_balance
    global update_monthly_expense
    global MainBG
    global WithdrawButtonImage
    global DepositButtonImage
    global MainBackButtonImage
    global MainAddIDButtonImage
    global MainDeleteIDButtonImage
    global MainSearchButtonImage
    global MainLabelImage
    global StatusImage
    try:
        loginwindow.destroy()
    except:
        pass
    
    tablewindow = Tk()
    tablewindow.title("{}'s Centsation".format(entered_username))
    tablewindow.maxsize(1200, 800)
    tablewindow.minsize(1200, 800)
    tablewindow.geometry("1200x800")
    tablewindow.config(bg="#282828")
    
    
    MainBG = PhotoImage(file= MainScreen_location+"Main_BG.png")
    MainLabelImage= PhotoImage(file= MainScreen_location+"label.png")
    DeleteEntryBtImage= PhotoImage(file= MainScreen_location+"delete_bt.png")
    EditEntryBtImage= PhotoImage(file= MainScreen_location+"edit_bt.png")
    
    BGLabel = Label(tablewindow, image=MainBG, bd=0)
    BGLabel.place(x=0, y=0)

    def update_balance():
        global balance
        cursor.execute("SELECT SUM(amount) FROM entries_for_{0}".format(entered_username))
        balance = cursor.fetchone()[0]
        if balance is None:
            balance = 0.0
    
    def update_monthly_expense():
        global monthly_expense
        cursor.execute("SELECT SUM(amount) FROM entries_for_{0} WHERE amount < 0 AND YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = MONTH(CURDATE())".format(entered_username))
        monthly_expense = cursor.fetchone()[0]
        if monthly_expense is None:
            monthly_expense = 0.0

    def update_expense():
        global expense
        cursor.execute("SELECT SUM(amount) FROM entries_for_{0} WHERE amount < 0".format(entered_username))
        expense = cursor.fetchone()[0]
        if expense is None:
            expense = 0.0

    
    def back():
        tablewindow.destroy()
        main()

    def searched():
        try:
            tablewindow.destroy()
        except:
            pass
        search()
    
    def deposited():
        try:
            tablewindow.destroy()
        except:
            pass
        description=""
        user_date=""
        amount=""
        deposit(description, amount, user_date)

    def withdrawed():
        try:
            tablewindow.destroy()
        except:
            pass
        description=""
        user_date=""
        amount=""

        withdraw(description, amount, user_date)
        
            
    def delete_user():
        cursor.execute("Drop TABLE entries_for_{}".format(entered_username))
        cursor.execute("DELETE FROM USERNAMES where username='{}'".format(entered_username))
        main()
        try:
            tablewindow.destroy()
        except:
            pass

    def add_user():
        global signup
        tablewindow.destroy()
        signup()

    update_balance()
    update_monthly_expense()
    update_expense()

    def delete_entry(Eid):
        command = "DELETE FROM entries_for_{0} WHERE id='{1}';".format(entered_username, Eid)
        cursor.execute(command)
        db.commit()

        mainscreen()
        update_balance()
        update_monthly_expense()
        update_expense()

    def edit_entry(Eid, description, amount, user_date):
        tablewindow.destroy()

        if float(amount) >= 0:
            edit_deposit(Eid, description, amount, user_date)
        else:
            edit_withdraw(Eid, description, abs(float(amount)), user_date)
    
    def get_status(money):
        if money < 0:
            return f"{MainScreen_location}//debt.png"
        elif money == 0:
            return f"{MainScreen_location}//zero.png"
        elif 0 < money < 1000:
            return f"{MainScreen_location}//alert.png"
        else:
            return f"{MainScreen_location}//rich.png"

    def mainscreen():
        global Eid
        style = ttk.Style()
        style.theme_use('clam')

        wrapper1 = LabelFrame(tablewindow, width="700", height="100", background="#161616", bd=0)
        mycanvas = Canvas(wrapper1, background="#161616", borderwidth=0, highlightthickness=0, width=698, height=462)
        mycanvas.pack(side=LEFT, expand=False, padx=0)

        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
        
        mycanvas.configure(yscrollcommand=yscrollbar.set)

        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))
        myframe = Frame(mycanvas)
        myframe.config(bg="#161616")
        mycanvas.create_window((0, 0), window=myframe, anchor="n")
        wrapper1.place(x=114, y=315)
        def OnMouseWheel(event):
            mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

        mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

        entries = "SELECT * from entries_for_{0} ORDER BY id".format(entered_username)
        cursor.execute(entries)
        show_entries = cursor.fetchall()

        id_list, user_list, description_list, amount_list, date_list = [], [], [], [], []

        for row in show_entries:
            id_list.append(row[0])
            user_list.append(row[1])
            description_list.append(row[2])
            amount_list.append(row[3])
            date_list.append(row[4])
        
        total_entries = len(id_list)
        row1, column1 = 0, 0

        for i in range(0, total_entries):
            Eid = id_list[i]
            description = description_list[i]
            amount = amount_list[i]
            user_date = date_list[i]

            label2 = Label(myframe, image=MainLabelImage, bg="#161616", border=0,borderwidth=1)
            label2.grid(row=i, pady=2)

            Amountlabel = Label(myframe, text=amount, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Amountlabel.grid(row=i, sticky=W, padx=105, pady=(0, 43))

            Descriptionlabel = Label(myframe, text=description, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Descriptionlabel.grid(row=i, sticky=W, padx=140, pady=(33, 0))

            Datelabel = Label(myframe, text=user_date, background="#282828", font=("Bahnschrift SemiLight Condensed", 18),
                              foreground="#FFFFFF")
            Datelabel.grid(row=i,sticky=W, padx=(460,10), pady=(1, 43))

            delete_but = Button(myframe, image= DeleteEntryBtImage, relief= FLAT, border=1, bg="#282828", activebackground="#282828", command=lambda Eid=Eid: delete_entry(Eid))
            delete_but.grid(row=i, sticky=W, padx=(657,10), pady=(3, 39))

            edit_but = Button(myframe, image= EditEntryBtImage, relief= FLAT, border=0, bg="#282828", activebackground="#282828", command=lambda Eid=Eid, description=description, amount=amount, user_date=user_date: edit_entry(Eid, description, amount, user_date))
            edit_but.grid(row=i, sticky=W, padx=(659,10), pady=(42, 3))

            row1 += 1
           
    mainscreen()   
    
    NameLabel = PhotoImage(file= MainScreen_location+"name_label.png")
    MoneyLabel = PhotoImage(file= MainScreen_location+"money_label.png")
    WithdrawButtonImage = PhotoImage(file= MainScreen_location+"withdraw_bt.png")
    DepositButtonImage = PhotoImage(file= MainScreen_location+"deposit_bt.png")
    MainBackButtonImage = PhotoImage(file= MainScreen_location+"main_back_bt.png")
    MainAddIDButtonImage = PhotoImage(file= MainScreen_location+"main_addID_bt.png")
    MainDeleteIDButtonImage = PhotoImage(file= MainScreen_location+"main_deleteID_bt.png")
    MainSearchButtonImage = PhotoImage(file= MainScreen_location+"main_search_bt.png")

    status=get_status(balance)
    StatusImage = PhotoImage(file= status)
    
    UsernameLabel = Label(tablewindow, image=NameLabel, text="{}".format(entered_username), font=("Century Gothic", 34), justify='center', compound="center", wraplength=500,  bd=0, fg="#FFFFFF", bg="#282828")
    UsernameLabel.place(x=124, y=137)

    AmountLabel = Label(tablewindow, image=MoneyLabel, text=(f"${balance:.2f}"), font=("Century Gothic", 30), justify='center', compound="center", wraplength=500, bd=0, fg="#FFFFFF", bg="#282828")
    AmountLabel.place(x=482, y=178)
    
    
    # Monthly_ExpenseLabel = Label(tablewindow, text=(f"Monthly Expense: ${-monthly_expense:.2f}"),font=("Bahnschrift SemiLight Condensed", 22), border=0)
    # Monthly_ExpenseLabel.place(x=800, y=125)
    ExpenseLabel = Label(tablewindow, image=MoneyLabel, text=(f"${-expense:.2f}"), font=("Century Gothic", 30), justify='center', compound="center", wraplength=500, bd=0, fg="#FFFFFF", bg="#282828")
    ExpenseLabel.place(x=840, y=178)
   
    StatusLabel = Label(tablewindow, image=StatusImage, bg="#282828", border=0)
    StatusLabel.place(x=895, y=562)

    deposit_but = Button(tablewindow, image=DepositButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=deposited)
    deposit_but.place(x=841, y=360)

    withdraw_but = Button(tablewindow, image=WithdrawButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=withdrawed)
    withdraw_but.place(x=841, y=426)

    back_bt = Button(tablewindow, image=MainBackButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=back)
    back_bt.place(x=1, y=210)

    search_but = Button(tablewindow, image=MainSearchButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=searched)
    search_but.place(x=1, y=299)

    add_user_but = Button(tablewindow, image=MainAddIDButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=add_user)
    add_user_but.place(x=1, y=388)

    delete_user_but = Button(tablewindow, image=MainDeleteIDButtonImage, relief=FLAT, bd=0, bg="#282828", activebackground="#282828", command=delete_user)
    delete_user_but.place(x=1, y=477)

def login():
    global entered_username
    global entered_password
    global loginwindow
    global SignIn_BG
    global login_bt_image
    global Back_bt_image
    
    try:
        window.destroy()
    except:
        pass
    loginwindow = Tk()
    loginwindow.title("Centsation")
    loginwindow.maxsize(410, 710)
    loginwindow.minsize(410, 710)
    loginwindow.geometry("410x710")
    loginwindow.config(bg="#D5EAE8")
    SignIn_BG = PhotoImage(file= login_location+"Main1.png")
    login_bt_image = PhotoImage(file= login_location+"SignIn_bt.png")
    Back_bt_image = PhotoImage(file= login_location+"back_bt.png")

    SignInBGLabel = Label(loginwindow, image=SignIn_BG, bd=0)
    SignInBGLabel.place(x=0, y=0)

    def logined():
        global entered_username
        global entered_password

        entered_username = UsernameEntryBox.get()
        entered_password = UserPasswordEntryBox.get()

        # Add logic to check if username and password match in the database
        select_query = "SELECT * FROM USERNAMES WHERE username = %s AND password = %s"
        cursor.execute(select_query, (entered_username, entered_password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Successful", "Welcome, {}!".format(entered_username))
            tables()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def back():
        loginwindow.destroy()
        main()

    UsernameEntryBox = Entry(loginwindow, relief=FLAT, width="16", font=("Century Gothic", 22), foreground="white", background="#404040")
    UsernameEntryBox.place(x=125, y=129)

    UserPasswordEntryBox = Entry(loginwindow, relief=FLAT, width="16", font=("Century Gothic", 22), foreground="white", background="#404040")
    UserPasswordEntryBox.place(x=125, y=238)

    login_but = Button(loginwindow, image=login_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=logined)
    login_but.place(x=130, y=380)

    back_bt = Button(loginwindow, image=Back_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=back)
    back_bt.place(x=130, y=460)

def signup():
    global entered_username
    global entered_password
    global SignUp_BG
    global SignUp_bt_image
    global Back_bt_image

    try:
        window.destroy()
    except:
        pass
    signupwindow = Tk()
    signupwindow.title("Centsation")
    signupwindow.maxsize(410, 710)
    signupwindow.minsize(410, 710)
    signupwindow.geometry("1200x800")
    signupwindow.config(bg="#D5EAE8")
    SignUp_BG = PhotoImage(file= login_location+"Main1.png")
    SignUp_bt_image = PhotoImage(file= login_location+"SignUp_bt.png")
    Back_bt_image = PhotoImage(file= login_location+"back_bt.png")
    SignUpBGLabel = Label(signupwindow, image=SignUp_BG, bd=0)
    SignUpBGLabel.place(x=0, y=0)

    def signed_up():
        global entered_username
        global entered_password

        entered_username = SignupUsernameEntryBox.get()
        entered_password = SignupUserPasswordEntryBox.get()
        
        insert_query = "INSERT INTO USERNAMES (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(insert_query, (entered_username, entered_password))
            # Commit the change
            db.commit()
            messagebox.showinfo("Registration Successful", "User {} registered successfully.".format(entered_username))
            check_query = "SELECT * FROM USERNAMES WHERE username = %s"
            cursor.execute(check_query, (entered_username,))
            checker = cursor.fetchall()
            if checker:
                # Create a new table for the user
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS entries_for_{0} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user VARCHAR(255),
                        description VARCHAR(255),
                        amount DECIMAL(10, 2),
                        date DATE
                    )
                """.format(entered_username)

                cursor.execute(create_table_query)
                print("Query successful")
                signupwindow.destroy()
                tables()
            else:
                messagebox.showerror("Table Creation Failed", "Failed to create table for user {}".format(entered_username))
            
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                messagebox.showerror("Registration Failed", "Username already exists. Please choose a different username.")
            else:
                messagebox.showerror("Registration Failed", "An error occurred: {}".format(e))

    def back():
        signupwindow.destroy()
        main()

    SignupUsernameEntryBox = Entry(signupwindow, relief=FLAT, width="16", font=("Century Gothic", 22), foreground="white", background="#404040")
    SignupUsernameEntryBox.place(x=125, y=129)

    SignupUserPasswordEntryBox = Entry(signupwindow, relief=FLAT, width="16", font=("Century Gothic", 22), foreground="white", background="#404040")
    SignupUserPasswordEntryBox.place(x=125, y=238)

    signup_but = Button(signupwindow, image=SignUp_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=signed_up)
    signup_but.place(x=130, y=380)

    back_bt = Button(signupwindow, image=Back_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=back)
    back_bt.place(x=130, y=460)

def main():
    global window
    global login_BG
    global login_bt_image
    global SignUp_bt_image
    window = Tk()
    window.geometry('410x710')
    window.maxsize(410, 710)
    window.minsize(410, 710)
    window.title("Centsation")
    window.configure(background='black')
    login_BG = PhotoImage(file= login_location+"Main.png")
    login_bt_image = PhotoImage(file= login_location+"SignIn_bt.png")
    SignUp_bt_image = PhotoImage(file= login_location+"SignUp_bt.png")

    ChoiceBGLabel = Label(window, image=login_BG, bd=0)
    ChoiceBGLabel.place(x=0, y=0)

    # Add Contact Button
    login_bt = Button(window,image=login_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=login)
    login_bt.place(x=130, y=280)

    # login Contact Button
    signup_bt = Button(window, image=SignUp_bt_image, relief=FLAT, bd=0, bg="#161616", activebackground="#161616", command=signup)
    signup_bt.place(x=130, y=370)

main()
mainloop()

cursor.close()
db.close()
