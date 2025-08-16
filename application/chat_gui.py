"""
Description: Creates a chat application using Tkinter that interacts with the SUSTAIN API.
The chat application allows users to send messages to SUSTAIN and receive optimized responses. 
The application also calculates the average token savings and CO2 emissions saved by using SUSTAIN.
"""

import os
import platform
import tkinter as tk
import ctypes
from tkinter import filedialog, scrolledtext

from dotenv import load_dotenv
from PIL import Image, ImageTk
from sustain import SUSTAIN

load_dotenv()


class ChatApp:
    '''Chat application GUI for interacting with the SUSTAIN API.'''

    def __init__(self, root_window, track_token_length):
        self.track_token_length = track_token_length
        self.root = root_window
        self.root.title("SUSTAIN Chat")
        self.root.geometry("800x800")
        
        # Set icon based on platform
        try:
            if platform.system() == "Windows":
                icon_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "assets/SUSTAINicon.ico")
                )
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            else:
                # For macOS/Linux, use PNG format
                png_icon_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "assets/icon.png")
                )
                if os.path.exists(png_icon_path):
                    img = Image.open(png_icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.root.iconphoto(True, photo)
        except (tk.TclError, OSError, FileNotFoundError) as e:
            print(f"Could not set window icon: {e}")
        
        self.message_history = []

        if platform.system() == "Windows":
            try:
                myappid = 'company.sustain.chat.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    myappid)
            except (OSError, AttributeError) as e:
                print(f"Failed to set application ID: {str(e)}")

        # Initialize token savings
        self.total_percentage_saved = 0
        self.message_count = 0

        # Initialize dark mode setting
        self.is_dark_mode = True

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=10)

        logo_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "assets/SUSTAINOriginalWhiteTransparentCropped.png"
            )
        )
        if os.path.exists(logo_path):
            original_logo = Image.open(logo_path)
            max_size = (200, 200)
            original_logo.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(original_logo)
        else:
            raise FileNotFoundError(f"Logo file not found at: {logo_path}")

        # Logo label with dark mode background
        self.logo_label = tk.Label(
            self.top_frame, image=self.logo, bg="#1e1e1e")
        self.logo_label.pack(side=tk.LEFT, padx=10)

        # Info button at the top-right corner
        self.info_button = tk.Button(
            self.top_frame,
            text='?',
            command=self.show_info,
            font=("Mangal_Pro", 14),
            width=3,
            bg="#3c3c3c",
            fg="white"
        )
        self.info_button.pack(side=tk.RIGHT, padx=20)

        # Create a chat area and entry field
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state='disabled',
            height=25,
            font=("Mangal_Pro", 16)
        )
        self.chat_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root, font=("Mangal_Pro", 16))
        self.entry.pack(padx=20, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Add a label to display token percentage saved
        self.token_savings_label = tk.Label(
            self.root,
            text="Average token savings: 0.00%. Thank you for going green!",
            fg="#318752",
            font=("Mangal_Pro", 16)
        )
        self.token_savings_label.pack(pady=10)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Chat", command=self.save_chat)
        self.file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Add Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(
            label="Calculate CO2 Savings",
            command=self.calculate_co2_savings
        )

        # Add Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Info", command=self.show_info)

        # Add View menu for dark/light mode toggle
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(
            label="Toggle Dark/Light Mode",
            command=self.toggle_mode
        )

        # Apply dark mode settings by default
        self.apply_theme(self.is_dark_mode)

        # Initialize the SUSTAIN API
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Please set the OPENAI_API_KEY environment variable."
            )
        self.sustain = SUSTAIN(api_key=self.api_key)
        self.display_settings_message(
            "Welcome to SUSTAIN Chat! Ask me: \"What is SUSTAIN?\" to learn more."
        )

    def apply_theme(self, is_dark_mode):
        """Apply the selected theme (dark or light) to the application."""
        if is_dark_mode:
            # Dark mode settings
            bg_color, fg_color = "#1e1e1e", "white"
            info_button_bg = "#4CAD75"
            logo_path = os.path.abspath(os.path.join(os.path.dirname(
                __file__), "assets/SUSTAINOriginalWhiteTransparentCropped.png"))
        else:
            # Light mode settings
            bg_color, fg_color = "#f5f5f5", "black"
            info_button_bg = "#4CAD75"
            logo_path = os.path.abspath(os.path.join(os.path.dirname(
                __file__), "assets/SUSTAINOriginalBlackTransparentCropped.png"))

        # Apply theme to widgets
        self.root.configure(bg=bg_color)
        self.chat_area.configure(
            bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.entry.configure(bg=bg_color, fg=fg_color,
                             insertbackground=fg_color)
        self.token_savings_label.configure(bg=bg_color, fg="#318752")
        self.top_frame.configure(bg=bg_color)

        self.info_button.configure(bg=info_button_bg, fg="#4CAD75")
        self.menu_bar.configure(bg=bg_color, fg=fg_color)
        self.file_menu.configure(bg=bg_color, fg=fg_color)
        self.tools_menu.configure(bg=bg_color, fg=fg_color)
        self.help_menu.configure(bg=bg_color, fg=fg_color)
        self.view_menu.configure(bg=bg_color, fg=fg_color)
        self.logo_label.configure(bg=bg_color)

        # Update the logo
        if os.path.exists(logo_path):
            original_logo = Image.open(logo_path)
            max_size = (200, 200)
            original_logo.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(original_logo)
            self.logo_label.configure(image=self.logo)
        else:
            self.display_settings_message(
                f"Logo file not found at: {logo_path}")

    def toggle_mode(self):
        """Toggle between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme(self.is_dark_mode)

    def send_message(self, event=None):
        '''Send a message to the SUSTAIN API and display the response.'''
        user_input = self.entry.get()
        if user_input:
            self.message_history.append(user_input)
            self.display_message("You: " + user_input)

            # Check if user input is a math expression
            math_answer = self.sustain.answer_math(user_input)
            if math_answer is not None:
                # Display the result of the math expression directly
                self.display_message(
                    f"SUSTAIN: Math detected! Result: {math_answer}")
                self.display_settings_message(
                    "You saved 100% tokens by using SUSTAIN's math optimizer!")
                self.entry.delete(0, tk.END)

                # Update token savings to 100% for math queries
                self.message_count += 1
                self.total_percentage_saved += 100  # Save 100% savings for math queries
                average_savings = self.total_percentage_saved / self.message_count
                self.token_savings_label.config(
                    text=f"Average token savings: {average_savings:.2f}%. Thank you for going green!")
                return  # Exit early to prevent API call

            # Check if user input is a special command
            if user_input.strip().lower() == "what is sustain?":
                response = (
                    "I am SUSTAIN, an environmentally-friendly, token-optimized AI wrapper designed to reduce compute costs "
                    "and increase productivity. I filter out irrelevant words and phrases from prompts and limit responses to "
                    "essential outputs, minimizing the number of tokens used."
                )
                percentage_saved = 0
            else:
                response, percentage_saved = self.sustain.get_response(
                    user_input)

            # Display the response from SUSTAIN
            self.display_message("\nSUSTAIN: " + response)
            if percentage_saved == 0:
                self.display_settings_message(
                    "With SUSTAIN, you saved 0.00% more tokens compared to traditional AI!\n")
            else:
                self.display_settings_message(
                    f"With SUSTAIN, you saved {percentage_saved:.2f}% more tokens compared to traditional AI!\n")
            self.entry.delete(0, tk.END)

            # Update token savings
            self.message_count += 1
            self.total_percentage_saved += percentage_saved
            average_savings = self.total_percentage_saved / self.message_count
            self.token_savings_label.config(
                text=f"Average token savings: {average_savings:.2f}%. Thank you for going green!")

            self.track_token_length(user_input)

    def display_message(self, message):
        '''Display a message in the chat area.'''
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def display_settings_message(self, message):
        '''Display a settings message in the chat area.'''
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n", "grey")
        self.chat_area.tag_config("grey", foreground="grey")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def save_chat(self):
        '''Save the chat history to a file.'''
        chat_history = self.chat_area.get("1.0", tk.END).strip()
        if chat_history:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                     ("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(chat_history)
                self.display_settings_message(
                    f"Chat history saved to {file_path}")

    def clear_chat(self):
        '''Clear the chat area.'''
        self.chat_area.config(state='normal')
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state='disabled')
        self.display_settings_message("Chat history cleared.")

    def calculate_co2_savings(self):
        '''Calculate CO2 savings based on token savings.'''
        kwh_per_token_saved = 0.0001
        co2_per_kwh_saved = 0.7

        total_tokens_saved = 0
        for msg in self.message_history:
            original_tokens = self.sustain.count_tokens(msg)
            optimized_input = self.sustain.text_optimizer.optimize_text(msg)
            optimized_tokens = self.sustain.count_tokens(optimized_input)
            tokens_saved = original_tokens - optimized_tokens
            total_tokens_saved += tokens_saved

            # Assuming the response is capped at 50 tokens
            response_tokens = 50
            total_tokens_saved += response_tokens

        total_kwh_saved = total_tokens_saved * kwh_per_token_saved * 365
        total_co2_saved = (total_kwh_saved * co2_per_kwh_saved) / 1_000

        # Display the CO2 savings message
        message = (
            f"If you continue using SUSTAIN at this pace for a year, you will have saved approximately {total_kwh_saved:.4f} "
            f"kWh of power, reducing {total_co2_saved:.4f} metric tons of CO2 emissions! Thank you for making a difference!"
        )
        self.display_settings_message(message)

    def show_info(self):
        """Show information about the chat application."""
        info_window = tk.Toplevel(self.root)
        info_window.title("Information")
        info_window.geometry("600x400")

        # Match the color theme of the current mode
        bg_color = "#1e1e1e" if self.is_dark_mode else "white"
        fg_color = "white" if self.is_dark_mode else "black"

        info_window.configure(bg=bg_color)

        # Scrollable text widget
        info_text = (
            "Welcome to SUSTAIN Chat!\n"
            "How to use:\n"
            "  1. Type your message in the text box at the bottom of the window.\n"
            "  2. Press Enter to send your message to SUSTAIN.\n"
            "  3. SUSTAIN will respond with an optimized message.\n\n"

            "FAQs:\n"
            "What is a token?\n"
            "  A token is a unit of text that the AI processes. Tokens can be as short as one character or as long as one word.\n\n"

            "Ethics Policy:\n"
            "  We follow OpenAI's ethics policy, ensuring that our AI is used responsibly and ethically. "
            "We prioritize user privacy and data security.\n\n"

            "What we cut out and why:\n"
            "  We remove unnecessary words and phrases to optimize the text and reduce the number of tokens used. "
            "This helps in reducing compute costs and environmental impact."
        )

        # Set UI for text widget
        text_widget = tk.Text(
            info_window, wrap=tk.WORD, font=("Courier", 12), padx=15, pady=10,
            bg=bg_color, fg=fg_color, relief=tk.FLAT
        )
        text_widget.insert(tk.END, info_text)
        text_widget.config(state='disabled')  # Make text read-only

        # Scrollbar configuration
        scrollbar = tk.Scrollbar(info_window, command=text_widget.yview)
        text_widget['yscrollcommand'] = scrollbar.set

        # Packing widgets
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Run the chat application
if __name__ == "__main__":
    root = tk.Tk()

    def dummy_track_token_length(_user_input):
        """Dummy function for tracking token length."""
        return None

    app = ChatApp(root, dummy_track_token_length)
    root.mainloop()
