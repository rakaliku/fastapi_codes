import tkinter as tk
from tkinter import messagebox
import requests

# Base URL for your FastAPI server
BASE_URL = "http://127.0.0.1:8000"

# Global token to store JWT after login
token = None

# Function to send sign-up request
def signup():
    username = entry_username_signup.get()
    password = entry_password_signup.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    response = requests.post(f"{BASE_URL}/signup", json={"username": username, "password": password})
    if response.status_code == 200:
        messagebox.showinfo("Success", "User signed up successfully!")
        show_login_screen()
    else:
        messagebox.showerror("Error", "Sign up failed. Try again.")

# Function to send login request
def login():
    global token
    username = entry_username_login.get()
    password = entry_password_login.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})

    if response.status_code == 200:
        token = response.json().get("access_token")
        messagebox.showinfo("Success", "Logged in successfully!")
        show_attendance_screen()
    else:
        messagebox.showerror("Error", "Login failed. Try again.")

# Function to mark attendance using the access token
def mark_attendance():
    global token
    if not token:
        messagebox.showerror("Error", "You must be logged in to mark attendance.")
        return

    registration_number = entry_registration.get()
    present = var_present.get()

    # Prepare the data to send to the API
    attendance_data = {
        "registration_number": registration_number,
        "present": present,
    }

    headers = {"Authorization": f"Bearer {token}"}

    # Send attendance request
    response = requests.post(f"{BASE_URL}/attendance", json=attendance_data, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Success", "Attendance marked successfully!")
    else:
        messagebox.showerror("Error", "Failed to mark attendance.")

# Function to show the Sign-Up screen
def show_signup_screen():
    frame_signup.pack(pady=20)
    frame_login.pack_forget()
    frame_attendance.pack_forget()

# Function to show the Login screen
def show_login_screen():
    frame_signup.pack_forget()
    frame_login.pack(pady=20)
    frame_attendance.pack_forget()

# Function to show the Attendance screen
def show_attendance_screen():
    frame_signup.pack_forget()
    frame_login.pack_forget()
    frame_attendance.pack(pady=20)

# Tkinter window setup
root = tk.Tk()
root.title("Student Attendance Management")

# Sign-up UI
frame_signup = tk.Frame(root)
frame_signup.pack(pady=20)

label_username_signup = tk.Label(frame_signup, text="Username")
label_username_signup.grid(row=0, column=0)
entry_username_signup = tk.Entry(frame_signup)
entry_username_signup.grid(row=0, column=1)

label_password_signup = tk.Label(frame_signup, text="Password")
label_password_signup.grid(row=1, column=0)
entry_password_signup = tk.Entry(frame_signup, show="*")
entry_password_signup.grid(row=1, column=1)

button_signup = tk.Button(frame_signup, text="Sign Up", command=signup)
button_signup.grid(row=2, columnspan=2)

# Login UI
frame_login = tk.Frame(root)

label_username_login = tk.Label(frame_login, text="Username")
label_username_login.grid(row=0, column=0)
entry_username_login = tk.Entry(frame_login)
entry_username_login.grid(row=0, column=1)

label_password_login = tk.Label(frame_login, text="Password")
label_password_login.grid(row=1, column=0)
entry_password_login = tk.Entry(frame_login, show="*")
entry_password_login.grid(row=1, column=1)

button_login = tk.Button(frame_login, text="Login", command=login)
button_login.grid(row=2, columnspan=2)

# Attendance UI
frame_attendance = tk.Frame(root)

label_registration = tk.Label(frame_attendance, text="Registration Number")
label_registration.grid(row=0, column=0)
entry_registration = tk.Entry(frame_attendance)
entry_registration.grid(row=0, column=1)

var_present = tk.BooleanVar()
checkbox_present = tk.Checkbutton(frame_attendance, text="Present", variable=var_present)
checkbox_present.grid(row=1, columnspan=2)

button_attendance = tk.Button(frame_attendance, text="Mark Attendance", command=mark_attendance)
button_attendance.grid(row=2, columnspan=2)

# Show the Sign-Up screen initially
show_signup_screen()

root.mainloop()
