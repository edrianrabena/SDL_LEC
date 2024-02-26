import tkinter as tk
from tkinter import messagebox
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="myPhone",
        database="hardware"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
    exit()

cursor = conn.cursor()

def update_inventory_add():
    update_inventory(1)

def update_inventory_subtract():
    selected_item = dropdown_var.get()
    count_change = entry_count.get()
    if not count_change.isdigit():
        messagebox.showerror("Error", "Please enter a valid count change (integer)")
        return

    cursor.execute("SELECT count FROM inventory WHERE BINARY item = %s", (selected_item,))
    result = cursor.fetchone()
    if result is None:
        messagebox.showerror("Error", f"Item '{selected_item}' not found in inventory")
        return
    current_count = result[0]

    try:
        count_change = int(count_change)
        new_count = current_count - count_change
    except ValueError:
        messagebox.showerror("Error", "Invalid count change")
        return
    
    if new_count < 0:
        messagebox.showerror("Error", "Subtracting this many items would result in a negative count")
        return

    query = "UPDATE inventory SET count = %s WHERE BINARY item = %s"
    cursor.execute(query, (new_count, selected_item))
    conn.commit()
    messagebox.showinfo("Success", f"Inventory for {selected_item} updated successfully")

    display_count.config(text=f"Current Count: {new_count}")

def update_inventory(change):
    selected_item = dropdown_var.get()
    count_change = entry_count.get()
    if not count_change.isdigit():
        messagebox.showerror("Error", "Please enter a valid count change (integer)")
        return

    cursor.execute("SELECT count FROM inventory WHERE BINARY item = %s", (selected_item,))
    result = cursor.fetchone()
    if result is None:
        messagebox.showerror("Error", f"Item '{selected_item}' not found in inventory")
        return
    current_count = result[0]

    try:
        count_change = int(count_change)
        new_count = current_count + (change * count_change)
    except ValueError:
        messagebox.showerror("Error", "Invalid count change")
        return

    query = "UPDATE inventory SET count = %s WHERE BINARY item = %s"
    cursor.execute(query, (new_count, selected_item))
    conn.commit()
    messagebox.showinfo("Success", f"Inventory for {selected_item} updated successfully")

    display_count.config(text=f"Current Count: {new_count}")

def validate_integer(new_value):
    if new_value == "":
        return True
    try:
        int(new_value)
        return True
    except ValueError:
        return False

def show_current_count(event):
    selected_item = dropdown_var.get()
    if selected_item == "Select an item":
        display_count.config(text="")
        return
    cursor.execute("SELECT count FROM inventory WHERE BINARY item = %s", (selected_item,))
    result = cursor.fetchone()
    if result:
        current_count = result[0]
        display_count.config(text=f"Current Count: {current_count}")
    else:
        messagebox.showerror("Error", f"Item '{selected_item}' not found in inventory")

root = tk.Tk()
root.geometry("400x200")
root.title("Inventory Management")

window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

dropdown_var = tk.StringVar(root)
dropdown_var.set("Select an item")

items = ['Motherboard', 'Hard Disk', 'Diskette', 'Compact Disk', 'Memory Cards']

dropdown_menu = tk.OptionMenu(root, dropdown_var, *items, command=show_current_count)
dropdown_menu.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

entry_label = tk.Label(root, text="Enter count:")
entry_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
validate_cmd = root.register(validate_integer)
entry_count = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P"))
entry_count.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

display_count = tk.Label(root, text="")
display_count.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

add_button = tk.Button(root, text="Add to Inventory", command=update_inventory_add)
add_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

subtract_button = tk.Button(root, text="Subtract from Inventory", command=update_inventory_subtract)
subtract_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
