import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
def create_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='exam',
            user='root',
            password=''
        )
        return conn
    except Error as e:
        print(f"Error: '{e}'")
    return conn

# Function to view courses in the Treeview
def view_courses(course_tree):
    for item in course_tree.get_children():
        course_tree.delete(item)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, course_name, course_code, credits FROM courses")
        for row in cursor.fetchall():
            course_tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

# Search course
def search_course(entry_search, course_tree):
    search_term = entry_search.get()
    for row in course_tree.get_children():
        course_tree.delete(row)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM courses WHERE course_name LIKE %s OR course_code LIKE %s"
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        results = cursor.fetchall()
        for row in results:
            course_tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to the database.")

# Open Course View window
def open_course_view():
    course_window = tk.Toplevel()
    course_window.title("Available Courses")
    course_window.geometry("1450x800")

    # Add a label for the title
    tk.Label(course_window, text="Available Courses", font=("Times new roman", 18), fg="blue").pack(pady=10)

    # Search functionality
    tk.Label(course_window, text="Search Course:").pack(pady=5)
    entry_search = tk.Entry(course_window)
    entry_search.pack(pady=5)

    tk.Button(course_window, text="Search", command=lambda: search_course(entry_search, course_tree)).pack(pady=10)

    # Define custom style for the Treeview headings
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Times new roman", 12), foreground="blue")

    # Treeview for displaying courses
    columns = ("ID", "Course Name", "Course Code", "Credits")
    course_tree = ttk.Treeview(course_window, columns=columns, show="headings")

    # Set the heading for each column and center align the text
    for col in columns:
        course_tree.heading(col, text=col)
        course_tree.column(col, anchor='center')  # Center align the column text

    course_tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Load all courses initially
    view_courses(course_tree)

# Example of how to integrate this into your main application
def create_main_window():
    root = tk.Tk()
    root.title("University ABC System")
    root.geometry("1450x800")

    # Create a menu bar
    menu_bar = tk.Menu(root)

    # Create the "Home" menu item
    #menu_bar.add_command(label="Home", command=open_home)

    # Create the "Management" menu
    management_menu = tk.Menu(menu_bar, tearoff=0)
    management_menu.add_command(label="View Courses", command=open_course_view)  # Link to view courses

    # Add the management menu to the menu bar
    menu_bar.add_cascade(label="View Options", menu=management_menu)

    root.config(menu=menu_bar)

    root.mainloop()  # Start the main event loop

# Run the application
if __name__ == "__main__":
    create_main_window()