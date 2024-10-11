# student.py
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

# Add student
def add_student(tree, entry_name, entry_age, entry_enrollment_number):
    name = entry_name.get()
    age = entry_age.get()
    enrollment_number = entry_enrollment_number.get()

    if name and age and enrollment_number:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO students (name, age, enrollment_number) VALUES (%s, %s, %s)",
                               (name, age, enrollment_number))
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully!")
                clear_fields(entry_name, entry_age, entry_enrollment_number)
                view_students(tree)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Update student
def update_student(tree, entry_name, entry_age, entry_enrollment_number):
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item)['values'][0]
        name = entry_name.get()
        age = entry_age.get()
        enrollment_number = entry_enrollment_number.get()

        if name and age and enrollment_number:
            # Ask for confirmation before updating
            confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this student record?")
            if confirm:  # Proceed only if the user confirms
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("UPDATE students SET name = %s, age = %s, enrollment_number = %s WHERE id = %s",
                                       (name, age, enrollment_number, student_id))
                        conn.commit()
                        messagebox.showinfo("Success", "Student updated successfully!")
                        clear_fields(entry_name, entry_age, entry_enrollment_number)
                        view_students(tree)
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"Error: {err}")
                    finally:
                        cursor.close()
                        conn.close()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")
    else:
        messagebox.showwarning("Warning", "Select a student to update.")

# Delete student
def delete_student(tree):
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item)['values'][0]
        # Ask for confirmation before deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
        if confirm:  # Proceed only if the user confirms
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    view_students(tree)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()
    else:
        messagebox.showwarning("Warning", "Select a student to delete.")

# View students
def view_students(tree):
    for row in tree.get_children():
        tree.delete(row)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

# Clear fields
def clear_fields(entry_name, entry_age, entry_enrollment_number):
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_enrollment_number.delete(0, tk.END)

# Select student for editing
def select_student(event, tree, entry_name, entry_age, entry_enrollment_number):
    selected_item = tree.selection()
    if selected_item:
        student = tree.item(selected_item)['values']
        entry_name.delete(0, tk.END)
        entry_name.insert(0, student[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, student[2])
        entry_enrollment_number.delete(0, tk.END)
        entry_enrollment_number.insert(0, student[3])

# Search student
def search_student(tree, entry_search):
    search_term = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM students WHERE name LIKE %s OR enrollment_number LIKE %s"
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

# Open Student Management window
def open_student_management():
    student_window = tk.Toplevel()
    student_window.title("Student Management")
    student_window.geometry("1400x1000")

    # Add a label for the title
    tk.Label(student_window, text="Student Management", font=("Times new roman", 18), fg="blue").grid(row=0, column=0, columnspan=6, pady=10)

    # Labels and Entries
    tk.Label(student_window, text="Name").grid(row=1, column=0)
    entry_name = tk.Entry(student_window, width=30)
    entry_name.grid(row=1, column=1)

    tk.Label(student_window, text="Age").grid(row=2, column=0)
    entry_age = tk.Entry(student_window, width=30)
    entry_age.grid(row=2, column=1)

    tk.Label(student_window, text="Enrollment Number").grid(row=3, column=0)
    entry_enrollment_number = tk.Entry(student_window, width=30)
    entry_enrollment_number.grid(row=3, column=1)

    # Search functionality
    tk.Label(student_window, text="Search").grid(row=1, column=4)
    entry_search = tk.Entry(student_window)
    entry_search.grid(row=1, column=5)
    tk.Button(student_window, text="Search Student", command=lambda: search_student(tree, entry_search)).grid(row=6, column=5)

    # Buttons
    tk.Button(student_window, text="Add Student", command=lambda: add_student(tree, entry_name, entry_age, entry_enrollment_number)).grid(row=6, column=0)
    tk.Button(student_window, text="Update Student", command=lambda: update_student(tree, entry_name, entry_age, entry_enrollment_number)).grid(row=6, column=1)
    tk.Button(student_window, text="Delete Student", command=lambda: delete_student(tree)).grid(row=6, column=2)

    # Define custom style for the Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Times new roman", 12), foreground="blue")  # Change font size and color

    # Treeview for displaying students with center-aligned columns
    columns = ("ID", "Name", "Age", "Enrollment Number")
    tree = ttk.Treeview(student_window, columns=columns, show="headings")

    # Set the heading for each column and center align the text
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')  # Center align the column text

    # Adjust the grid placement as needed
    tree.grid(row=8, column=0, columnspan=17)

    # Bind selection event to handle row selection
    tree.bind("<<TreeviewSelect>>",
              lambda event: select_student(event, tree, entry_name, entry_age, entry_enrollment_number))

    # Function to view students (assuming it's defined elsewhere)
    view_students(tree)