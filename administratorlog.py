import tkinter as tk
from tkinter import messagebox
import mysql.connector
from main import create_main_window


# Function to connect to the MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="exam"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# Function to open Administrator Login
def open_admin_login():
    login_window = tk.Toplevel()
    login_window.title("Administrator Login")
    login_window.geometry("1450x700")

    tk.Label(login_window, text="Administrator Login", font=("Arial", 14), fg="blue").pack(pady=10)

    tk.Label(login_window, text="Email:").pack(pady=5)
    global entry_email
    entry_email = tk.Entry(login_window, width=30)
    entry_email.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(login_window, show="*", width=30)
    entry_password.pack(pady=5)

    # Pass login_window to login_admin using a lambda function
    tk.Button(login_window, text="Login", command=lambda: login_admin(login_window), width=15).pack(pady=20)


# Function to handle the login of an administrator
def login_admin(login_window):
    email = entry_email.get()
    password = entry_password.get()

    # Simple validation
    if not email or not password:
        messagebox.showwarning("Warning", "Please enter both email and password.")
        return

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM administrators WHERE email = %s AND password = %s", (email, password))
            admin = cursor.fetchone()
            if admin:
                open_main_app(login_window)  # Pass the login window to close it
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()


# Function to navigate to the main application
def open_main_app(login_window):
    # Close the login window
    login_window.destroy()

    # Open the main application
    create_main_window()  # Call the main application (from main.py)

    # Title Label
    tk.Label(login_window, text="Administrator Login", font=("Times new roman", 14)).pack(pady=10)

    # Email Input
    tk.Label(login_window, text="Email:").pack(pady=5)
    global entry_email
    entry_email = tk.Entry(login_window, width=30)
    entry_email.pack(pady=5)

    # Password Input
    tk.Label(login_window, text="Password:").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(login_window, show="*", width=30)
    entry_password.pack(pady=5)

    # Login Button
    tk.Button(login_window, text="Login", command=login_admin, width=15).pack(pady=20)


# Function to open the main menu
def main():
    root = tk.Tk()
    root.title("University Management System")
    root.geometry("400x300")

    # Title Label
    title_label = tk.Label(root, text="Welcome to the University Management System", font=("Arial", 14))
    title_label.pack(pady=20)

    # Buttons for various options
    '''btn_admin_registration = tk.Button(root, text="Administrator Registration", command=open_admin_registration,
                                       width=30)
    btn_admin_registration.pack(pady=5)'''

    btn_admin_login = tk.Button(root, text="Administrator Login", command=open_admin_login, width=30)
    btn_admin_login.pack(pady=5)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()