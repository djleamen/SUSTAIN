'''
Description: This file is responsible for running the chat application.
'''

import logging
import os
import platform
import ctypes
import tkinter as tk

import spacy
from spacy.cli import download
from chat_gui import ChatApp
from dotenv import load_dotenv
from PIL import Image, ImageTk

# Configure logging
log_file_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../sustain.log'))
logging.basicConfig(filename=log_file_path, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

def track_token_length(message):
    '''Track the token length of a message.'''
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(message)
    return len(doc)

def main():
    '''Main function to run the chat application.'''
    logging.info("Starting SUSTAIN Chat Application")
    print("Starting SUSTAIN Chat Application")

    # Set the taskbar icon ID and icon (Windows only)
    if platform.system() == "Windows":
        try:
            myappid = 'company.sustain.chat.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                myappid)
        except (OSError, AttributeError) as e:
            logging.error("Failed to set application ID: %s", str(e))

    # Create root window before setting icon
    root = tk.Tk()

    # Set the icon for both window and taskbar
    try:
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "assets/SUSTAINicon.ico")
        )
        if os.path.exists(icon_path):
            if platform.system() == "Windows":
                root.iconbitmap(icon_path)
            else:
                # For macOS/Linux, try using PNG format instead
                png_icon_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "assets/icon.png")
                )
                if os.path.exists(png_icon_path):
                    img = Image.open(png_icon_path)
                    photo = ImageTk.PhotoImage(img)
                    root.iconphoto(True, photo)
                else:
                    logging.warning("PNG icon file not found, skipping icon setup")
        else:
            logging.error("Icon file not found at: %s", icon_path)
            print(f"Icon file not found at: {icon_path}")
    except (tk.TclError, OSError, FileNotFoundError, ImportError) as e:
        logging.error("Failed to set icon: %s", str(e))
        print(f"Failed to set icon: {str(e)}")

    # Rest of your initialization
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error(
            "API key not found. Please set the OPENAI_API_KEY environment variable."
        )
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        raise ValueError(
            "API key not found. Please set the OPENAI_API_KEY environment variable."
        )

    # Check if spaCy model is installed, if not, download it
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")

    ChatApp(root, track_token_length)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, tk.TclError) as e:
        logging.error("Application error: %s", str(e))
        print(f"Application error: {str(e)}")
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
        print("Application interrupted by user")
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        print(f"Unexpected error: {str(e)}")
        raise
