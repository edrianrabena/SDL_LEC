import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="myPhone",
        database="students"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
    exit()

cursor = conn.cursor()

root = tk.Tk()
root.geometry("1400x400")
root.title("Teacher's Student Database")

tree = ttk.Treeview(root, columns=("Student ID", "Name", "Quiz 1", "Quiz 2", "Quiz 3", "Quiz 4"))

for i, column in enumerate(("Student ID", "Name", "Quiz 1", "Quiz 2", "Quiz 3", "Quiz 4")):
    tree.heading(i, text=column)

for column in tree["columns"]:
    tree.column(column, anchor="center")

tree.column("#0", width=0, stretch=tk.NO)

def display_data():
    try:
        result_label.config(text="")

        cursor.execute("SELECT * FROM quizzes")
        data = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in data:
            centered_row = tuple(f"{value:^10}" for value in row)
            tree.insert("", tk.END, values=centered_row)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch data from the database: {e}")
    finally:
        cursor.fetchall()

def calculate_s():
    entryVal = entry.get()
    query = "SELECT student_ID, student_name, quiz1, quiz2, quiz3, quiz4 FROM quizzes WHERE student_name LIKE %s"
    values = (f"%{entryVal}%",)
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()

        if not results:
            result_label.config(text="No results found")
        else:
            result_label.config(text=f"{len(results)} result(s) found")

        for item in tree.get_children():
            tree.delete(item)

        for row in results:
            centered_row = tuple(f"{value:^10}" for value in row)
            tree.insert("", tk.END, values=centered_row)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to search data in the database: {e}")
    finally:
        cursor.fetchall()

def calculate():
    entryVal = entry.get()
    query = "SELECT (quizzes.quiz1 + quizzes.quiz2 + quizzes.quiz3 + quizzes.quiz4)/4 AS Average, student_name FROM quizzes WHERE student_name LIKE %s"
    values = (f"%{entryVal}%",)
    
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()

        result_label.config(text="")

        if result:
            num_results = len(tree.get_children())
            if num_results > 1:  
                result_label.config(text="Error: More than one result in the list. Please refine your search.")
            else:
                average, student_name = result
                result_label.config(text=f"Average for {student_name}: {average}")
        else:
            result_label.config(text="No data available")
    except mysql.connector.Error as e:
        result_label.config(text=f"Error: {e}")
    finally:
        cursor.fetchall()

entry_label = tk.Label(root, text="Enter student name:")
entry_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

dispButton = tk.Button(button_frame, text="Search", command=calculate_s)
dispButton.pack(side=tk.LEFT)

calculate_button = tk.Button(button_frame, text="Calculate Average", command=calculate)
calculate_button.pack(side=tk.LEFT)

disp_all_button = tk.Button(button_frame, text="Display All Data", command=display_data)
disp_all_button.pack(side=tk.LEFT)

result_label = tk.Label(root, text="")
result_label.pack()

display_data()

tree.pack(expand=True, fill="both")
root.mainloop()
