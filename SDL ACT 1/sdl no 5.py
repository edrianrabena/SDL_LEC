import tkinter as tk
from tkinter import ttk
import mysql.connector

def search_number():
    person_name = entry_name.get()
    query = "SELECT person_name, person_number FROM numbers WHERE person_name LIKE %s"
    cursor.execute(query, (f"%{person_name}%",))
    results = cursor.fetchall()
    tree.delete(*tree.get_children())
    if results:
        for result in results:
            number = str(result[1])
            if number.isdigit():
                number = f"0{number}"
            tree.insert("", "end", values=(result[0], number))
        selected_name.set("")
        selected_number.set("")
    else:
        selected_name.set("No number found for")
        selected_number.set(person_name)

def show_selected_item(event):
    selection = tree.selection()
    if selection:
        item = selection[0]
        values = tree.item(item, "values")
        if values:
            selected_name.set(values[0])
            number = values[1]
            if number.isdigit():
                number = f"{number}"
            selected_number.set(number)
        else:
            selected_name.set("")
            selected_number.set("")
    else:
        selected_name.set("")
        selected_number.set("")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="myPhone",
        database="my_phonebook"
    )
except mysql.connector.Error as e:
    tk.messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
    exit()

cursor = conn.cursor()

root = tk.Tk()
root.title("Phonebook Search")

label_name = tk.Label(root, text="Enter Person's Name:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

search_button = tk.Button(root, text="Search Number", command=search_number)
search_button.pack()

selected_name = tk.StringVar()
selected_number = tk.StringVar()
selected_label = tk.Label(root, textvariable=selected_name)
selected_label.pack()
selected_label = tk.Label(root, textvariable=selected_number)
selected_label.pack()

tree = ttk.Treeview(root, columns=("Name", "Number"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Number", text="Number")
tree.pack()

tree.bind("<<TreeviewSelect>>", show_selected_item)

root.mainloop()
