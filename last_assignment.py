from tkinter import *
from tkinter import ttk
import mysql.connector as mc
from tkinter import messagebox as mb


def add_info():
    try:
        std_id = int(entry_id.get())
        name = entry_name.get()
        address = entry_address.get()
        number = entry_number.get()
        degree = entry_degree.get()

        query = 'insert into my_table values(%s, %s, %s, %s, %s)'
        values = (std_id, name, address, number, degree)
        db_cursor.execute(query, values)

        connector.commit()
        mb.showinfo("Data inserted successfully.")
        clear()
        show()

    except ValueError as err:
        mb.showinfo('error', 'ID contains number only')
        print(err)

    except mc.IntegrityError as err:
        print(err)

    except mc.DatabaseError:
        mb.showinfo('long', 'please enter shorter value in the columns.')


def partition(arr, low, high):
    if combo_sort.get() == 'Id':
        column = 0
    elif combo_sort.get() == 'Name':
        column = 1
    elif combo_sort.get() == 'Address':
        column = 2
    elif combo_sort.get() == 'Number':
        column = 3
    else:
        column = 4
    i = (low - 1)
    pivot = arr[high][column]
    for j in range(low, high):
        if arr[j][column] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

def quickSort(arr, low, high):
    if low < high:

        pi = partition(arr, low, high)

        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def sort():
    db_cursor.execute('select * from my_table')
    array = db_cursor.fetchall()
    quickSort(array, 0, len(array) - 1)

    student_table.delete(*student_table.get_children())

    for row in array:
        student_table.insert('', 'end', values=row)


def clear():
    entry_id.config(state='normal')
    entry_search.delete(0, END)
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    entry_address.delete(0, END)
    entry_number.delete(0, END)
    entry_degree.delete(0, END)


def show():
    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    query = 'select * from my_table'
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    for row in results:
        student_table.insert('', 'end', values=row)


def search(provided_list=None):
    if not provided_list:
        query = "select * from my_table"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
    else:
        results = provided_list

    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    target = entry_search.get()
    if combo_search.get() == 'Id':
        column = 0
        if target.isdigit():
            target = int(target)
        else:
            return
    elif combo_search.get() == 'Name':
        column = 1
    elif combo_search.get() == 'Address':
        column = 2
    elif combo_search.get() == 'Number':
        column = 3
    else:
        column = 4

    found = []
    for row in results:
        if target == row[column]:
            found.append(row)

    for row in found:
        student_table.insert('', 'end', values=row)
    return found


def update():
    try:
        name = entry_name.get()
        address = entry_address.get()
        number = entry_number.get()
        degree = entry_degree.get()

        query = 'update my_table set name=%s, address=%s, number=%s, degree=%s where id=%s'
        values = (name, address, number, degree, pointer())
        db_cursor.execute(query, values)
        connector.commit()
        clear()
        show()

    except ValueError as err:
        print(err)


def delete():
    query = 'delete from my_table where id=%s'
    values = (pointer(),)
    db_cursor.execute(query, values)
    connector.commit()
    show()
    clear()


def pointer():
    try:
        clear()
        point = student_table.focus()

        content = student_table.item(point)
        row = content['values']
        entry_id.insert(0, row[0])
        entry_name.insert(0, row[1])
        entry_address.insert(0, row[2])
        entry_number.insert(0, row[3])
        entry_degree.insert(0, row[4])
        return row[0]

    except IndexError:
        pass


try:
    connector = mc.connect(user='root', passwd='Iamstillyounge1@', host='localhost')
    db_cursor = connector.cursor()
    db_cursor.execute('create database if not exists db')
    connector.database = "db"
    db_cursor.execute('create table if not exists my_table(id int not null,'
                      'name varchar(40), address varchar(50), number varchar(13), degree varchar(40),'
                      'constraint pk_id primary key(id))')

except mc.DatabaseError as err:
    print(err)

root = Tk()
root.title("Student Management System")
root.geometry('800x650+300+60')
root.configure(bg="purple")

# Frames
top_frame = Frame(root)
top_frame.configure(bg="purple")
top_frame.pack()

bottom_frame = Frame(root)
bottom_frame.configure(bg="purple")
bottom_frame.pack()

show_frame = Frame(root, width=200, height=150, relief=RIDGE, bd=4)
show_frame.configure(bg="purple")
show_frame.pack()

combo_search = ttk.Combobox(top_frame, width=10, font='bold 12')
combo_search['values'] = ('Id', 'Name', 'Address', 'Number', 'Degree')
combo_search.current(0)
combo_search.grid(row=0, column=1, pady=8)

combo_sort = ttk.Combobox(top_frame, width=10, font='bold 12')
combo_sort['values'] = ('Id', 'Name', 'Address', 'Number', 'Degree')
combo_sort.current(0)
combo_sort.grid(row=1, column=1, pady=8)


# widgets
lbl_search = Label(top_frame, text="Search", font='bold 16', bg='aqua')
lbl_sort = Label(top_frame, text="Sort", font='bold 16', bg='aqua')
lbl_id = Label(top_frame, text="ID :-", font='bold 16', bg='aqua')
lbl_name = Label(top_frame, text="Name :-", font='bold 16', bg='aqua')
lbl_address = Label(top_frame, text="Address :-", font='bold 16', bg='aqua')
lbl_number = Label(top_frame, text="Number:-", font='bold 16', bg='aqua')
lbl_degree = Label(top_frame, text="Degree :-", font='bold 16', bg='aqua')


lbl_search.grid(row=0, column=0, padx=8, pady=8)
lbl_sort.grid(row=1, column=0, padx=8, pady=8)

entry_search = Entry(top_frame, width=15, font='bold 12')
entry_search.grid(row=0, column=2, padx=15, pady=8)
btn_search = Button(top_frame, width=8, text='Search', font='bold 12', command=search, bg="blue")
btn_search.grid(row=0, column=3, padx=20, pady=20)
btn_sort = Button(top_frame, width=8, text='Sort', font='bold 12', command=sort, bg="blue")
btn_sort.grid(row=1, column=2, padx=20, pady=20)

lbl_id.grid(row=4, column=0, padx=15, pady=8)
lbl_name.grid(row=5, column=0, padx=15, pady=8)
lbl_address.grid(row=6, column=0, padx=15, pady=8)
lbl_number.grid(row=7, column=0, padx=15, pady=8)
lbl_degree.grid(row=8, column=0, padx=15, pady=8)

# Entry

entry_id = Entry(top_frame, width=28, font='bold 14')
entry_name = Entry(top_frame, width=28, font='bold 14')
entry_address = Entry(top_frame, width=28, font='bold 14')
entry_number = Entry(top_frame, width=28, font='bold 14')
entry_degree = Entry(top_frame, width=28, font='bold 14')

entry_search.bind('<Return>', lambda e: search())

entry_id.grid(row=4, column=1, padx=15, pady=8)
entry_name.grid(row=5, column=1, padx=15, pady=8)
entry_address.grid(row=6, column=1, padx=15, pady=8)
entry_number.grid(row=7, column=1, padx=15, pady=8)
entry_degree.grid(row=8, column=1, padx=15, pady=8)

# button
btn_add = Button(bottom_frame, width=8, text='Add', font='arial 14', command=add_info, bg="blue")
btn_show = Button(bottom_frame, width=8, text='Show', font='arial 14', command=show, bg="blue")
btn_delete = Button(bottom_frame, width=8, text='Delete', font='arial 14', command=delete, bg="blue")
btn_update = Button(bottom_frame, width=8, text='Update', font='arial 14', command=update, bg="blue")
btn_clear = Button(bottom_frame, width=8, text='Clear', font='arial 14', command=clear, bg="blue")


btn_add.grid(row=9, column=0, padx=20, pady=20)
btn_show.grid(row=9, column=1, padx=20, pady=20)
btn_delete.grid(row=9, column=2, padx=20, pady=20)
btn_update.grid(row=9, column=3, padx=20, pady=20)
btn_clear.grid(row=9, column=4, padx=20, pady=20)

# Tree view
scroll_x = Scrollbar(show_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(show_frame, orient=VERTICAL)

student_table = ttk.Treeview(show_frame, column=('id', 'name', 'address', 'number', 'degree'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
student_table.pack()

student_table.column('id', width=120)
student_table.column('name', width=120)
student_table.column('address', width=120)
student_table.column('number', width=120)
student_table.column('degree', width=120)
student_table['show'] = 'headings'

student_table.heading('id', text='ID', anchor=W)
student_table.heading('name', text='Name', anchor=W)
student_table.heading('address', text='Address', anchor=W)
student_table.heading('number', text='Number', anchor=W)
student_table.heading('degree', text='Degree', anchor=W)

scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)
student_table.bind('<ButtonRelease-1>', lambda e: pointer())


if __name__ == '__main__':
    root.mainloop()