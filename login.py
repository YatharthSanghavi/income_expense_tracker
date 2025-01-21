import sqlite3
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os

# Establish database connection
db_file = 'finance.db'  # SQLite database file in the same directory
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

# Global variable for root window
root = None

# Function to check if the admin table is empty
def check_admin_table(register_admin_button):
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]
    if count == 0:
        register_admin_button.configure(state=tk.NORMAL)
    else:
        register_admin_button.configure(state=tk.DISABLED)

def login(usn_ent, pwd_ent):
    unm = usn_ent.get()
    pwd = pwd_ent.get()
    
    # First, check the admin table
    sql_admin = "SELECT * FROM admin WHERE username=? AND password=?"
    cursor.execute(sql_admin, (unm, pwd))
    admin_result = cursor.fetchone()
    
    if admin_result:
        CTkMessagebox(title="Success", message=f"Logged in as Admin: {unm}")
        root.after(1000, lambda: close_and_open_admin(unm))
    else:
        # If not an admin, check the normal login table
        sql_user = "SELECT id, username FROM login WHERE username=? AND password=?"
        cursor.execute(sql_user, (unm, pwd))
        user_result = cursor.fetchone()
        
        if user_result:
            user_id, username = user_result
            CTkMessagebox(title="Success", message=f"Logged in successfully as {username}")
            root.after(1000, lambda: close_and_open_dashboard(user_id, username))
        else:
            CTkMessagebox(title="Error", message="Incorrect username or password.")

def close_and_open_dashboard(user_id, username):
    global root
    root.quit()  # Stop the main loop
    root.destroy()  # Destroy the window
    import dashboard
    dashboard.main(user_id, username)

def close_and_open_admin(username):
    global root
    root.quit()  # Stop the main loop
    root.destroy()  # Destroy the window
    import admin
    admin.main(username)

# Function to handle registration of an admin
def register_admin(usn_ent, pwd_ent, register_admin_button):
    unm = usn_ent.get()
    pwd = pwd_ent.get()
    
    cursor.execute("SELECT * FROM admin WHERE username=?", (unm,))
    result = cursor.fetchone()
    
    if result:
        CTkMessagebox(title="Error", message="Admin already exists with this username.")
    else:
        sql = "INSERT INTO admin(username, password) VALUES(?, ?)"
        cursor.execute(sql, (unm, pwd))
        conn.commit()
        CTkMessagebox(title="Success", message=f"Admin registration successful for {unm}")
        register_admin_button.configure(state=tk.DISABLED)
        usn_ent.delete(0, tk.END)
        pwd_ent.delete(0, tk.END)

# Function to handle user registration (normal users)
def register_user(usn_ent, pwd_ent):
    unm = usn_ent.get()
    pwd = pwd_ent.get()
    role = 'user'  # By default, register users as 'user'
    cursor.execute("SELECT * FROM login WHERE username=?", (unm,))
    result = cursor.fetchone()
    
    if result:
        CTkMessagebox(title="Error", message="Username already exists. Please choose a different username.")
    else:
        sql = "INSERT INTO login(username, password) VALUES(?, ?)"
        cursor.execute(sql, (unm, pwd))
        conn.commit()
        CTkMessagebox(title="Success", message=f"Registration successful for {unm}")
        usn_ent.delete(0, tk.END)
        pwd_ent.delete(0, tk.END)

# Create main window with dark theme
ctk.set_appearance_mode("dark")  # Set appearance mode to dark
ctk.set_default_color_theme("dark-blue")  # Set the color theme

def main():
    global root
    create_tables()
    root = ctk.CTk()  # Create main window using customtkinter
    root.geometry("400x400")
    root.resizable(False, False)
    root.title("Login")

    # Labels and Entry widgets for username and password
    username_label = ctk.CTkLabel(root, text="Username:", font=("Helvetica", 15, "bold"))
    username_label.grid(row=1, column=0, padx=20, pady=(40, 10), sticky="e")

    password_label = ctk.CTkLabel(root, text="Password:", font=("Helvetica", 15, "bold"))
    password_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="e")

    usn_ent = ctk.CTkEntry(root, width=250)  # Use CTkEntry instead of Entry
    usn_ent.grid(row=1, column=1, padx=20, pady=(40, 10))

    pwd_ent = ctk.CTkEntry(root, show='*', width=250)  # Use CTkEntry instead of Entry
    pwd_ent.grid(row=2, column=1, padx=20, pady=(10, 5))

    # Buttons for login and registration
    login_button = ctk.CTkButton(root, text="Login", command=lambda: login(usn_ent, pwd_ent), width=150, font=("Helvetica", 15, "bold"))  # Use CTkButton instead of Button
    login_button.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

    register_user_button = ctk.CTkButton(root, text="Register User", command=lambda: register_user(usn_ent, pwd_ent), width=150, font=("Helvetica", 15, "bold"))  # Use CTkButton instead of Button
    register_user_button.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

    # Admin Registration Button
    register_admin_button = ctk.CTkButton(root, text="Register Admin", command=lambda: register_admin(usn_ent, pwd_ent, register_admin_button), width=150, font=("Helvetica", 15, "bold"), state=tk.DISABLED)
    register_admin_button.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

    # Check if admin exists and enable/disable the button accordingly
    check_admin_table(register_admin_button)

    root.mainloop()

# Main loop to run the application
if __name__ == "__main__":
    main()