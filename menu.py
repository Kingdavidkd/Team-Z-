import tkinter as tk
from tkinter import Menu, messagebox
from Students import open_student_management  # Import the function from student.py
from view_course import open_course_view  # Import the function from course.py
from view_grades import open_display_search_grades  # Import the function from course.py

# Function to handle Home action


def create_main_window():
    root = tk.Tk()
    root.title("University ABC System")
    root.geometry("1400x1000")

    # Create a menu bar
    menu_bar = Menu(root)

    # Create the "Home" menu item
    menu_bar.add_command(label="Home")

    # Create the "Management" menu
    management_menu = Menu(menu_bar, tearoff=0)
    management_menu.add_command(label="View Course", command=open_course_view)  # Link to student.py
    management_menu.add_command(label="View Grade", command=open_display_search_grades)  # Link to course.py

    # Add the management menu to the menu bar
    menu_bar.add_cascade(label="View option", menu=management_menu)

    # Configure the menu bar
    root.config(menu=menu_bar)

    # Replace all pack with grid for consistency
    tk.Label(root, text="   ", font=("Times new roman", 50), fg="blue").grid(row=0, column=0, columnspan=6, pady=1)

    tk.Label(root, text="     Welcome to the University ABC System", font=("Times new roman", 50), fg="blue").grid(row=2,
                                                                                                               column=3,
                                                                                                               columnspan=6,
                                                                                                               pady=1)

    tk.Label(root, text="   ", font=("Times new roman", 50), fg="blue").grid(row=3, column=0, columnspan=6, pady=1)

    tk.Label(root, text="Our Motto is", font=("Times new roman", 50), fg="blue").grid(row=4, column=8, columnspan=6,
                                                                                      pady=1, sticky="ew")

    tk.Label(root, text="   ", font=("Times new roman", 50), fg="blue").grid(row=5, column=0, columnspan=6, pady=1)

    tk.Label(root, text="'Better education for better future'", font=("Times new roman", 50), fg="blue").grid(row=6,
                                                                                                                 column=8,
                                                                                                                 columnspan=6,
                                                                                                                 pady=1,
                                                                                                                 sticky="ew")

    root.mainloop()  # Start the main event loop

# Run the application
if __name__ == "__main__":
    create_main_window()