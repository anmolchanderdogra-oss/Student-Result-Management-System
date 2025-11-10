import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- Database Setup ----------------
conn = sqlite3.connect("student_results.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    subject1 INTEGER,
    subject2 INTEGER,
    subject3 INTEGER,
    total INTEGER,
    average REAL,
    grade TEXT
)
""")
conn.commit()

# ---------------- Helper Functions ----------------
def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sub1_entry.delete(0, tk.END)
    sub2_entry.delete(0, tk.END)
    sub3_entry.delete(0, tk.END)

def calculate_grade(total):
    if total >= 270:
        return "A+"
    elif total >= 240:
        return "A"
    elif total >= 200:
        return "B"
    elif total >= 150:
        return "C"
    else:
        return "Fail"

def add_result():
    name = name_entry.get()
    roll = roll_entry.get()
    try:
        sub1 = int(sub1_entry.get())
        sub2 = int(sub2_entry.get())
        sub3 = int(sub3_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid marks (numbers only)!")
        return

    if name == "" or roll == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    total = sub1 + sub2 + sub3
    avg = total / 3
    grade = calculate_grade(total)

    cursor.execute("""
        INSERT INTO results (name, roll_no, subject1, subject2, subject3, total, average, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, roll, sub1, sub2, sub3, total, avg, grade))
    conn.commit()

    messagebox.showinfo("Success", "Result Added Successfully!")
    clear_fields()
    view_results()

def view_results():
    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()
    result_table.delete(*result_table.get_children())
    for row in rows:
        result_table.insert("", tk.END, values=row)

def get_selected_row(event):
    selected = result_table.focus()
    data = result_table.item(selected)
    row = data["values"]
    if row:
        clear_fields()
        name_entry.insert(0, row[1])
        roll_entry.insert(0, row[2])
        sub1_entry.insert(0, row[3])
        sub2_entry.insert(0, row[4])
        sub3_entry.insert(0, row[5])

def update_result():
    selected = result_table.focus()
    data = result_table.item(selected)
    row = data["values"]
    if not row:
        messagebox.showerror("Error", "No record selected!")
        return

    try:
        sub1 = int(sub1_entry.get())
        sub2 = int(sub2_entry.get())
        sub3 = int(sub3_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid marks!")
        return

    total = sub1 + sub2 + sub3
    avg = total / 3
    grade = calculate_grade(total)

    cursor.execute("""
        UPDATE results SET name=?, roll_no=?, subject1=?, subject2=?, subject3=?, total=?, average=?, grade=? WHERE id=?
    """, (name_entry.get(), roll_entry.get(), sub1, sub2, sub3, total, avg, grade, row[0]))
    conn.commit()
    messagebox.showinfo("Success", "Result Updated Successfully!")
    view_results()

def delete_result():
    selected = result_table.focus()
    data = result_table.item(selected)
    row = data["values"]
    if not row:
        messagebox.showerror("Error", "No record selected!")
        return

    cursor.execute("DELETE FROM results WHERE id=?", (row[0],))
    conn.commit()
    messagebox.showinfo("Success", "Result Deleted Successfully!")
    view_results()
    clear_fields()

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("850x550")
root.config(bg="#f0f0f0")

tk.Label(root, text="🎓 Student Result Management System", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10).pack(fill=tk.X)

# ---------- Input Frame ----------
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Roll No:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
roll_entry = tk.Entry(frame, font=("Arial", 12))
roll_entry.grid(row=1, column=1, padx=10)

tk.Label(frame, text="Subject 1 Marks:", font=("Arial", 12)).grid(row=0, column=2, sticky="w", pady=5)
sub1_entry = tk.Entry(frame, font=("Arial", 12))
sub1_entry.grid(row=0, column=3, padx=10)

tk.Label(frame, text="Subject 2 Marks:", font=("Arial", 12)).grid(row=1, column=2, sticky="w", pady=5)
sub2_entry = tk.Entry(frame, font=("Arial", 12))
sub2_entry.grid(row=1, column=3, padx=10)

tk.Label(frame, text="Subject 3 Marks:", font=("Arial", 12)).grid(row=2, column=2, sticky="w", pady=5)
sub3_entry = tk.Entry(frame, font=("Arial", 12))
sub3_entry.grid(row=2, column=3, padx=10)

# ---------- Buttons ----------
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Result", width=12, bg="#4CAF50", fg="white", command=add_result).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update", width=12, bg="#2196F3", fg="white", command=update_result).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete", width=12, bg="#f44336", fg="white", command=delete_result).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Clear", width=12, bg="#9E9E9E", fg="white", command=clear_fields).grid(row=0, column=3, padx=10)

# ---------- Table ----------
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("ID", "Name", "Roll No", "Sub1", "Sub2", "Sub3", "Total", "Average", "Grade")
result_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    result_table.heading(col, text=col)
    result_table.column(col, width=90)
result_table.pack(fill=tk.X)

result_table.bind("<ButtonRelease-1>", get_selected_row)

view_results()

root.mainloop()
