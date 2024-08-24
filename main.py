from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.title("MasterJ's IDE")
file_path = ''
file_types = [('Python Files', '*.py'), ('Nodejs Files', '*.js'), ('All Files', '*.*')]


def set_file_path(path):
    global file_path
    file_path = path


def new():
    editor.delete('1.0', END)
    set_file_path('')


def open_file():
    try:
        path = askopenfilename(filetypes=file_types)
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)
    except FileNotFoundError:
        print('File not found')


def save_as():
    try:
        if file_path == '':
            path = asksaveasfilename(filetypes=file_types)
        else:
            path = file_path
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)
    except FileNotFoundError:
        print('File not found')


def run():
    if file_path == '':
        error_msg.replace('1.0', END, 'Please save your code.')
        return

    if file_path.endswith('.py'):
        command = f'python {file_path}'
    elif file_path.endswith('.js'):
        command = f'node {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    error_msg.replace('1.0', END, '')
    terminal.insert(END, output)
    terminal.insert(END, error)


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', command=new)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor = Text(height=31, width=1920)
editor.pack()

terminal = Text(height=10, width=1920)
terminal.pack()

error_msg = Text(height=1, width=1920)
error_msg.pack()

compiler.mainloop()
