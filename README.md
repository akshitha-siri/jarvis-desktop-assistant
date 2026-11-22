# J.A.R.V.I.S. — Voice-Controlled Desktop Assistant

J.A.R.V.I.S. is a Python-based desktop assistant designed to perform everyday tasks through text and voice commands. It provides a simple Tkinter graphical interface, speech recognition, text-to-speech responses, desktop automation, and SQLite-based data storage.

## Features

- **Voice and Text Commands:** Interact with the assistant using typed commands or voice input.
- **Speech Recognition:** Recognizes spoken commands using Google Speech Recognition.
- **Text-to-Speech:** Responds using voice output through pyttsx3.
- **Desktop Automation:** Open and close applications such as Notepad and Calculator.
- **Web Navigation:** Open websites including Google, YouTube, GitHub, LinkedIn, ChatGPT, Instagram, and Amazon.
- **Google Search:** Perform Google searches using commands.
- **System Controls:** Lock, shut down, or restart the computer with confirmation options.
- **Task Management:** Add tasks and view pending tasks.
- **Conversation History:** Store and retrieve previous conversations using SQLite.

## Technologies Used

- Python
- Tkinter
- SQLite
- SpeechRecognition
- PyAudio
- pyttsx3

## Project Structure

```text
JARVIS/
│
├── main.py
├── requirements.txt
├── .gitignore
└── jarvis.db  (created locally when the application runs)
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/akshitha-siri/jarvis-desktop-assistant.git
   ```

2. Navigate to the project folder:

   ```bash
   cd jarvis-desktop-assistant
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python main.py
   ```

## Example Commands

- "Hello Jarvis"
- "Are you Jarvis?"
- "Open Notepad"
- "Open Calculator"
- "Open YouTube"
- "Search Python tutorials"
- "Add task complete Python practice"
- "Show tasks"
- "View history"
- "Lock computer"

## Database

The application uses SQLite to store:

- Conversation history
- User-created tasks

The database file is generated locally when the application runs and is excluded from Git tracking.

## Requirements

- Windows operating system
- Python installed
- Microphone for voice commands
- Internet connection for Google Speech Recognition and web searches

## Project Purpose

This project demonstrates the practical use of Python for desktop automation, GUI development, speech interaction, multithreading, and database management.