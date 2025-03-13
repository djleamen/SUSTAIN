'''
Description: This file is responsible for running the chat application.

'''

# Import required libraries
import os
import logging
import tkinter as tk
from dotenv import load_dotenv
from chat_gui import ChatApp
import spacy
import platform

# Configure logging
log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sustain.log'))
print(f"Log file path: {log_file_path}")
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Logging is configured")

# Load environment variables from .env file
load_dotenv()
logging.debug("Environment variables loaded")

# Function to track the token length of a message
def track_token_length(message):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(message)
    return len(doc)

# Main function to run the chat application
def main():
    logging.info("Starting SUSTAIN Chat Application")
    print("Starting SUSTAIN Chat Application")

    # Set the taskbar icon ID and icon (Windows only)
    if platform.system() == "Windows":
        try:
            import ctypes
            myappid = u'company.sustain.chat.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            logging.debug("Application ID set for Windows")
        except Exception as e:
            logging.error(f"Failed to set application ID: {str(e)}")

    # Create root window before setting icon
    logging.debug("Creating root window")
    print("Creating root window")
    root = tk.Tk()

    # Set the icon for both window and taskbar
    try:
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "SUSTAINicon.ico"))
        logging.debug(f"Icon path: {icon_path}")
        print(f"Icon path: {icon_path}")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
            logging.debug("Icon set successfully")
            print("Icon set successfully")
        else:
            logging.error(f"Icon file not found at: {icon_path}")
            print(f"Icon file not found at: {icon_path}")
    except Exception as e:
        logging.error(f"Failed to set icon: {str(e)}")
        print(f"Failed to set icon: {str(e)}")

    # Rest of your initialization
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Check if spaCy model is installed, if not, download it
    try:
        spacy.load("en_core_web_sm")
        logging.debug("spaCy model loaded successfully")
        print("spaCy model loaded successfully")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        logging.debug("spaCy model downloaded and loaded successfully")
        print("spaCy model downloaded and loaded successfully")

    logging.debug("Initializing ChatApp")
    print("Initializing ChatApp")
    app = ChatApp(root, track_token_length)
    root.mainloop()
    logging.debug("ChatApp main loop started")
    print("ChatApp main loop started")


# Run the main function
if __name__ == "__main__":
    try:
        logging.debug("Starting main function")
        print("Starting main function")
        main()
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        print(f"Unhandled exception: {str(e)}")