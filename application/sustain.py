"""
Description: This module contains the SUSTAIN class that interacts with the 
OpenAI API to generate responses to user queries.The SUSTAIN class optimizes 
user input by removing unnecessary phrases and converting words to contractions 
before sending the input to the OpenAI API.

"""

# Import required libraries
import os
import logging
from openai import OpenAI
import spacy
import tiktoken
import re
from word2number import w2n

# Configure logging
logging.basicConfig(filename='../sustain.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_openai_response(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"{user_input} in <20 words."}],
                max_tokens=50
            )
            return response.choices[0].message.content.strip()
        except OpenAI.error.OpenAIError as e:
            logging.error(f"OpenAIError: {str(e)}")
            return self.handle_api_error(e)

    @staticmethod
    def handle_api_error(error):
        if error.code == 'insufficient_quota':
            return "Error: The API quota has been exceeded. Please contact SUSTAIN."
        elif error.code == 'model_not_found':
            return "Error: The specified model does not exist or you do not have access to it."
        return f"Error: {str(error)}"


class MathOptimizer:
    def __init__(self):
        # Initialize any necessary mathematical operators.
        self.word_to_operator = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'multiplied by': '*',
            'x': '*',
            'X': '*',
            'divided by': '/',
            'over': '/',
            'to the power of': '**',
            '^': '**'
        }

        # Convert words like 'five' to numbers like '5'

    def convert_number(self, user_input):
        try:
            return w2n.word_to_num(user_input)
        except ValueError:
            return user_input  # Return as-is if it's not a valid word-to-number

        # Clean up the input to remove unnecessary parts like question words and punctuation

    def clean_input(self, user_input):
        # Remove common question words and punctuation (like "What is", "what’s", etc.)
        user_input = re.sub(r'^(what is|what\'s|whats|please|can you|please tell me)\s*', '', user_input,
                            flags=re.IGNORECASE)
        # Remove trailing question marks or any other non-math characters
        user_input = re.sub(r'[^\w\s\+\-\*/\^\(\)]', '', user_input)
        # Remove excessive spaces
        user_input = ' '.join(user_input.split())
        return user_input

        # Recognize a math expression by looking for numbers and operators

    def recognize_math(self, user_input):
        math_pattern = r'(\d+|\w+)\s*(\+|\-|\*|\/|\bplus\b|\bminus\b|\btimes\b|\bdivided\b|\bto\s+the\s+power\s+of\b|\^)\s*(\d+|\w+)'
        if re.search(math_pattern, user_input, re.IGNORECASE):
            return True
        return False

        # Convert word-based operators (e.g. "plus") to mathematical symbols (e.g. "+")

    def convert_ops(self, user_input):
        for word, operator in self.word_to_operator.items():
            user_input = user_input.replace(word, operator)
        return user_input

        # Solve the mathematical expression

    def solve_math(self, user_input):
        # Step 1: Clean the input by removing unnecessary words and punctuation
        user_input = self.clean_input(user_input)

        # Step 2: Handle word-based numbers and operators
        input_parts = user_input.split()
        for i in range(len(input_parts)):
            # Convert word-based numbers to actual numbers
            number = self.convert_number(input_parts[i])
            if number is not None:
                input_parts[i] = str(number)

        # Step 3: Convert word-based operators to symbols (+, -, *, /)
        user_input = " ".join(input_parts)
        user_input = self.convert_ops(user_input)

        # Step 4: Safely evaluate the mathematical expression
        try:
            # Remove any potential malicious input or code execution risks
            if re.match(r'^[\d+\-*/(). ]+$', user_input):
                result = eval(user_input)
                return result
            else:
                return "Error: Invalid math expression"
        except Exception as e:
            return f"Error: {str(e)}"





class TextOptimizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.contractions = self.load_contractions()
        self.phrases_to_remove = self.load_phrases_to_remove()

    @staticmethod
    def load_contractions():
        return {
            "do not": "don't", "i am": "i'm", "you are": "you're", "we are": "we're",
            "they are": "they're", "is not": "isn't", "are not": "aren't", "cannot": "can't",
            "could not": "couldn't", "would not": "wouldn't", "should not": "shouldn't",
            "will not": "won't", "have not": "haven't", "has not": "hasn't", "had not": "hadn't",
            "it is": "it's", "that is": "that's", "there is": "there's", "what is": "what's",
            "who is": "who's", "where is": "where's", "when is": "when's", "why is": "why's",
            "how is": "how's",
        }

    @staticmethod
    def load_phrases_to_remove():
        try:
            with open('phrases_to_remove.txt', 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def optimize_text(self, text):
        for phrase in self.phrases_to_remove:
            text = text.replace(phrase, "")
        text = self.convert_to_contractions(text)
        return ' '.join(text.split()).strip()

    def convert_to_contractions(self, text):
        for phrase, contraction in self.contractions.items():
            text = re.sub(r'\b' + phrase + r'\b', contraction, text, flags=re.IGNORECASE)
        return text

    @staticmethod
    def trim_response(response_text):
        words = response_text.split()
        return ' '.join(words[:20]) + "..." if len(words) > 20 else response_text

    @staticmethod
    def deep_optimize_response(response_text):
        phrases_to_remove = [
            "has improved", "better ability to", "compared to", "in terms of", "offers improved",
            "provides", "includes", "while", "and also", "specializes in"
        ]
        for phrase in phrases_to_remove:
            response_text = response_text.replace(phrase, "")
        return ' '.join(response_text.split())

    @staticmethod
    def truncate_list(response_text):
        items = response_text.split(",")
        cleaned_items = [item.split(":")[0].strip() for item in items]
        return ", ".join(cleaned_items[:3])


class SUSTAIN:
    def __init__(self, api_key):
        self.api_client = OpenAIClient(api_key)
        self.text_optimizer = TextOptimizer()
        self.cache = {}
        self.math_optimizer = MathOptimizer()

    def answer_math(self, user_input):
        if self.math_optimizer.recognize_math(user_input):
            return self.math_optimizer.solve_math(user_input)
        return None  # If not math, return None

    def get_response(self, user_input):
        math_answer = self.answer_math(user_input)
        if math_answer is not None:
            # Return the math result directly without API call
            return math_answer

        if user_input in self.cache:
            logging.info(f"Cache hit for input: {user_input}")
            return self.cache[user_input]

        optimized_input = self.text_optimizer.optimize_text(user_input)
        original_tokens = self.count_tokens(user_input)
        optimized_tokens = self.count_tokens(optimized_input)
        percentage_saved = self.calculate_percentage_saved(original_tokens, optimized_tokens)

        response_text = self.api_client.get_openai_response(optimized_input)
        logging.info(f"Response: {response_text}, Tokens saved: {percentage_saved:.2f}%")

        self.cache[user_input] = (response_text, percentage_saved)
        return response_text, percentage_saved

    @staticmethod
    def count_tokens(text):
        tokenizer = tiktoken.get_encoding("cl100k_base")
        return len(tokenizer.encode(text))

    @staticmethod
    def calculate_percentage_saved(original_tokens, optimized_tokens):
        if original_tokens <= 0 or optimized_tokens < 0:
            return 0
        tokens_saved = original_tokens - optimized_tokens
        return max((tokens_saved / original_tokens) * 100, 0)
