import sqlite3
from sqlite3 import Error
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = Tk()
window.title("Дупа росте")
window.geometry('500x480')

try:
    con = sqlite3.connect('dup.sqlite3')
except Error as e:
    messagebox.showinfo("  ", f"'{e}', Помилка бази даних ")

tree = ttk.Treeview(columns=("Name", "Calories"), show="headings")


cursor_obj = con.cursor()
cursor_obj.execute('SELECT name FROM fruits')
drop_list = cursor_obj.fetchall()  # Випадаючий список


def sql_table():
    cursor_obj.execute(
        "CREATE TABLE fruits(id integer PRIMARY KEY AUTOINCREMENT, name text, calories real)")
    con.commit()


def sql_insert():
    input_name = entry_input_name.get()
    input_calories = entry_input_calories.get()
    if input_name.isalnum() and input_calories.isdigit() and int(input_calories) > 0:
        input_summ = (input_name, input_calories)
        try:
            cursor_obj.execute('INSERT INTO fruits(name, calories) VALUES(?, ?)', input_summ)
        except Error:
            messagebox.showinfo("  ", "Така позиція вже існує ")
        con.commit()
        entry_input_name.delete(0, tk.END)
        entry_input_calories.delete(0, tk.END)
    else:
        messagebox.showinfo("  ", "Введіть коректні дані ")


def sql_update():
    input_name = entry_input_name.get()
    input_calories = entry_input_calories.get()
    if (input_name,) in drop_list:
        if input_name.isalnum() and input_calories.isdigit() and int(input_calories) > 0:
            input_summ = (input_calories, input_name)
            cursor_obj.execute('UPDATE fruits SET calories = ? where name = ?', input_summ)
            con.commit()
            entry_input_name.delete(0, tk.END)
            entry_input_calories.delete(0, tk.END)
        else:
            messagebox.showinfo("  ", "Введіть коректні дані ")
    else:
        messagebox.showinfo("  ", "Така позиція відсутня ")


def sql_del():
    name_for_del = (entry_input_name.get(),)
    if name_for_del in drop_list:
        cursor_obj.execute('DELETE FROM fruits where name = ?', name_for_del)
        entry_input_name.delete(0, tk.END)
        con.commit()
    else:
        messagebox.showinfo("  ", "Така позиція відсутня ")


def sql_print():
    global tree
    tree = ttk.Treeview(columns=("Name", "Calories"), show="headings")
    tree.heading("Name", text="Найменування", anchor=W)
    tree.heading("Calories", text="Калорійність", anchor=W)
    cursor_obj.execute('SELECT name, calories FROM fruits  ORDER BY name')
    tree.place(x=20, y=250)
    scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=0.95, rely=0.5, relheight=0.5)
    for i in cursor_obj:
        tree.insert("", END, values=i)


def create_button(txt, comm, xcoord, ycoord):
    creating_button = Button(window, text=txt, command=comm)
    creating_button.place(x=xcoord, y=ycoord)


create_button("Ввести", sql_insert, 20, 80)
create_button("Корегувати", sql_update, 100, 80)
create_button("Видалити", sql_del, 260, 80)
create_button("Друк", sql_print, 350, 80)

label_input_name = Label(text="введіть найменування :").place(x=18, y=30)
entry_input_name = Entry(window, width=25)
entry_input_name.place(x=20, y=50)

label_input_calories = Label(text="введіть калорійність, кКал/кг :").place(x=250, y=30)
entry_input_calories = Entry(window, width=25)
entry_input_calories.place(x=250, y=50)

label_assortment = Label(text="виберіть продукт :").place(x=18, y=130)
combo = ttk.Combobox(window, values=drop_list)
combo.current(0)
combo.place(x=20, y=150)

label_input_weight = Label(text="введіть кількість, гр :").place(x=250, y=130)
entry_input_weight = Entry(window, width=25)
entry_input_weight.place(x=250, y=150)


output_table = Text(window, wrap=WORD)

catalog_selecting = []  # Каталог вибраних продуктів:  продукт - вага
catalog_calories = {}  # Каталог вибраних продуктів: продукт - кількість калорій


def selection():
    select = combo.get()
    weight = entry_input_weight.get()  # Ввід кількості продукта
    if (select,) in drop_list and weight.isdigit():
        entry_input_weight.delete(0, tk.END)  # Обнулення поля вводу кількості продукта
        catalog_selecting.append((select, weight))  # Заповнення каталогу вибраних продуктів: продукт - вага
        calories = cursor_obj.execute("SELECT calories FROM fruits WHERE name=?", (select,)).fetchone()
        catalog_calories[select] = float(weight) * calories[0]  # формування каталогу: продукт - кількість калорій
    else:
        messagebox.showinfo("  ", "Введіть коректні дані ")


def show():
    global tree
    tree = ttk.Treeview(columns=("Name", "Calories"), show="headings")
    tree.heading("Name", text="Найменування", anchor=W)
    tree.heading("Calories", text="Калорійність", anchor=W)
    tree.place(x=20, y=250)
    scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=0.95, rely=0.5, relheight=0.5)
    for i in catalog_selecting:
        tree.insert("", END, values=i)


def calculation():
    summ = sum(catalog_calories.values())
    output_text = 'Ваша дупа зросте на ' + str(round(summ/1000)) + ' кКал'
    messagebox.showinfo(" ", output_text)


def clear_all():
    catalog_calories.clear()
    catalog_selecting.clear()
    global tree
    tree = ttk.Treeview(columns=("Name", "Calories"), show="headings")
    tree.heading("Name", text="Найменування", anchor=W)
    tree.heading("Calories", text="Калорійність", anchor=W)
    tree.place(x=20, y=250)


create_button("Додати", selection, 20, 180)
create_button("Показати", show, 100, 180)
create_button("Розрахувати", calculation, 250, 180)
create_button("Очистити", clear_all, 340, 180)

window.mainloop()
