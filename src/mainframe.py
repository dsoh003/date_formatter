import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os

from handlers.csv_handler import *
from handlers.xlsx_handler import *

# Vars
formats = ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY/MM/DD', 'YYYY/DD/MM']

# Window Init
window = tk.Tk()
window.title('CSV/XLSX Date Formatter')
window.geometry('500x400')
window.resizable(False, False)


# Handlers
def open_file():
    file = fd.askopenfilename()
    select_entry.insert(0, file)
    if file:
        select_button.config(state="active")


def clear_all():
    select_entry.delete(0, 'end')
    select_fieldnames.delete(0, 'end')
    select_button.config(state='disabled')
    convert_button.config(state='disabled')


def check_filetype(file: str) -> str:
    file_list = file.split('.')
    return file_list[len(file_list)-1].lower()


def check_file(file: str) -> bool:
    return os.path.exists(file)


def display_error(message: str):
    mb.showerror('Error!', message)


def read_file():
    file = select_entry.get()
    date_format = default_select.get()
    if len(select_fieldnames.curselection()) == 0:
        mb.showwarning('Warning!',
                       'No headers selected! Please select at least one header!')
    else:
        if file:
            if not check_file(file):
                raise Exception('File does not exist')
            ext = check_filetype(file)
            if ext == 'csv':
                filename, error = read_csv(file, date_format, select_fieldnames)
                if error is None:
                    clear_all()
                    mb.showinfo('Success!',
                                'File saved to: %s' % filename)
                    latest_file.configure(text=filename)
                    latest_file.grid(row=4, column=1, columnspan=4,
                                     padx=10, pady=(10, 0), sticky='w')
                else:
                    display_error(error)
            elif ext == 'xlsx':
                filename, error = read_xlsx(file, date_format, select_fieldnames)
                if error is None:
                    clear_all()
                    mb.showinfo('Success!',
                                'File saved to: %s' % filename)
                    latest_file.configure(text=filename)
                    latest_file.grid(row=4, column=1, columnspan=4,
                                     padx=10, pady=(10, 0), sticky='w')
                else:
                    print(error)
                    display_error(error)
            else:
                display_error('File extension not supported: .%s' % ext)
        else:
            mb.showwarning('Warning!',
                           'Invalid or no file selected!')


def show_fieldnames():
    file = select_entry.get()
    select_fieldnames.delete(0, 'end')
    if file:
        if not check_file(file):
            raise Exception('File does not exist')
        ext = check_filetype(file)
        if ext == 'csv':
            fieldnames = get_fieldnames(file)
            for i in range(len(fieldnames)):
                select_fieldnames.insert(i, fieldnames[i])
            convert_button.config(state='active')
        elif ext == 'xlsx':
            fieldnames = get_xlsx_headers(file)
            for i in range(len(fieldnames)):
                select_fieldnames.insert(i, fieldnames[i])
            convert_button.config(state='active')
        else:
            display_error('File extension not supported: .%s' % ext)
    else:
        mb.showwarning('Warning!',
                       'Invalid or no file selected!')


# UI
# initial frame
main_frame = tk.Frame(
    master=window,
    borderwidth=5
)
main_frame.pack(expand=False)
# r0c0
top_pad = tk.Label(
    master=main_frame,
    text='CSV/XLSX Date Formatter',
    font='Helvetica 18 bold',
)
top_pad.grid(row=0, column=0, columnspan=5, sticky='w')
# r1c0
select_text = tk.Label(
    master=main_frame,
    text='Select a file:'
)
select_text.grid(row=1, column=0, sticky='w')
# r1c1
select_entry = tk.Entry(
    master=main_frame,
    width=40
)
select_entry.grid(row=1, column=1, columnspan=3)
# r1c4
select_button = tk.Button(
    master=main_frame,
    text='Open file',
    command=open_file,
    width=10
)
select_button.grid(row=1, column=4, padx=10)
# r2c0
select_format = tk.Label(
    master=main_frame,
    text='Select a format:',
    width=11
)
select_format.grid(row=2, column=0, columnspan=1, pady=(10, 0), sticky='w')
# r2c1
default_select = tk.StringVar(
    master=main_frame
)
default_select.set(formats[0])
format_selector = tk.OptionMenu(
    main_frame,
    default_select,
    *formats
)
format_selector.grid(row=2, column=1, pady=(10, 0), columnspan=3)
# r3c0
fieldname_label = tk.Label(
    master=main_frame,
    text='Select valid\ndate headers'
)
# r3c1
fieldname_label.grid(row=3, column=0)
select_fieldnames = tk.Listbox(
    master=main_frame,
    selectmode='multiple',
    height=11
)
select_fieldnames.grid(row=3, column=1, padx=10, pady=(0,10), sticky='sw')
# r3c2
buttons_frame = tk.Frame(
    master=main_frame
)
buttons_frame.rowconfigure(5)
buttons_frame.columnconfigure(2)
buttons_frame.grid(row=3, column=2, columnspan=3)
# r3c2 r0c0
usage_label = tk.Label(
    master=buttons_frame,
    text='How to use',
    font=('Helvetica', '8', 'bold')
)
usage_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky='nw')
# r3c2 r1c0
instructions = tk.Label(
    master=buttons_frame,
    text='1) Open a CSV/XLSX file\n'
         '2) Select target format\n'
         '3) Click "Read File"\n'
         '4) Select target headers to convert\n'
         '5) Click "Convert"\n'
         '6) Locate output on Desktop',
    font=('Helvetica', '8'),
    justify='left'
)
instructions.grid(row=1, column=0, columnspan=2, sticky='nw')
# r3c2 r2c0
select_button = tk.Button(
    master=buttons_frame,
    text='Read File',
    command=show_fieldnames,
    width=10
)
select_button.config(state="disabled")
select_button.grid(row=2, column=0, padx=10, pady=10, sticky='n')
# r3c2 r2c1
clear_all_button = tk.Button(
    master=buttons_frame,
    text='Clear all',
    command=clear_all,
    width=10
)
clear_all_button.grid(row=2, column=1, padx=10, pady=10, sticky='n')
# r3c2 r3c0
convert_button = tk.Button(
    master=buttons_frame,
    text='Convert',
    command=read_file,
    width=10
)
convert_button.config(state='disabled')
convert_button.grid(row=3, column=0, padx=10, pady=10, sticky='n')
# r4c0
latest_title = tk.Label(
    master=main_frame,
    text='Latest file processed:'
)
latest_title.grid(row=4, column=0, padx=10, pady=(10, 0))
# r4c1
latest_file = tk.Label(
    master=main_frame,
    font=('Helvetica', '9')
)
latest_file.grid_forget()
window.mainloop()

# How to create .exe
# pyinstaller mainframe.py --name "DA Date Formatter"
