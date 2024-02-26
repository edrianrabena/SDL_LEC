import tkinter as tk

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

def encrypt_text():
    text = entry.get()
    shift_str = shift_entry.get()

    if not text:
        result_label.config(text="Error: Please enter text")
        return
    if not shift_str:
        result_label.config(text="Error: Please enter shift value")
        return

    try:
        shift = int(shift_str)
        encrypted_text = caesar_cipher(text, shift)
        result_label.config(text="Encrypted text: " + encrypted_text)
    except ValueError:
        result_label.config(text="Error: Invalid shift value")

root = tk.Tk()
root.title("Caesar Cipher")

label = tk.Label(root, text="Enter text:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

shift_label = tk.Label(root, text="Enter shift value:")
shift_label.pack()

shift_entry = tk.Entry(root)
shift_entry.pack()

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
