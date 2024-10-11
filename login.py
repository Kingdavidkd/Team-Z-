import tkinter as tk
from tkinter import messagebox
from administratorreg import open_admin_registration  # Import the function from administratorreg.py
from administratorlog import open_admin_login  # Import the function from administratorlog.py
from studentreg import open_student_registration  # Import the function from administratorreg.py
from studentlog import open_student_login  # Import the function from administratorreg.py

# Main application window
def main():
    root = tk.Tk()
    root.title("University ABC Management System")
    root.geometry("1450x800")

    # Title Label
    title_label = tk.Label(root, text="Welcome to the University ABC Management System", font=("Times new roman", 16), fg="blue")
    title_label.pack(pady=20)

    # Buttons for various options
    btn_admin_registration = tk.Button(root, text="Administrator Registration", command=open_admin_registration, width=30)
    btn_admin_registration.pack(pady=5)

    btn_student_registration = tk.Button(root, text="Student Registration", command=open_student_registration, width=30)
    btn_student_registration.pack(pady=5)

    btn_admin_login = tk.Button(root, text="Administrator Login", command=open_admin_login, width=30)
    btn_admin_login.pack(pady=5)

    btn_student_login = tk.Button(root, text="Student Login", command=open_student_login, width=30)
    btn_student_login.pack(pady=5)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()