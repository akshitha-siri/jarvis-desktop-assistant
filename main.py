
import pyttsx3
import speech_recognition as sr
import time
import subprocess
import webbrowser
import ctypes
import tkinter as tk
import threading
import sqlite3
from datetime import datetime, timedelta

pending_action = None
last_response = ""

# =====================================
# 1. DATABASE CONNECTION
# =====================================

connection = sqlite3.connect("jarvis.db")
cursor = connection.cursor()

# CREATE CONVERSATION HISTORY TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_command TEXT,
        jarvis_response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

connection.commit()

# CREATE TASKS TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        due_date TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

connection.commit()

print("JARVIS: Tasks table created successfully!")
print("JARVIS: Database connected successfully!")
print("JARVIS: Conversation table created successfully!")


# SAVE CONVERSATION FUNCTION

def save_conversation(user_command, jarvis_response):

    cursor.execute("""
        INSERT INTO conversation_history (user_command, jarvis_response)
        VALUES (?, ?)
    """, (user_command, jarvis_response))

    connection.commit()


# ADD TASK FUNCTION

def add_task(task_name):

    cursor.execute("""
        INSERT INTO tasks (task_name)
        VALUES (?)
    """, (task_name,))

    connection.commit()

    speak("Task added successfully.")


# VIEW TASKS FUNCTION

def view_tasks():

    cursor.execute("""
        SELECT task_id, task_name
        FROM tasks
        WHERE status = 'Pending'
    """)

    tasks = cursor.fetchall()

    if not tasks:

        speak("You have no pending tasks.")

    else:

        response = "Here are your pending tasks. "

        for task in tasks:

            response += f"Task {task[0]}: {task[1]}. "

        speak(response)


# RETRIEVE CONVERSATION HISTORY

def show_history():

    cursor.execute("""
        SELECT user_command, jarvis_response, created_at
        FROM conversation_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    command_display.config(state="normal")

    command_display.insert(
        tk.END,
        "\n--- CONVERSATION HISTORY ---\n"
    )

    if records:

        for record in records:

            command_display.insert(
                tk.END,
                "\nYOU: " + str(record[0]) + "\n"
            )

            command_display.insert(
                tk.END,
                "JARVIS: " + str(record[1]) + "\n"
            )

            utc_time = datetime.strptime(
                record[2],
                "%Y-%m-%d %H:%M:%S"
            )

            ist_time = utc_time + timedelta(hours=5, minutes=30)

            command_display.insert(
                tk.END,
                "DATE: " + ist_time.strftime(
                    "%Y-%m-%d %I:%M:%S %p"
                ) + "\n"
            )

    else:

        command_display.insert(
            tk.END,
            "No previous conversations found.\n"
        )

    command_display.config(state="disabled")
    command_display.see(tk.END)


# =====================================
# 2. TEXT-TO-SPEECH ENGINE
# =====================================

engine = pyttsx3.init()

engine.setProperty("rate", 200)
engine.setProperty("volume", 1.0)


def speak(text):

    global last_response

    last_response = text

    engine.say(text)
    engine.runAndWait()

    if "command_display" in globals():

        command_display.config(state="normal")

        command_display.insert(
            tk.END,
            "JARVIS: " + text + "\n"
        )

        command_display.config(state="disabled")
        command_display.see(tk.END)


# =====================================
# 3. SPEECH RECOGNITION ENGINE
# =====================================

recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 300
recognizer.pause_threshold = 1.2
recognizer.non_speaking_duration = 0.5


# =====================================
# 4. MICROPHONE CALIBRATION
# =====================================

with sr.Microphone() as source:

    print("JARVIS: Calibrating microphone...")

    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

print("JARVIS: Microphone ready!")


# =====================================
# 5. LISTEN FUNCTION
# =====================================

def listen():

    try:

        with sr.Microphone() as source:

            print("JARVIS: Listening...")

            audio = recognizer.listen(
                source,
                timeout=3,
                phrase_time_limit=10
            )

        print("JARVIS: Processing...")

        start_time = time.time()

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        end_time = time.time()

        print(
            "Processing time:",
            round(end_time - start_time, 2),
            "seconds"
        )

        print("JARVIS: Command recognised!")
        print("JARVIS HEARD:", repr(text))

        return text

    except sr.WaitTimeoutError:

        print("JARVIS: No speech detected.")
        return None

    except sr.UnknownValueError:

        print("JARVIS: Could not understand you.")
        return None

    except sr.RequestError as error:

        print("JARVIS: Recognition service error:", error)
        return None

    except OSError as error:

        print("JARVIS: Microphone error:", error)
        return None


# =====================================
# 6. OPEN APPLICATIONS
# =====================================

def open_application(app_name):

    if app_name == "notepad":

        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")

    elif app_name == "calculator":

        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator.")

    else:

        speak("Sorry, this application is not available.")


# CLOSE APPLICATIONS

def close_application(app_name):

    if app_name == "notepad":

        subprocess.run(
            ["taskkill", "/IM", "notepad.exe", "/F"],
            capture_output=True
        )

        speak("Closing Notepad.")

    elif app_name == "calculator":

        subprocess.run(
            ["taskkill", "/IM", "CalculatorApp.exe", "/F"],
            capture_output=True
        )

        speak("Closing Calculator.")

    else:

        speak("Sorry, I cannot close that application.")


# LOCK COMPUTER

def lock_computer():

    speak("Locking your computer.")

    ctypes.windll.user32.LockWorkStation()


# =====================================
# 7. SYSTEM CONTROL
# =====================================

def system_control(action):

    global pending_action

    pending_action = action

    if action == "shutdown":

        speak("Are you sure? Say confirm shutdown.")

    elif action == "restart":

        speak("Are you sure? Say confirm restart.")


def confirm_system_action(action):

    global pending_action

    if action == pending_action:

        if action == "shutdown":

            speak(
                "Shutdown confirmed. Your computer will shut down in 60 seconds."
            )

            subprocess.run(["shutdown", "/s", "/t", "60"])

        elif action == "restart":

            speak(
                "Restart confirmed. Your computer will restart in 60 seconds."
            )

            subprocess.run(["shutdown", "/r", "/t", "60"])

        pending_action = None

    else:

        speak("That confirmation does not match the pending action.")


def cancel_system_action():

    global pending_action

    if pending_action:

        pending_action = None

        speak("System action cancelled.")

    else:

        speak("There is no pending system action.")


# =====================================
# 8. WEBSITE CONTROL
# =====================================

def open_website(website):

    website = website.lower().replace(" ", "").strip()

    websites = {

        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "linkedin": "https://www.linkedin.com",
        "chatgpt": "https://chatgpt.com",
        "instagram": "https://www.instagram.com",
        "amazon": "https://www.amazon.in"

    }

    websites_name = {

        "google": "Google",
        "youtube": "YouTube",
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "chatgpt": "Chat GPT",
        "instagram": "Instagram",
        "amazon": "Amazon"

    }

    if website in websites:

        webbrowser.open(websites[website])

        speak("Opening " + websites_name[website])

    else:

        speak("Sorry, I don't know that website.")


# GOOGLE SEARCH

def search_google(query):

    search_url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    webbrowser.open(search_url)

    speak("Here are the Google search results.")


# =====================================
# 9. JARVIS COMMAND RECOGNITION
# =====================================

def process_command(command):

    command = command.lower().strip()

    # SYSTEM ACTION CONFIRMATION

    if command in ["confirm shutdown", "jarvis confirm shutdown"]:

        confirm_system_action("shutdown")
        return

    elif command in ["confirm restart", "jarvis confirm restart"]:

        confirm_system_action("restart")
        return

    elif "cancel shutdown" in command or "cancel restart" in command:

        cancel_system_action()
        return

    words = command.split()

    # VIEW TASKS

    if command in ["view tasks", "show tasks", "view task", "show task"]:

        view_tasks()
        return
    # VIEW CONVERSATION HISTORY

    elif command in ["view history", "show history"]:

        show_history()
        speak("Here is your conversation history.")
        return
    # ADD TASK

    elif command.startswith("add task"):

        task_name = command.replace("add task", "", 1).strip()

        if task_name:
            add_task(task_name)
        else:
            speak("Please tell me the task name.")

        return

    # GREETINGS

    elif any(word in words for word in ["hello", "hi", "hey"]):

        speak("Hello buddy! Nice to hear from you.")

    # ASKING ABOUT JARVIS

    elif "how are you" in command:

        speak("I am doing great. All systems are working.")

    # ASKING JARVIS'S NAME

    elif "your name" in command or "who are you" in command:

        speak("I am JARVIS, your personal desktop assistant.")

    # THANKING JARVIS

    elif any(word in words for word in ["thanks", "thank"]):

        speak("You are welcome buddy.")

    # OPEN NOTEPAD

    elif "open notepad" in command or "launch notepad" in command:

        open_application("notepad")

    # OPEN CALCULATOR

    elif "open calculator" in command or "launch calculator" in command:

        open_application("calculator")

    # OPEN GOOGLE

    elif "open google" in command:

        open_website("google")

    # OPEN YOUTUBE

    elif "open youtube" in command:

        open_website("youtube")

    # GOOGLE SEARCH

    elif command.startswith("search for "):

        query = command.replace("search for ", "", 1)
        search_google(query)

    elif command.startswith("google "):

        query = command.replace("google ", "", 1)
        search_google(query)

    # CLOSE NOTEPAD

    elif "close notepad" in command:

        close_application("notepad")

    # CLOSE CALCULATOR

    elif "close calculator" in command:

        close_application("calculator")

    # OPEN OTHER WEBSITES

    elif command.startswith("open "):

        website = command.replace("open ", "", 1).strip()
        open_website(website)

    # LOCK COMPUTER

    elif "lock my computer" in command or "lock the screen" in command:

        lock_computer()

    # SHUTDOWN COMPUTER

    elif "shutdown computer" in command:

        system_control("shutdown")

    # RESTART COMPUTER

    elif "restart computer" in command:

        system_control("restart")

    # UNKNOWN COMMAND

    else:

        speak("Sorry, I don't know that command yet.")


# =====================================
# 10. SEND TEXT COMMAND
# =====================================

def send_command():

    global last_response

    user_command = command_entry.get().strip()

    if user_command:

        command_display.config(state="normal")

        command_display.insert(
            tk.END,
            "YOU: " + user_command + "\n"
        )

        command_display.config(state="disabled")

        command_entry.delete(0, tk.END)

        last_response = ""

        process_command(user_command)

        save_conversation(
            user_command,
            last_response
        )


# =====================================
# 11. VOICE LISTENING
# =====================================

def listen_in_background():

    user_command = listen()

    root.after(
        0,
        process_voice_command,
        user_command
    )


# PROCESS VOICE COMMAND

def process_voice_command(user_command):

    global last_response

    if user_command:

        command_display.config(state="normal")

        command_display.insert(
            tk.END,
            "YOU: " + user_command + "\n"
        )

        command_display.config(state="disabled")
        command_display.see(tk.END)

        last_response = ""

        process_command(user_command)

        save_conversation(
            user_command,
            last_response
        )

    status_label.config(text="SYSTEM ONLINE")
    mic_button.config(state="normal")


# START LISTENING

def start_listening():

    mic_button.config(state="disabled")

    status_label.config(text="LISTENING...")

    threading.Thread(
        target=listen_in_background,
        daemon=True
    ).start()


# =====================================
# 12. CLEAR CHAT
# =====================================

def clear_chat():

    command_display.config(state="normal")

    command_display.delete("1.0", tk.END)

    command_display.config(state="disabled")


# =====================================
# 13. TKINTER GUI
# =====================================

root = tk.Tk()

root.title("J.A.R.V.I.S")

root.geometry("800x500")

root.configure(bg="#101820")


# JARVIS HEADING

title_label = tk.Label(
    root,
    text="J.A.R.V.I.S",
    font=("Arial", 28, "bold"),
    fg="#00BFFF",
    bg="#101820"
)

title_label.pack(pady=30)


# WELCOME MESSAGE

welcome_label = tk.Label(
    root,
    text="YOUR PERSONAL DESKTOP ASSISTANT",
    font=("Arial", 10),
    fg="white",
    bg="#101820"
)

welcome_label.pack()


# SYSTEM STATUS

status_label = tk.Label(
    root,
    text="SYSTEM ONLINE",
    font=("Arial", 12),
    fg="#00FF00",
    bg="#101820"
)

status_label.pack()


# COMMAND DISPLAY AREA

command_display = tk.Text(
    root,
    height=10,
    width=70,
    font=("Arial", 12),
    bg="#1C2833",
    fg="white",
    insertbackground="white",
    relief="solid",
    bd=1
)

command_display.pack(pady=25)


# COMMAND INPUT

command_entry = tk.Entry(
    root,
    font=("Arial", 12),
    width=50
)

command_entry.pack(pady=10)


# ENTER KEY FUNCTION

def enter_pressed(event):

    send_command()


command_entry.bind(
    "<Return>",
    enter_pressed
)


# SEND BUTTON

send_button = tk.Button(
    root,
    text="SEND",
    font=("Arial", 12, "bold"),
    bg="#00BFFF",
    fg="black",
    width=12,
    command=send_command
)

send_button.pack(pady=10)


# MICROPHONE BUTTON

mic_button = tk.Button(
    root,
    text="START LISTENING",
    font=("Arial", 12, "bold"),
    bg="#00FF00",
    fg="black",
    width=18,
    command=start_listening
)

mic_button.pack(pady=10)


# CLEAR CHAT BUTTON

clear_button = tk.Button(
    root,
    text="CLEAR CHAT",
    bg="red",
    fg="white",
    command=clear_chat
)

clear_button.pack(pady=5)


# VIEW HISTORY BUTTON

history_button = tk.Button(
    root,
    text="VIEW HISTORY",
    bg="#FFA500",
    fg="black",
    font=("Arial", 10, "bold"),
    command=show_history
)

history_button.pack(pady=5)


# INITIAL JARVIS GREETING

speak("Hello! I am JARVIS. Your personal assistant is online.")
speak("How can I help you today?")


# START GUI

root.mainloop()
