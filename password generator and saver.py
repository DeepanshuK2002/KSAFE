import random
import string
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, scrolledtext, simpledialog

def generate_password():
    try:
        length = int(password_length.get())
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        generated_password.set(password)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the password length")

def save_password():
    username = username_entry.get()
    password = generated_password.get()
    
    if username and password:
        with open("passwords.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        messagebox.showinfo("Success", f"Password saved for {username}!")
        username_entry.delete(0, tk.END)
        generated_password.set("")
    else:
        messagebox.showwarning("Input Error", "Please generate a password and enter a username")

def check_master_password():
    try:
        with open("master_password.txt", "r") as file:
            stored_password = file.read().strip()
    except FileNotFoundError:
        stored_password = None
    
    if not stored_password:
        master_password = simpledialog.askstring("Create Master Password", "Enter your new master password:", show='*')
        if master_password:
            with open("master_password.txt", "w") as file:
                file.write(master_password)
            messagebox.showinfo("Success", "Master password created!")
            return True
        else:
            messagebox.showerror("Input Error", "Master password not set. Please try again.")
            return False
    else:
        entered_password = simpledialog.askstring("Master Password", "Enter the master password:", show='*')
        if entered_password == stored_password:
            return True
        else:
            messagebox.showerror("Access Denied", "Incorrect password!")
            return False

def view_saved_passwords():
    if not check_master_password():
        return
    
    try:
        with open("passwords.txt", "r") as file:
            passwords = file.read()
        
        if passwords:
            text_area.config(state=tk.NORMAL)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, passwords)
            text_area.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No Data", "No passwords have been saved yet.")
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "No passwords saved yet.")

def delete_password():
    if not check_master_password():
        return

    username_to_delete = delete_entry.get()
    if not username_to_delete:
        messagebox.showwarning("Input Error", "Please enter a username to delete.")
        return

    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()
        
        with open("passwords.txt", "w") as file:
            deleted = False
            for line in lines:
                if f"Username: {username_to_delete}" not in line:
                    file.write(line)
                else:
                    deleted = True
        
        if deleted:
            messagebox.showinfo("Success", f"Password for '{username_to_delete}' has been deleted.")
            delete_entry.delete(0, tk.END)
            view_saved_passwords()
        else:
            messagebox.showinfo("Not Found", f"No password found for username '{username_to_delete}'.")
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "No passwords saved yet.")

root = tk.Tk()
root.title("Random Password Generator")
root.geometry("440x550")
root.resizable(False, False)

image_icon = tk.PhotoImage(file="lock.png")
root.iconphoto(False, image_icon)

password_length = tk.StringVar()
generated_password = tk.StringVar()

tk.Label(root, text="Enter password length:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root, textvariable=password_length)
length_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Button(root, text="Generate Password", command=generate_password).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Generated Password:").grid(row=2, column=0, padx=10, pady=10)
password_display = tk.Entry(root, textvariable=generated_password, state='readonly')
password_display.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Username:").grid(row=3, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Save Password", command=save_password).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

tk.Button(root, text="View Saved Passwords", command=view_saved_passwords).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

text_area = scrolledtext.ScrolledText(root, width=50, height=10)
text_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
text_area.config(state=tk.DISABLED)

tk.Label(root, text="Enter Username to Delete:").grid(row=7, column=0, padx=10, pady=10)
delete_entry = tk.Entry(root)
delete_entry.grid(row=7, column=1, padx=10, pady=10)

tk.Button(root, text="Delete Password", command=delete_password).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

def resize_master_password_prompt():
    master_window = simpledialog._QueryString(root) 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = master_window.winfo_height()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    master_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.mainloop()
