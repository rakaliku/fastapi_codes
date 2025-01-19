import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

# FastAPI Base URL
BASE_URL = "http://127.0.0.1:8000"

# Functions for API Calls
def get_attendance():
    registration_number = reg_no_entry.get()
    if not registration_number:
        messagebox.showerror("Error", "Registration number is required.")
        return

    try:
        response = requests.get(f"{BASE_URL}/attendance/{registration_number}")
        if response.status_code == 200:
            records = response.json()
            output = "\n".join(
                [f"Date: {rec['date']}, Present: {rec['present']}" for rec in records]
            )
            result_label.config(text=output)
        else:
            result_label.config(text="No attendance records found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def post_attendance():
    try:
        data = {
            "name": name_entry.get(),
            "registration_number": reg_no_entry.get(),
            "branch": branch_entry.get(),
            "section": section_entry.get(),
            "date": date_entry.get(),
            "present": present_var.get(),
        }
        response = requests.post(f"{BASE_URL}/attendance", json=data)
        if response.status_code == 200 or response.status_code == 201:
            messagebox.showinfo("Success", "Attendance record created successfully!")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Failed to create record."))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_attendance():
    try:
        data = {
            "date": date_entry.get(),
            "present": present_var.get(),
        }
        reg_no = reg_no_entry.get()
        if not reg_no:
            messagebox.showerror("Error", "Registration number is required for updating.")
            return

        response = requests.put(f"{BASE_URL}/attendance/{reg_no}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Attendance record updated successfully!")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Failed to update record."))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_attendance():
    reg_no = reg_no_entry.get()
    if not reg_no:
        messagebox.showerror("Error", "Registration number is required.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/attendance/{reg_no}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Attendance record deleted successfully!")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Failed to delete record."))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI Setup
app = tk.Tk()
app.title("Student Attendance Management" )

# Input Fields
tk.Label(app, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(app, text="Registration Number:").grid(row=1, column=0, padx=5, pady=5)
reg_no_entry = tk.Entry(app)
reg_no_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(app, text="Branch:").grid(row=2, column=0, padx=5, pady=5)
branch_entry = tk.Entry(app)
branch_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(app, text="Section:").grid(row=3, column=0, padx=5, pady=5)
section_entry = tk.Entry(app)
section_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(app, text="Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
date_entry = tk.Entry(app)
date_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(app, text="Present (True/False):").grid(row=5, column=0, padx=5, pady=5)
present_var = tk.BooleanVar(value=False)
present_check = ttk.Checkbutton(app, variable=present_var)
present_check.grid(row=5, column=1, padx=5, pady=5)

# Buttons
tk.Button(app, text="Get Attendance", command=get_attendance).grid(row=6, column=0, padx=5, pady=5)
tk.Button(app, text="Add Attendance", command=post_attendance).grid(row=6, column=1, padx=5, pady=5)
tk.Button(app, text="Update Attendance", command=update_attendance).grid(row=7, column=0, padx=5, pady=5)
tk.Button(app, text="Delete Attendance", command=delete_attendance).grid(row=7, column=1, padx=5, pady=5)

# Result Label
result_label = tk.Label(app, text="", wraplength=400, justify="left")
result_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

app.mainloop()

