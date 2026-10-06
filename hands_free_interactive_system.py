import os
import pyautogui
import speech_recognition as sr
import webbrowser
import time
import subprocess

# ------------------ Application Mapping ------------------ #
APP_MAP = {
    "notepad": "notepad.exe",
    "wordpad": "write.exe",
    "paint": "mspaint.exe",
    "calculator": "calc.exe",
    "snipping tool": "SnippingTool.exe",
    "file explorer": "explorer.exe",
    "control panel": "control.exe",
    "settings": "ms-settings:",
    "command prompt": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "photos": "microsoft.photos:",
    "windows media player": "wmplayer.exe",
    "voice recorder": "ms-callrecording:",
    "clock": "ms-clock:",
    "camera": "microsoft.windows.camera:",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "edge": "msedge.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe"
}

# ------------------ Website Mapping ------------------ #
WEBSITE_MAP = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com/a"
}

# ------------------ Mouse Actions ------------------ #
def click_mouse():
    pyautogui.click()

def double_click_mouse():
    pyautogui.doubleClick()

def select_mouse():
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def move_mouse(direction, pixels=50):
    x, y = pyautogui.position()
    if direction == "up":
        pyautogui.moveTo(x, y - pixels)
    elif direction == "down":
        pyautogui.moveTo(x, y + pixels)
    elif direction == "left":
        pyautogui.moveTo(x - pixels, y)
    elif direction == "right":
        pyautogui.moveTo(x + pixels, y)

# ------------------ Window Management ------------------ #
def minimize_window():
    pyautogui.hotkey('win', 'down')

def maximize_window():
    pyautogui.hotkey('win', 'up')

def close_window():
    pyautogui.hotkey('alt', 'f4')

def switch_window():
    pyautogui.hotkey('alt', 'tab')

# ------------------ Scroll Actions ------------------ #
def scroll_up():
    pyautogui.scroll(300)  # Scroll up

def scroll_down():
    pyautogui.scroll(-300)  # Scroll down

# ------------------ Typing and Messaging ------------------ #
def type_text(text):
    pyautogui.typewrite(text, interval=0.05)

def send_message(text):
    pyautogui.typewrite(text, interval=0.05)
    pyautogui.press('enter')

# ------------------ Close Application ------------------ #
def close_app(app_name):
    if app_name in APP_MAP:
        process_name = APP_MAP[app_name]
        try:
            subprocess.call(f"taskkill /f /im {process_name}", shell=True)
            print(f"{app_name} closed successfully.")
        except Exception as e:
            print(f"Could not close {app_name}: {e}")
    else:
        print(f"No such app '{app_name}' found in mapping.")

# ------------------ Command Mapping ------------------ #
COMMAND_MAP = {
    "click": click_mouse,
    "double click": double_click_mouse,
    "select": select_mouse,
    "up": lambda: move_mouse("up"),
    "down": lambda: move_mouse("down"),
    "left": lambda: move_mouse("left"),
    "right": lambda: move_mouse("right"),
    "small window": minimize_window,
    "large window": maximize_window,
    "close": close_window,
    "switch": switch_window,
    "scroll up": scroll_up,
    "scroll down": scroll_down
}

# ------------------ Voice Recognition ------------------ #
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return ""

# ------------------ Execute Command ------------------ #
def execute_command(command):
    # Open applications
    for app in APP_MAP:
        if app in command and "close" not in command:
            print(f"Opening {app}...")
            os.startfile(APP_MAP[app])
            return

    # Open websites
    for site in WEBSITE_MAP:
        if site in command:
            print(f"Opening {site}...")
            webbrowser.open(WEBSITE_MAP[site])
            return

    # Mouse/window actions
    for action in COMMAND_MAP:
        if action in command:
            COMMAND_MAP[action]()
            return

    # Typing text
    if command.startswith("type "):
        text_to_type = command.replace("type ", "")
        print(f"Typing text: {text_to_type}")
        type_text(text_to_type)
        return

    # Send message
    if command.startswith("send message "):
        message = command.replace("send message ", "")
        print(f"Sending message: {message}")
        send_message(message)
        return

    # Close applications
    if command.startswith("close "):
        app_to_close = command.replace("close ", "")
        close_app(app_to_close)
        return

    print("Command not recognized!")

# ------------------ Main Program ------------------ #
if __name__ == "__main__":
    print("Hands-Free Voice-Controlled System Started...")
    while True:
        command = listen_command()
        if command in ["exit", "quit", "stop"]:
            print("Exiting system...")
            break
        if command:
            execute_command(command)
        time.sleep(1)