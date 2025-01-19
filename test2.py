import time
import pyautogui
import win32gui

# Function to check if the target Tkinter window is present
def is_tkinter_window_present(window_title):
    def callback(hwnd, titles):
        if window_title in win32gui.GetWindowText(hwnd):
            titles.append(hwnd)
    titles = []
    win32gui.EnumWindows(callback, titles)
    return titles

# Function to auto-click the "Get Attendance" button
def auto_click_button(window_title, button_text, click_interval=60):
    while True:
        # Check if the Tkinter window is present
        tkinter_windows = is_tkinter_window_present(window_title)
        if tkinter_windows:
            # Find the specified button within the Tkinter window
            for hwnd in tkinter_windows:
                button_location = None
                try:
                    # Locate the button based on its text within the Tkinter window
                    button_location = pyautogui.locateOnScreen(f'{button_text}.png', region=(0, 0, 1920, 1080), confidence=0.8)
                    if button_location:
                        break
                except:
                    pass

            if button_location:
                # Auto-click the located button
                pyautogui.click(pyautogui.center(button_location))
                print("Button clicked successfully!")
            else:
                print(f"Button '{button_text}' not found in the specified Tkinter window.")

        # Sleep for the specified interval
        time.sleep(click_interval)

# Specify the window title and button text you are targeting
window_title = "Student Attendance Management"
button_text = "Get Attendance"

# Start auto-clicking the button every 5 minutes (300 seconds)
auto_click_button(window_title, button_text)
