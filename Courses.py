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

# Function to clear course input fields
def clear_course_fields(entry_course_name, entry_course_code, entry_credits):
    entry_course_name.delete(0, tk.END)
    entry_course_code.delete(0, tk.END)
    entry_credits.delete(0, tk.END)

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

# Add course
def add_course(entry_course_name, entry_course_code, entry_credits, course_tree):
    course_name = entry_course_name.get()
    course_code = entry_course_code.get()
    credits = entry_credits.get()

    if course_name and course_code and credits.isdigit():
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)",
                               (course_name, course_code, int(credits)))
                conn.commit()
                messagebox.showinfo("Success", "Course added successfully!")
                clear_course_fields(entry_course_name, entry_course_code, entry_credits)
                view_courses(course_tree)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields correctly.")

# Update course
def update_course(entry_course_name, entry_course_code, entry_credits, course_tree):
    selected_item = course_tree.selection()
    if selected_item:
        course_id = course_tree.item(selected_item)['values'][0]
        course_name = entry_course_name.get()
        course_code = entry_course_code.get()
        credits = entry_credits.get()

        if course_name and course_code and credits.isdigit():
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE courses SET course_name = %s, course_code = %s, credits = %s WHERE id = %s",
                                   (course_name, course_code, int(credits), course_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Course updated successfully!")
                    clear_course_fields(entry_course_name, entry_course_code, entry_credits)
                    view_courses(course_tree)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields correctly.")
    else:
        messagebox.showwarning("Warning", "Select a course to update.")

# Delete course
def delete_course(course_tree):
    selected_item = course_tree.selection()
    if selected_item:
        course_id = course_tree.item(selected_item)['values'][0]
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
                conn.commit()
                messagebox.showinfo("Success", "Course deleted successfully!")
                view_courses(course_tree)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning", "Select a course to delete.")

# Select course for editing
def select_course(event, course_tree, entry_course_name, entry_course_code, entry_credits):
    selected_item = course_tree.selection()
    if selected_item:
        course = course_tree.item(selected_item)['values']
        entry_course_name.delete(0, tk.END)
        entry_course_name.insert(0, course[1])
        entry_course_code.delete(0, tk.END)
        entry_course_code.insert(0, course[2])
        entry_credits.delete(0, tk.END)
        entry_credits.insert(0, course[3])


def enroll_student(entry_student_id, course_tree):
    student_id = entry_student_id.get()
    selected_item = course_tree.selection()

    if selected_item and student_id.isdigit():
        course_id = course_tree.item(selected_item)['values'][0]
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)",
                               (int(student_id), course_id))
                conn.commit()
                messagebox.showinfo("Success", "Student enrolled in course successfully!")
                entry_student_id.delete(0, tk.END)  # Clear the entry field
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning", "Select a course and enter a valid student ID.")

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

# Function to enroll a student (placeholder)
'''def enroll_student():
    student_id = entry_student_id.get()
    # Here you would add the logic to enroll the student in the course
    if student_id:
        # Example logic (you can replace this with actual database logic)
        messagebox.showinfo("Success", f"Student ID {student_id} enrolled successfully.")
        entry_student_id.delete(0, tk.END)  # Clear the entry field
    else:
        messagebox.showerror("Error", "Please enter a Student ID.")'''

# Open Course Management window
def open_course_management():
    course_window = tk.Toplevel()
    course_window.title("Course Management")
    course_window.geometry("1400x1000")

    # Add a label for the title
    tk.Label(course_window, text="Course Management", font=("Times new roman", 18), fg="blue").grid(row=0, column=0, columnspan=6, pady=10)

    # Course management UI
    tk.Label(course_window, text="Course Name").grid(row=1, column=0)
    entry_course_name = tk.Entry(course_window, width=30)
    entry_course_name.grid(row=1, column=1)

    tk.Label(course_window, text="Course Code").grid(row=2, column=0)
    entry_course_code = tk.Entry(course_window, width=30)
    entry_course_code.grid(row=2, column=1)

    tk.Label(course_window, text="Credits").grid(row=3, column=0)
    entry_credits = tk.Entry(course_window, width=30)
    entry_credits.grid(row=3, column=1)

    # Search functionality
    tk.Label(course_window, text="Search course").grid(row=1, column=4)
    entry_search = tk.Entry(course_window)
    entry_search.grid(row=1, column=5)
    tk.Button(course_window, text="Search Course", command=lambda: search_course(entry_search, course_tree)).grid(row=5, column=5)

    # Buttons for course management
    tk.Button(course_window, text="Add Course", command=lambda: add_course(entry_course_name, entry_course_code, entry_credits, course_tree)).grid(row=5, column=0)
    tk.Button(course_window, text="Update Course", command=lambda: update_course(entry_course_name, entry_course_code, entry_credits, course_tree)).grid(row=5, column=1)
    tk.Button(course_window, text="Delete Course", command=lambda: delete_course(course_tree)).grid(row=5, column=2)

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

    # Adjust the grid placement as needed
    course_tree.grid(row=10, column=0, columnspan=6)

    # Bind selection event to handle row selection
    course_tree.bind("<<TreeviewSelect>>",
                     lambda event: select_course(event, course_tree, entry_course_name, entry_course_code,
                                                 entry_credits))

    # Student Enrollment Section
    tk.Label(course_window, text="Student ID:").grid(row=18, column=0, padx=10, pady=10)
    entry_student_id = tk.Entry(course_window)
    entry_student_id.grid(row=18, column=1)

    # Modify the button command to pass parameters
    tk.Button(course_window, text="Enroll Student", command=lambda: enroll_student(entry_student_id, course_tree)).grid(
        row=18, column=2)
    # Function to view courses (assuming it's defined elsewhere)
    view_courses(course_tree)