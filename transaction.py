import tkinter as tk
import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame
from CTkMessagebox import CTkMessagebox
import sqlite3
from tkcalendar import DateEntry
import os

db_file = 'finance.db'  # SQLite database file in the same directory
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
cursor = conn.cursor()

def disable_event():
    pass

class TransactionWindow(CTk):
    def __init__(self, user_id, username, dashboard_callback):
        super().__init__()
        self.title(f"Transactions - {username}")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", disable_event)

        self.user_id = user_id
        self.username = username
        self.dashboard_callback = dashboard_callback
        self.setup_ui()

    def setup_ui(self):
        self.frame = CTkFrame(self, corner_radius=10, fg_color="#2b2b2b")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = CTkLabel(self.frame, text="Your Transactions", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Fetch all transactions
        cursor.execute("""
            SELECT 'Income' AS type, amount, description, date 
            FROM income 
            WHERE user_id = ?
            UNION ALL 
            SELECT 'Expense' AS type, amount, description, date 
            FROM expense 
            WHERE user_id = ?
            ORDER BY date
        """, (self.user_id, self.user_id))
        transactions = cursor.fetchall()

        # Display transactions in a table
        columns = ("Type", "Amount", "Description", "Date")
        self.tree = tk.Listbox(self.frame, width=80, height=20, font=("Arial", 12))
        
        # Insert column headers
        self.tree.insert(tk.END, f"{columns[0]:<10}{columns[1]:<15}{columns[2]:<30}{columns[3]:<20}")

        # Insert data into the table
        total_income = 0
        total_expense = 0
        for transaction in transactions:
            transaction_type, amount, description, date = transaction
            self.tree.insert(tk.END, f"{transaction_type:<10}{amount:<15}{description:<30}{date:<20}")
            try:
                amount = float(amount)  # Convert amount to float
                if transaction_type == 'Income':
                    total_income += amount
                else:
                    total_expense += amount
            except ValueError:
                print(f"Invalid amount value: {amount}")  # For debugging

        # Pack the listbox into the frame
        self.tree.pack(fill="both", expand=True)

        # Display totals
        self.total_label = CTkLabel(self.frame, text=f"Total Income: ${total_income:.2f}    Total Expense: ${total_expense:.2f}    Net Total: ${total_income - total_expense:.2f}", font=("Arial", 16, "bold"))
        self.total_label.pack(pady=10)

        # Back button
        self.back_button = CTkButton(self.frame, text="Back to Dashboard", command=self.back_to_dashboard)
        self.back_button.pack(pady=20)
                
    def back_to_dashboard(self):
        self.destroy()
        self.dashboard_callback(self.user_id, self.username)

def get_user_id(self, username):
    cursor.execute("SELECT id FROM login WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def main(user_id, username, dashboard_callback):
    app = TransactionWindow(user_id, username, dashboard_callback)
    app.mainloop()

if __name__ == "__main__":
    main(None)  # Call the main function with a default value for logged_in_user