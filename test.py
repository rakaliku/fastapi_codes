import pyautogui

# Specify the button image file (make sure the image is the correct one)
button_image = 'Get Attendance.png'

# Check if pyautogui can locate the image
button_location = pyautogui.locateOnScreen(button_image, confidence=0.2)

if button_location:
    print("Button found:", button_location)
else:
    print("Button not found")
