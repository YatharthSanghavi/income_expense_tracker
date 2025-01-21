import tkinter as tk
import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkFrame
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
import sqlite3
import os

# Establish database connection
db_file = 'finance.db'  # SQLite database file in the same directory
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
cursor = conn.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS income 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES login(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expense 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES login(id))''')
    conn.commit()

# Set the color theme
ctk.set_appearance_mode("Dark")

def disable_event():
    pass

def create_dashboard(user_id, username):
    # Create the main application window
    root = CTk()
    root.geometry("800x600")
    root.title(f"Dashboard - {username}")
    root.protocol("WM_DELETE_WINDOW", disable_event)

    # Create validation command
    validate_cmd = root.register(validate_numeric_input)

    # Create the tab view
    tab_view = ctk.CTkTabview(root, width=800, height=600, command=lambda: handle_action(tab_view, income_expense_content, open_content, root, validate_cmd, user_id, username))
    tab_view.pack(fill="both", expand=True)

    # Create tabs
    income_expense_tab = tab_view.add("Income/Expense")
    open_tab = tab_view.add("Transaction")
    exit_tab = tab_view.add("Exit")

    # Create content frames for each tab
    income_expense_content = CTkFrame(income_expense_tab, corner_radius=10, fg_color="#2b2b2b")
    income_expense_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    open_content = CTkFrame(open_tab, corner_radius=10, fg_color="#2b2b2b")
    open_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    exit_content = CTkFrame(exit_tab, corner_radius=10, fg_color="#2b2b2b")
    exit_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Configure grid for all tabs
    for tab in (income_expense_tab, open_tab, exit_tab):
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

    # Initial setup
    handle_action(tab_view, income_expense_content, open_content, root, validate_cmd, user_id, username)

    # Start the main loop
    root.mainloop()


def get_user_id(username):
    cursor.execute("SELECT id FROM login WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def cincome(inc_text_box, dec_text_box, date_entry, user_id):
    amount = inc_text_box.get()
    description = dec_text_box.get()
    date = date_entry.get_date()
    
    try:
        amount = float(amount)  # Convert amount to float
        cursor.execute("INSERT INTO income (amount, description, date, user_id) VALUES (?, ?, ?, ?)", 
                       (amount, description, date, user_id))
        if cursor.rowcount > 0:
            conn.commit()
            CTkMessagebox(title="Success", message="Income added successfully!", icon="check")
            inc_text_box.delete(0, 'end')
            dec_text_box.delete(0, 'end')
            date_entry.set_date(None)
        else:
            CTkMessagebox(title="Error", message="Failed to add income. No rows affected.", icon="cancel")
    except ValueError:
        CTkMessagebox(title="Error", message="Invalid amount. Please enter a valid number.", icon="cancel")

def cexpence(exp_text_box, exp_dec_text_box, exp_date_entry, user_id):
    amount = exp_text_box.get()
    description = exp_dec_text_box.get()
    date = exp_date_entry.get_date()
    
    try:
        amount = float(amount)  # Convert amount to float
        cursor.execute("INSERT INTO expense (amount, description, date, user_id) VALUES (?, ?, ?, ?)", 
                       (amount, description, date, user_id))
        if cursor.rowcount > 0:
            conn.commit()
            CTkMessagebox(title="Success", message="Expense added successfully!", icon="check")
            exp_text_box.delete(0, 'end')
            exp_dec_text_box.delete(0, 'end')
            exp_date_entry.set_date(None)
        else:
            CTkMessagebox(title="Error", message="Failed to add expense. No rows affected.", icon="cancel")
    except ValueError:
        CTkMessagebox(title="Error", message="Invalid amount. Please enter a valid number.", icon="cancel")
        

    
def validate_numeric_input(value):
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function to handle action based on the tab
def handle_action(tab_view, income_expense_content, open_content, root, validate_cmd, user_id, username):
    current_tab = tab_view.get()
    
    if current_tab == "Income/Expense":
        setup_income_expense_tab(income_expense_content, validate_cmd, user_id)
    elif current_tab == "Transaction":
        setup_open_tab(open_content, root, user_id, username)
    elif current_tab == "Exit":
        quit()

def setup_income_expense_tab(income_expense_content, validate_cmd, user_id):
    # Clear the content frame
    for widget in income_expense_content.winfo_children():
        widget.destroy()
    
    #INCOME TAB
    inc = CTkLabel(income_expense_content, text="Income", font=("Arial", 19,"bold"))
    inc.grid(row=0, column=0, padx=10, pady=10)
    income = CTkLabel(income_expense_content, text="Enter Income:", font=("Arial", 16))
    income.grid(row=1, column=0, padx=10, pady=10)
    global inc_text_box
    inc_text_box = CTkEntry(income_expense_content, width=200, height=30, font=("Arial", 16), validate="key", validatecommand=(validate_cmd, '%P'))
    inc_text_box.grid(row=1, column=1, padx=10, pady=10)
    description = CTkLabel(income_expense_content, text="Enter Description:", font=("Arial", 16))
    description.grid(row=3, column=0, padx=10, pady=10)
    global dec_text_box
    dec_text_box = CTkEntry(income_expense_content, width=200, height=30, font=("Arial", 16))
    dec_text_box.grid(row=3, column=1, padx=10, pady=10)
    date = CTkLabel(income_expense_content, text="Date", font=("Arial", 16))
    date.grid(row=5, column=0, padx=10, pady=10)
    global date_entry
    date_entry = DateEntry(income_expense_content)
    date_entry.grid(row=5, column=1, padx=10, pady=10)
    inc_button = CTkButton(income_expense_content, text="Submit", font=("Arial", 16),
                       command=lambda: cincome(inc_text_box, dec_text_box, date_entry, user_id))
    inc_button.grid(row=6, column=1, padx=10, pady=10)

    #EXPENCE TAB
    exp = CTkLabel(income_expense_content, text="Expence", font=("Arial", 19,"bold"))
    exp.grid(row=8, column=0, padx=10, pady=10)
    expence=CTkLabel(income_expense_content,text="Enter Expence:",font=("Arial", 16))
    expence.grid(row=9, column=0,padx=10,pady=10)
    global exp_text_box
    exp_text_box = CTkEntry(income_expense_content, width=200, height=30, font=("Arial", 16), validate="key", validatecommand=(validate_cmd, '%P'))
    exp_text_box.grid(row=9, column=1, padx=10, pady=10)
    exp_desl = CTkLabel(income_expense_content, text="Enter Description:", font=("Arial", 16))
    exp_desl.grid(row=10, column=0, padx=10, pady=10)
    global exp_dec_text_box
    exp_dec_text_box = CTkEntry(income_expense_content, width=200, height=30, font=("Arial", 16))
    exp_dec_text_box.grid(row=10, column=1, padx=10, pady=10)
    exp_date = CTkLabel(income_expense_content, text="Date", font=("Arial", 16))
    exp_date.grid(row=11, column=0, padx=10, pady=10)
    global exp_date_entry
    exp_date_entry = DateEntry(income_expense_content)
    exp_date_entry.grid(row=11, column=1, padx=10, pady=10)
    exp_button = CTkButton(income_expense_content, text="Submit", font=("Arial", 16),
                       command=lambda: cexpence(exp_text_box, exp_dec_text_box, exp_date_entry, user_id))   
    exp_button.grid(row=12, column=1, padx=10, pady=10)

def open_transaction_page(root, user_id, username):
    root.withdraw()  # Hide the main window
    from transaction import main as transaction_main
    transaction_main(user_id, username, lambda uid, uname: back_to_dashboard(root, uid, uname))

def back_to_dashboard(root, user_id, username):
    root.deiconify() 

def setup_open_tab(open_content, root, user_id, username):
    for widget in open_content.winfo_children():
        widget.destroy()
    CTkButton(open_content, text="See Transaction", font=("Arial", 16), 
              command=lambda: open_transaction_page(root, user_id, username)).grid(row=0, column=0, padx=10, pady=10)
 
def main(user_id, username):
    create_table()
    create_dashboard(user_id, username)

if __name__ == "__main__":
    main()