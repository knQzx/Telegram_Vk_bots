from tkinter import *
from tkinter import messagebox
def btn_click():
    k = ent.get()
    if k == 'ПАРОЛЬ':
        messagebox.showinfo(title = 'Успех', message = 'Windows разблокирована\n Нажмите ОК')
        root.destroy()
    else:
        messagebox.showinfo(title = 'Неудача', message = 'Windows еще блокирована')
def exits():
    if ent.get() != 'ПАРОЛЬ':
        messagebox.showwarning(title = 'Ошибка', message = 'Неправильный пароль')
root = Tk()
root.title('Windows заблокирован')
root.geometry('1500x1500')
root['bg'] = 'red'
root.protocol('WM_DELETE_WINDOW', exits)
Label(root, text = 'Введи пароль, твоя винда заблокирована', font = 'Arial 25', bg = 'red', fg = 'white').pack()
ent = Entry(root, text = ' ', font = 'Arial 25', width = 15)
ent.pack()
Button(root, text = 'Разблокировать', font = 'Arial 25', bg = 'purple', fg = 'white', command = btn_click).pack()
root.mainloop()
