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

# Function to fetch student IDs and names for the ComboBox
def fetch_student_ids():
    conn = create_connection()
    student_data = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students")  # Assuming 'name' is a field in the 'students' table
        for row in cursor.fetchall():
            student_data.append((row[0], row[1]))  # (ID, Name)
        cursor.close()
        conn.close()
    return student_data

# Function to fetch course IDs and names for the ComboBox
def fetch_course_ids():
    conn = create_connection()
    course_data = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, course_name FROM courses")  # Assuming 'course_name' is a field in the 'courses' table
        for row in cursor.fetchall():
            course_data.append((row[0], row[1]))  # (ID, Course Name)
        cursor.close()
        conn.close()
    return course_data

# Function to clear input fields
def clear_grade_fields(combo_student_id, combo_course_id, entry_grade):
    combo_student_id.set('')  # Clear ComboBox selection
    combo_course_id.set('')    # Clear ComboBox selection
    entry_grade.delete(0, tk.END)

# Function to add or update grades
def save_grade(combo_student_id, combo_course_id, entry_grade, grade_tree):
    student_id = combo_student_id.get().split(" ")[0]  # Get the ID from the selected value
    course_id = combo_course_id.get().split(" ")[0]    # Get the ID from the selected value
    grade = entry_grade.get()

    if student_id.isdigit() and course_id.isdigit() and grade.replace('.', '', 1).isdigit():
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Check if the grade record already exists
                cursor.execute("SELECT id FROM grades WHERE student_id = %s AND course_id = %s",
                               (student_id, course_id))
                result = cursor.fetchone()

                if result:  # Update existing grade
                    cursor.execute("UPDATE grades SET grade = %s WHERE student_id = %s AND course_id = %s",
                                   (float(grade), student_id, course_id))
                    messagebox.showinfo("Success", "Grade updated successfully!")
                else:  # Insert new grade
                    cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)",
                                   (student_id, course_id, float(grade)))
                    messagebox.showinfo("Success", "Grade added successfully!")

                conn.commit()
                clear_grade_fields(combo_student_id, combo_course_id, entry_grade)
                view_grades(grade_tree)  # Refresh the grades view
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields correctly.")

# Function to view grades in the Treeview
def view_grades(grade_tree):
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
        cursor.execute(query)
        for row in cursor.fetchall():
            grade_tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

# Open Grades Management window
def open_grades_management():
    grades_window = tk.Toplevel()
    grades_window.title("Grades Management")
    grades_window.geometry("1450x800")

    # Add a label for the title
    tk.Label(grades_window, text="Grades Management", font=("Times new roman", 18), fg="blue").pack(pady=10)

    # Fetch student IDs and names for ComboBox
    student_data = fetch_student_ids()
    course_data = fetch_course_ids()

    # Search field
    tk.Label(grades_window, text="Search by Student or Course Name:").pack(anchor='w', padx=10)
    search_entry = tk.Entry(grades_window)
    search_entry.pack(padx=10, pady=5)

    # Input fields for student ID (ComboBox), course ID (ComboBox), and grade
    tk.Label(grades_window, text="Student").pack(anchor='w', padx=10, pady=5)
    combo_student_id = ttk.Combobox(grades_window, values=[f"{id} {name}" for id, name in student_data])
    combo_student_id.pack(padx=10, pady=5)

    tk.Label(grades_window, text="Course").pack(anchor='w', padx=10, pady=5)
    combo_course_id = ttk.Combobox(grades_window, values=[f"{id} {name}" for id, name in course_data])
    combo_course_id.pack(padx=10, pady=5)

    tk.Label(grades_window, text="Grade").pack(anchor='w', padx=10, pady=5)
    entry_grade = tk.Entry(grades_window)
    entry_grade.pack(padx=10, pady=5)

    # Buttons for saving grades and searching
    tk.Button(grades_window, text="Save Grade",
              command=lambda: save_grade(combo_student_id, combo_course_id, entry_grade, grade_tree)).pack(pady=10)

    # Treeview for displaying grades
    columns = ("ID", "Student ID", "Student Name", "Course ID", "Course Name", "Grade")
    grade_tree = ttk.Treeview(grades_window, columns=columns, show="headings")

    # Set the heading for each column
    for col in columns:
        grade_tree.heading(col, text=col)
        grade_tree.column(col, anchor='center')

    grade_tree.pack(pady=20, fill=tk.BOTH, expand=True)

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
    management_menu.add_command(label="Grades Management", command=open_grades_management)  # Link to grades management

    # Add the management menu to the menu bar
    menu_bar.add_cascade(label="Management", menu=management_menu)

    root.config(menu=menu_bar)

    root.mainloop()  # Start the main event loop

# Run the application
if __name__ == "__main__":
    create_main_window()