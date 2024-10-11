import tkinter as tk
from tkinter import messagebox
import mysql.connector


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


# Function to handle the registration of an administrator
def register_admin():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    # Simple validation
    if not name or not email or not password:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO administrators (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, password))
            conn.commit()
            messagebox.showinfo("Success", "Administrator registered successfully!")
            clear_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()


# Function to clear the input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)


# Function to open Administrator Registration
def open_admin_registration():
    registration_window = tk.Toplevel()
    registration_window.title("Administrator Registration")
    registration_window.geometry("1450x800")

    # Title Label
    tk.Label(registration_window, text="Administrator Registration", font=("Times new roman", 16), fg="blue").pack(pady=10)

    # Name Input
    tk.Label(registration_window, text="Name:").pack(pady=5)
    global entry_name
    entry_name = tk.Entry(registration_window, width=30)
    entry_name.pack(pady=10)

    # Email Input
    tk.Label(registration_window, text="Email:").pack(pady=5)
    global entry_email
    entry_email = tk.Entry(registration_window, width=30)
    entry_email.pack(pady=5)

    # Password Input
    tk.Label(registration_window, text="Password:").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(registration_window, show="*", width=30)
    entry_password.pack(pady=5)

    # Register Button
    tk.Button(registration_window, text="Register", command=register_admin, width=15).pack(pady=20)


# Function to open the main menu
def main():
    root = tk.Tk()
    root.title("University Management System")
    root.geometry("400x300")

    # Title Label
    title_label = tk.Label(root, text="Welcome to the University Management System", font=("Arial", 14))
    title_label.pack(pady=20)

    # Buttons for various options
    btn_admin_registration = tk.Button(root, text="Administrator Registration", command=open_admin_registration,
                                       width=30)
    btn_admin_registration.pack(pady=5)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()