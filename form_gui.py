import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import END
import mysql.connector

### Connect to database
student_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="student_gui"
)

my_cursor = student_db.cursor()

### Create Root Window

root = tk.Tk()
root.title("Student Registration")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Form")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="List")
tabControl.pack(expand=1, fill="both")

###


### FORM FRAME

### Functions:  Add Student to DB and List Frame

def add_student():
    if not name.get() and not roll_no.get() and not gender.get() :
        messagebox.showerror(title="Error", message="Something is missing")
    else:
        messagebox.showinfo(title="Student Added", message= "Student "+ name.get() +" with roll no " + roll_no.get() +" registered")
       
        student_val = (name.get(), roll_no.get(), gender.get(), grade.get())
        sql = "INSERT INTO students (name, rollno, gender, grade) VALUES (%s, %s, %s, %s)"
        my_cursor.execute(sql, student_val)
        student_db.commit()

        for item in list_frame.winfo_children():
                item.destroy()
        create_list()
        entry_name.delete(0,END)
        entry_roll.delete(0,END)

### Delete Student
def del_student():
    if not delroll.get():
         messagebox.showerror(title="Error", message="Enter valid roll no")
    else:
        check_student = "Select * from students where rollno = "+ delroll.get()
        my_cursor.execute(check_student)

        for _ in my_cursor: 
            del_sql = "DELETE FROM students where rollno = " + delroll.get()
            my_cursor.execute(del_sql)
            student_db.commit()
            messagebox.showinfo(title="Deletion", message="Student with roll no " + delroll.get() + " deleted")
            entry_delroll.delete(0,END)

            for item in list_frame.winfo_children():
                item.destroy()
            create_list()
            break
        else:
            messagebox.showerror(title="Error", message="No Student with roll no " + delroll.get())


# Elements

form_frame = ttk.LabelFrame(tab1) #Create form_frame
form_frame.grid(column=0, row=0, padx=4, pady=2)

title_1 = ttk.Label(form_frame, text="Student Registration", font=24)
title_1.grid(column=0, row=0, padx=12, pady=10)

ttk.Label(form_frame, text="Enter name", font=10).grid(column=0, row=1, padx=4)
name = tk.StringVar()
entry_name = ttk.Entry(form_frame, width=20, textvariable=name)
entry_name.grid(column=1, row=1, sticky="W")


ttk.Label(form_frame, text="Enter Roll No.", font=10).grid(column=0, row=2, padx=4, pady=16)
roll_no = tk.StringVar()
entry_roll = ttk.Entry(form_frame, width=20, textvariable=roll_no)
entry_roll.grid(column=1, row=2, sticky="W")


ttk.Label(form_frame, text="Gender ", font=10).grid(column=0, row=3, padx=4)
gender = tk.StringVar()
radio_male = tk.Radiobutton(form_frame, text="Male", font=10, variable=gender, value="M")
radio_male.grid(column=0, row=4, padx=4, pady=2)
radio_female = tk.Radiobutton(form_frame, text="Female",font=10, variable=gender, value="F")
radio_female.grid(column=1, row=4, sticky="W")
radio_male = tk.Radiobutton(form_frame, text="Others   ", font=10, variable=gender, value="O")
radio_male.grid(column=2, row=4, sticky="W")


ttk.Label(form_frame, text="Select Grade", font=10).grid(column=0, row=5)
grade = tk.StringVar()
select_grade = ttk.Combobox(form_frame, width=16, textvariable=grade, state="readonly")
select_grade['values'] = ('O', 'A', 'B', 'C')
select_grade.grid(column=1, row=5)
select_grade.current(0)

btn_confirm = tk.Button(form_frame, text="Confirm",font=16, command=add_student)
btn_confirm.grid(column=1,row=6, pady=10, sticky="W")

ttk.Label(form_frame, text="Enter Roll no to delete", font=10).grid(column=0, row=7)
btn_delete = tk.Button(form_frame, text="Delete",font=16, command=del_student)
delroll = tk.StringVar()
entry_delroll = ttk.Entry(form_frame, width=20, textvariable=delroll)
entry_delroll.grid(column=1, row=7, sticky="W")
btn_delete.grid(column=2,row=7, padx=4, pady=10)

###

### LIST FRAME

list_frame = ttk.LabelFrame(tab2) #Create form_frame
list_frame.grid(column=0, row=0, padx=4, pady=2)

def create_list():
    ttk.Label(list_frame, text="Roll No", font=24).grid(pady=2, padx=4,column=0, row=1)
    ttk.Label(list_frame, text="Name", font=24).grid(pady=2, padx=4, column=1, row=1)
    ttk.Label(list_frame, text="Grade", font=24).grid(pady=2, padx=4, column=2, row=1)
    ttk.Label(list_frame, text="Gender", font=24).grid(pady=2, padx=4, column=3, row=1)

    # Fill list from DB
    get_data = "SELECT * FROM students"
    my_cursor.execute(get_data)

    for x in my_cursor: 
        inline_frame = ttk.LabelFrame(list_frame)
        inline_frame.grid(column=0, columnspan=4)
        ttk.Label(inline_frame, text=x[1], font=24).grid(padx=4,column=0, row=0, columnspan=1)
        ttk.Label(inline_frame, text=x[0], font=24).grid(padx=4, column=1, row=0, columnspan=1)
        ttk.Label(inline_frame, text=x[3], font=24).grid(padx=4, column=2, row=0, columnspan=1)
        ttk.Label(inline_frame, text=x[2], font=24).grid(padx=4, column=3, row=0, columnspan=1)

###
create_list()

root.mainloop() # start application