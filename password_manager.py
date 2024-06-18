import os
import json
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog,messagebox

class PasswordManager:
    def __init__(self, key_file="secret.key",data_file = "password.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.load_key()
        self.fernet = Fernet(self.key)
        self.passwords = self.load_passwords()
    
    def load_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file,'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file,'wb') as file:
                file.write(key)
        return key
    
    def load_passwords(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data.encode()).decode()
            return json.loads(decrypted_data)
        else:
            return {}
        
    def save_passwords(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.passwords).encode()).decode()
        with open(self.data_file, 'w') as file:
            file.write(encrypted_data)

    def add_password(self, site, username, password):
        self.passwords[site] = {'username': username, 'password': password}
        self.save_passwords()

    def get_password(self, site):
        return self.passwords.get(site)

    def delete_password(self, site):
        if site in self.passwords:
            del self.passwords[site]
            self.save_passwords()

class PasswordManagerGUI:
    def __init__(self, root, password_manager):
        self.root = root
        self.password_manager = password_manager
        self.root.title("Password Manager")

        self.create_widgets()

    def create_widgets(self):
        # Add/Update Password
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(pady=10)

        tk.Label(self.add_frame, text="Site:").grid(row=0, column=0)
        self.site_entry = tk.Entry(self.add_frame)
        self.site_entry.grid(row=0, column=1)

        tk.Label(self.add_frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(self.add_frame)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.add_frame, text="Password:").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.add_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.add_frame, text="Add/Update Password", command=self.add_password)
        self.add_button.grid(row=3, columnspan=2, pady=5)

        # Get Password
        self.get_frame = tk.Frame(self.root)
        self.get_frame.pack(pady=10)

        tk.Label(self.get_frame, text="Site:").grid(row=0, column=0)
        self.get_site_entry = tk.Entry(self.get_frame)
        self.get_site_entry.grid(row=0, column=1)

        self.get_button = tk.Button(self.get_frame, text="Get Password", command=self.get_password)
        self.get_button.grid(row=1, columnspan=2, pady=5)

        # Delete Password
        self.delete_frame = tk.Frame(self.root)
        self.delete_frame.pack(pady=10)

        tk.Label(self.delete_frame, text="Site:").grid(row=0, column=0)
        self.delete_site_entry = tk.Entry(self.delete_frame)
        self.delete_site_entry.grid(row=0, column=1)

        self.delete_button = tk.Button(self.delete_frame, text="Delete Password", command=self.delete_password)
        self.delete_button.grid(row=1, columnspan=2, pady=5)

    def add_password(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if site and username and password:
            self.password_manager.add_password(site, username, password)
            messagebox.showinfo("Success", f"Password for {site} added/updated successfully.")
        else:
            messagebox.showwarning("Error", "All fields must be filled out.")

    def get_password(self):
        site = self.get_site_entry.get()
        credentials = self.password_manager.get_password(site)

        if credentials:
            messagebox.showinfo(f"Password for {site}", f"Username: {credentials['username']}\nPassword: {credentials['password']}")
        else:
            messagebox.showwarning("Error", f"No credentials found for {site}.")

    def delete_password(self):
        site = self.delete_site_entry.get()

        if site:
            self.password_manager.delete_password(site)
            messagebox.showinfo("Success", f"Password for {site} deleted successfully.")
        else:
            messagebox.showwarning("Error", "Site must be provided.")
        

if __name__ == "__main__":
    root = tk.Tk()
    password_manager = PasswordManager()
    app = PasswordManagerGUI(root, password_manager)
    root.mainloop()

