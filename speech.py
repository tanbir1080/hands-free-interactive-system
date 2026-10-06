import os
import pyautogui
import speech_recognition as sr
import webbrowser
import time
import subprocess

# Full path of taskkill (FIX)
TASKKILL_PATH = r"C:\Windows\System32\taskkill.exe"

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
    "whatsapp": "https://web.whatsapp.com/"
}

# ------------------ Mouse ------------------ #
def click_mouse():
    pyautogui.click()

def double_click_mouse():
    pyautogui.doubleClick()

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

# ------------------ Window ------------------ #
def minimize_window():
    pyautogui.hotkey('win', 'down')

def maximize_window():
    pyautogui.hotkey('win', 'up')

def close_window():
    pyautogui.hotkey('alt', 'f4')

def switch_window():
    pyautogui.hotkey('alt', 'tab')

# ------------------ Scroll ------------------ #
def scroll_up():
    pyautogui.scroll(300)

def scroll_down():
    pyautogui.scroll(-300)

# ------------------ Typing ------------------ #
def type_text(text):
    pyautogui.typewrite(text, interval=0.05)

# ------------------ FIXED Close App ------------------ #
def close_app(app_name):

    if app_name in APP_MAP:

        process_name = APP_MAP[app_name]

        try:
            subprocess.call([TASKKILL_PATH, "/f", "/im", process_name])
            print(f"{app_name} closed successfully")

        except Exception as e:
            print("Error:", e)

    else:
        print("Application not found")

# ------------------ FIXED Taskkill ------------------ #
def taskkill_app(app_name):

    if app_name in APP_MAP:

        process_name = APP_MAP[app_name]

        try:
            subprocess.call([TASKKILL_PATH, "/f", "/im", process_name])
            print(f"{app_name} force closed successfully")

        except Exception as e:
            print("Error:", e)

    else:
        print("Application not found")

# ------------------ Notepad Dictation ------------------ #
def notepad_dictation():

    recognizer = sr.Recognizer()

    print("Dictation started. Say 'stop typing' to exit.")

    while True:

        with sr.Microphone() as source:

            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:

            text = recognizer.recognize_google(audio).lower()
            print("Dictated:", text)

            if text in ["stop typing", "stop dictation"]:
                print("Dictation stopped")
                break

            pyautogui.typewrite(text + " ", interval=0.05)

        except:
            print("Could not understand")

# ------------------ Voice Recognition ------------------ #
def listen_command():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nWaiting for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:

        command = recognizer.recognize_google(audio).lower()
        print("Command:", command)
        return command

    except:
        return ""

# ------------------ Execute ------------------ #
def execute_command(command):

    # Taskkill
    if command.startswith("taskkill "):

        app = command.replace("taskkill ", "").strip()
        taskkill_app(app)
        return

    # Close app
    if command.startswith("close ") and command != "close window":

        app = command.replace("close ", "").strip()
        close_app(app)
        return

    # Open app
    for app in APP_MAP:

        if command == f"open {app}" or app in command:

            print("Opening", app)
            os.startfile(APP_MAP[app])

            if app == "notepad":
                time.sleep(2)
                notepad_dictation()

            return

    # Open website
    for site in WEBSITE_MAP:

        if site in command:

            print("Opening", site)
            webbrowser.open(WEBSITE_MAP[site])
            return

    # Window control
    if command == "close window":
        close_window()

    elif command == "switch window":
        switch_window()

    elif command == "minimize window":
        minimize_window()

    elif command == "maximize window":
        maximize_window()

    elif command == "scroll up":
        scroll_up()

    elif command == "scroll down":
        scroll_down()

    # Mouse
    elif command == "click":
        click_mouse()

    elif command == "double click":
        double_click_mouse()

    elif command in ["up", "down", "left", "right"]:
        move_mouse(command)

    # Typing
    elif command.startswith("type "):

        text = command.replace("type ", "")
        type_text(text)

    else:
        print("Command not recognized")

# ------------------ Main ------------------ #
if __name__ == "__main__":

    print("Hands Free Voice System Started")

    while True:

        command = listen_command()

        if command in ["exit", "quit", "stop system"]:
            print("System stopped")
            break

        if command:
            execute_command(command)

        time.sleep(1)