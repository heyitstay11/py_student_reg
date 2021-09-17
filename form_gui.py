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

### Create Root Window and TabControl

root = tk.Tk()
root.title("Student Registration")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="  Form  ")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="  List  ")
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text="  Update  ")
tabControl.pack(expand=1)

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

            for item in list_frame.winfo_children():  # Delete all items inside list frame
                item.destroy()
            create_list() # Create a new List with new/updated data
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


ttk.Label(form_frame, text="Gender ", font=10).grid(column=0, row=3, padx=4, pady=6)
gender = tk.StringVar()
radio_male = ttk.Radiobutton(form_frame, text="Male" , variable=gender, value="M")
radio_male.grid(column=0, row=4, padx=4, pady=2)
radio_female = ttk.Radiobutton(form_frame, text="Female", variable=gender, value="F")
radio_female.grid(column=1, row=4, sticky="W")
radio_others = ttk.Radiobutton(form_frame, text="Others   ", variable=gender, value="O")
radio_others.grid(column=2, row=4, sticky="W")


ttk.Label(form_frame, text="Select Grade", font=10).grid(column=0, row=5)
grade = tk.StringVar()
select_grade = ttk.Combobox(form_frame, width=16, textvariable=grade, state="readonly")
select_grade['values'] = ('O', 'A', 'B', 'C')
select_grade.grid(column=1, row=5, pady=6)
select_grade.current(0)

btn_confirm = ttk.Button(form_frame, text="Confirm", command=add_student)
btn_confirm.grid(column=1,row=6, pady=16, sticky="W")

ttk.Label(form_frame, text="Enter Roll no to delete", font=10).grid(column=0, row=7)
btn_delete = ttk.Button(form_frame, text="Delete", command=del_student)
delroll = tk.StringVar()
entry_delroll = ttk.Entry(form_frame, width=20, textvariable=delroll)
entry_delroll.grid(column=1, row=7, sticky="W")
btn_delete.grid(column=2,row=7, padx=4, pady=10)

###



### LIST FRAME

list_frame = ttk.LabelFrame(tab2) #Create form_frame
list_frame.grid(column=0, row=0, padx=4, pady=2)

def create_list():
    ttk.Label(list_frame, text="Roll No", font=12).grid(pady=2, padx=4,column=0, row=1)
    ttk.Label(list_frame, text="Name", font=12).grid(pady=2, padx=4, column=1, row=1)
    ttk.Label(list_frame, text="Grade", font=12).grid(pady=2, padx=4, column=2, row=1)
    ttk.Label(list_frame, text="Gender", font=12).grid(pady=2, padx=4, column=3, row=1)

    # Fill list from DB
    get_data = "SELECT * FROM students"
    my_cursor.execute(get_data)

    for x in my_cursor: 
        inline_frame = ttk.Frame(list_frame)
        inline_frame.grid(column=0, columnspan=4, pady=2)
        ttk.Label(inline_frame, text=x[1], font=12).grid(padx=8,column=0, row=0, columnspan=1, sticky="W")
        ttk.Label(inline_frame, text=x[0], font=12).grid(padx=8, column=1, row=0, columnspan=1)
        ttk.Label(inline_frame, text=x[3], font=12).grid(padx=8, column=2, row=0, columnspan=1)
        ttk.Label(inline_frame, text=x[2], font=12).grid(padx=8, column=3, row=0, columnspan=1)

###
def fill_details():
     if not update_roll.get():
         messagebox.showerror(title="Error", message="Enter valid roll no")
     else:
        check_student = "Select * from students where rollno = " + update_roll.get()
        my_cursor.execute(check_student)
        
        for x in my_cursor: 
            print(x)
            entry_name_new.delete(0,END)
            entry_roll_new.delete(0, END)
            entry_name_new.insert(0,x[0])
            entry_roll_new.insert(0, x[1])
            if x[2] == 'M':
                radio_male_new.invoke()
            elif x[2] == 'F':
                radio_female_new.invoke()
            else:
                radio_others_new.invoke()
            select_grade_new.set(x[3])
            break
        else:
            messagebox.showerror(title="Error", message="No Student with roll no " + update_roll.get())

###



##### Update Student Frame
update_frame = tk.LabelFrame(tab3)
update_frame.grid(column=0, row=0, pady=2)
ttk.Label(update_frame, text="Update Student info", font=24).grid(column=0, row=0, padx=2, pady=4)

ttk.Label(update_frame, text="Enter Roll no to fill", font=10).grid(column=0, row=2)
btn_fill = ttk.Button(update_frame, text="Fill details", command=fill_details)
btn_fill.grid(column=2,row=2, padx=4, pady=10)
update_roll = tk.StringVar()
entry_update = ttk.Entry(update_frame, width=20, textvariable=update_roll)
entry_update.grid(column=1, row=2, sticky="W")

## update form elements
ttk.Label(update_frame, text="Enter name", font=10).grid(column=0, row=3, padx=4)
name_new = tk.StringVar()
entry_name_new = ttk.Entry(update_frame, width=20, textvariable=name_new)
entry_name_new.grid(column=1, row=3, sticky="W")


ttk.Label(update_frame, text="Enter Roll No.", font=10).grid(column=0, row=4, padx=4, pady=16)
roll_no_new = tk.StringVar()
entry_roll_new = ttk.Entry(update_frame, width=20, textvariable=roll_no_new)
entry_roll_new.grid(column=1, row=4, sticky="W")


ttk.Label(update_frame, text="Gender ", font=10).grid(column=0, row=5, padx=4)
gender_new = tk.StringVar()
radio_male_new = ttk.Radiobutton(update_frame, text="Male", variable=gender_new, value="M")
radio_male_new.grid(column=0, row=6, padx=4, pady=2)
radio_female_new = ttk.Radiobutton(update_frame, text="Female", variable=gender_new, value="F")
radio_female_new.grid(column=1, row=6, sticky="W")
radio_others_new = ttk.Radiobutton(update_frame, text="Others   ", variable=gender_new, value="O")
radio_others_new.grid(column=2, row=6, sticky="W")


ttk.Label(update_frame, text="Select Grade", font=10).grid(column=0, row=7)
grade_new = tk.StringVar()
select_grade_new = ttk.Combobox(update_frame, width=16, textvariable=grade_new, state="readonly")
select_grade_new['values'] = ('O', 'A', 'B', 'C')
select_grade_new.grid(column=1, row=7)
select_grade_new.current(0)

def update_student():
    check_student = "Select * from students where rollno = "+ roll_no_new.get()
    my_cursor.execute(check_student)
    
    for _ in my_cursor: 
        update_sql = "Update students SET name='"+name_new.get() + "', rollno='"+roll_no_new.get()+"', gender='"+gender_new.get()+"', grade='"+grade_new.get()+"' WHERE rollno="+roll_no_new.get()
        my_cursor.execute(update_sql)
        student_db.commit()
        messagebox.showinfo(title="Update", message="Student with roll no " + roll_no_new.get() + " updated")
        entry_update.delete(0,END)

        for item in list_frame.winfo_children():  # Delete all items inside list frame
            item.destroy()
        create_list() # Create a new List with new/updated data
        break
    else:
         messagebox.showerror(title="Error", message="No Student with roll no " + delroll.get())

btn_update_new = ttk.Button(update_frame, text="Update", command=update_student)
btn_update_new.grid(column=1,row=8, pady=10, sticky="W")

###


create_list()
root.mainloop() # start application