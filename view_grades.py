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

# Function to view grades in the Treeview
def view_grades(grade_tree, filter_text=None):
    for item in grade_tree.get_children():
        grade_tree.delete(item)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        SELECT g.id, s.id AS student_id, s.name AS student_name, c.id AS course_id, c.course_name, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        """
        if filter_text:
            query += " WHERE s.name LIKE %s OR c.course_name LIKE %s"
            cursor.execute(query, (f"%{filter_text}%", f"%{filter_text}%"))
        else:
            cursor.execute(query)

        for row in cursor.fetchall():
            grade_tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

# Open Display and Search Grades window
def open_display_search_grades():
    search_window = tk.Toplevel()
    search_window.title("Display and Search Grades")
    search_window.geometry("1450x800")

    # Add a label for the title
    tk.Label(search_window, text="Display and Search Grades", font=("Times new roman", 18), fg="blue").pack(pady=10)

    # Search field
    tk.Label(search_window, text="Search by Student or Course Name:").pack(pady=5)
    search_entry = tk.Entry(search_window)
    search_entry.pack(pady=5)

    # Treeview for displaying grades
    columns = ("ID", "Student ID", "Student Name", "Course ID", "Course Name", "Grade")
    grade_tree = ttk.Treeview(search_window, columns=columns, show="headings")

    # Set the heading for each column
    for col in columns:
        grade_tree.heading(col, text=col)
        grade_tree.column(col, anchor='center')

    grade_tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Button to search grades
    def search_grades():
        filter_text = search_entry.get()
        view_grades(grade_tree, filter_text)

    tk.Button(search_window, text="Search", command=search_grades).pack(pady=10)

    # Load all grades initially
    view_grades(grade_tree)

# Example of how to integrate this into your main application
def create_main_window():
    root = tk.Tk()
    root.title("University ABC System")
    root.geometry("1450x800")

    # Create a menu bar
    menu_bar = tk.Menu(root)

    # Create the "Management" menu
    management_menu = tk.Menu(menu_bar, tearoff=0)
    #management_menu.add_command(label="Grades Management", command=open_grades_management)  # Link to grades management
    management_menu.add_command(label="Display & Search Grades", command=open_display_search_grades)  # Link to display and search

    # Add the management menu to the menu bar
    menu_bar.add_cascade(label="Management", menu=management_menu)

    root.config(menu=menu_bar)

    root.mainloop()  # Start the main event loop

# Run the application
if __name__ == "__main__":
    create_main_window()