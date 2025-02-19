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
import ctypes

# Configure logging
logging.basicConfig(filename='../sustain.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Function to track the token length of a message
def track_token_length(message):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(message)
    return len(doc)

# Main function to run the chat application
def main():
    logging.info("Starting SUSTAIN Chat Application")

    # Set the taskbar icon ID and icon
    try:
        # Set app ID
        myappid = u'company.sustain.chat.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Get absolute path to icon
        import os
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "SUSTAINicon.ico"))

        if not os.path.exists(icon_path):
            logging.error(f"Icon file not found at: {icon_path}")
    except Exception as e:
        logging.error(f"Failed to set application ID: {str(e)}")

    # Create root window before setting icon
    root = tk.Tk()

    # Set the icon for both window and taskbar
    try:
        root.iconbitmap(default=icon_path)
    except Exception as e:
        logging.error(f"Failed to set icon: {str(e)}")

    # Rest of your initialization
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Check if spaCy model is installed, if not, download it
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")

    app = ChatApp(root, track_token_length)
    root.mainloop()


# Run the main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")