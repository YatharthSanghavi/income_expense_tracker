import sqlite3
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkFrame, CTkTabview
from CTkMessagebox import CTkMessagebox
import os

# Establish database connection
db_file = 'finance.db'  # SQLite database file in the same directory
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
cursor = conn.cursor()

# Set the color theme
ctk.set_appearance_mode("Dark")

def view_users():
    # Clear the content frame
    for widget in users_content.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM login")
    users = cursor.fetchall()
    
    if users:
        for i, user in enumerate(users):
            username = user[1]
            CTkLabel(users_content, text=f"User {i+1}: {username}", font=("Arial", 16)).grid(row=i, column=0, padx=10, pady=10)
            delete_button = CTkButton(users_content, text="Delete", command=lambda u=username: delete_user(u))
            delete_button.grid(row=i, column=1, padx=10, pady=10)
    else:
        CTkLabel(users_content, text="No users found.", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10)

def delete_user(username):
    cursor.execute("DELETE FROM login WHERE username=?", (username,))
    conn.commit()
    CTkMessagebox(title="Success", message=f"User {username} deleted successfully!", icon="check")
    view_users()

def add_user():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        cursor.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        CTkMessagebox(title="Success", message=f"User {username} added successfully!", icon="check")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        CTkMessagebox(title="Error", message="Username and password cannot be empty!", icon="cancel")

def handle_action():
    current_tab = tab_view.get()
    
    if current_tab == "Users":
        view_users()
    elif current_tab == "Exit":
        exit()


# Create the main application window
root = CTk()
root.geometry("800x600")
root.title("Admin Dashboard")

# Create the tab view
tab_view = CTkTabview(root, width=800, height=600, command=handle_action)
tab_view.pack(fill="both", expand=True)

# Create tabs
users_tab = tab_view.add("Users")
add_user_tab = tab_view.add("Add User")
exit_tab = tab_view.add("Exit")

# Create content frames for each tab
users_content = CTkFrame(users_tab, corner_radius=10, fg_color="#2b2b2b")
users_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

add_user_content = CTkFrame(add_user_tab, corner_radius=10, fg_color="#2b2b2b")
add_user_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

exit_content = CTkFrame(exit_tab, corner_radius=10, fg_color="#2b2b2b")
exit_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Add User Section in Add User Tab
username_label = CTkLabel(add_user_content, text="Username:", font=("Arial", 14))
username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

username_entry = CTkEntry(add_user_content)
username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

password_label = CTkLabel(add_user_content, text="Password:", font=("Arial", 14))
password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

password_entry = CTkEntry(add_user_content, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

add_user_button = CTkButton(add_user_content, text="Add User", command=add_user)
add_user_button.grid(row=3, column=0, columnspan=2, pady=20)

# Configure grid for all tabs
for tab in (users_tab, add_user_tab, exit_tab):
    tab.grid_rowconfigure(0, weight=1)
    tab.grid_columnconfigure(0, weight=1)

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Initial setup
handle_action()

# Start the main loop
root.mainloop()
