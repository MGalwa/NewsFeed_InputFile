# Magdalena Galwa
# 19/09/2025
# Description:

# Homework:
# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# Define your input format (one or many records)
# Default folder or user provided file path
# Remove file if it was successfully processed
# Apply case normalization functionality form Homework 3/4

import os  # Importing the os module for file and directory operations
from datetime import datetime  # Importing datetime module for working with dates and times


# Class GUI - responsible for displaying information and capturing the user's choice
class GUI:
    def __init__(self):
        # Display the opening menu and instructions at the start of the application
        self.show_menu_options()

    def show_menu_options(self):
        # Display the application's initial menu options
        self.display_message("=== News Feed Tool ===")  # Application header
        self.display_message("Choose one of the options:")  # Inform user of available menu options
        self.display_message("1 - News Feed")  # Option 1: News
        self.display_message("2 - Private Ad")  # Option 2: Private Ad
        self.display_message("3 - Book Review")  # Option 3: Book Review
        self.display_message("\nA default input file will be created in:")  # Show input file location
        self.display_message(r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\NewsFeed_InputFile\input.txt")
        self.display_message("After filling the file, you can process it.")  # How to proceed with the app

    def display_message(self, message):
        # Centralized method to print messages to the console
        print(message)  # Print the given message in terminal

    def get_user_choice(self):
        # Get and validate the user's choice from the menu
        while True:  # Repeat until a valid choice is provided
            try:
                choice = int(input("Enter your choice (1, 2, 3): "))  # Prompt user to input a choice
                if choice in [1, 2, 3]:  # Check if the choice is valid (1, 2, or 3)
                    return choice  # Return the valid choice
                else:
                    self.display_message("Invalid choice. Please select 1, 2, or 3.")  # Handle invalid choices
            except ValueError:
                self.display_message("Invalid input. Please enter the number 1, 2, or 3.")  # Handle non-integer inputs


# Class User - represents the user and their selected category choice
class User:
    def __init__(self, gui):
        self.gui = gui  # Reference to the GUI instance for displaying messages
        self.choice = self.gui.get_user_choice()  # Store the user's menu choice (1, 2, or 3)


# Class for the News category
class News:
    def __init__(self, text, city):
        self.text = text  # The message body of the news
        self.city = city  # The city associated with the news
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")  # Full timestamp for internal processing
        self.publication_date = datetime.now().strftime("%d/%m/%Y")  # Only date for output formatting

    def __str__(self):
        # Format the News record as a string for saving in the output file
        # Includes the text, city, and publication date in separate lines
        return f"News ------------------------\n{self.text}\n{self.city}\nPublished on: {self.publication_date}\n"


# Class for the Private Ad category
class AdPrivate:
    def __init__(self, text, expire_date):
        self.text = text  # The message body of the private ad
        self.expire_date = expire_date  # Expiration date entered by the user

    def __str__(self):
        # Calculate the number of days remaining until the expiration date
        days_left = (self.expire_date - datetime.now().date()).days
        # Format the Private Ad record for saving in the output file
        return f"Private Ad ------------------------\n{self.text}\nActual until: {self.expire_date}, {days_left} days left\n"


# Class for the Book Review category
class BookReview:
    def __init__(self, text, rate):
        self.text = text  # The message body of the book review
        self.rate = rate  # Rating for the book (1-5)
        self.publication_date = datetime.now().strftime("%d/%m/%Y")  # Current date for output formatting

    def __str__(self):
        # Format the Book Review record for saving in the output file
        return f"Book Review ------------------------\n{self.text}\nRate: {self.rate}/5\nPublished on: {self.publication_date}\n"


# Class FileProcessor - responsible for handling input and output files
class FileProcessor:
    def __init__(self):
        # Paths to the input and output files
        self.input_file_path = r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\NewsFeed_InputFile\input.txt"
        self.output_file_path = "output.txt"  # The output file where records are saved

    def create_input_file(self, choice, gui):
        # Create an input file with an example based on the user's choice
        examples = {
            1: "Today it's raining. Take your umbrella.;Gliwice",  # Example for News
            2: "I want to sell a bike;2026-02-02",  # Example for Private Ad
            3: "This book is amazing. Excellent storytelling.;5"  # Example for Book Review
        }

        # Create the directory for the input file if it doesn't exist
        input_dir = os.path.dirname(self.input_file_path)
        os.makedirs(input_dir, exist_ok=True)  # Ensure the directory exists

        # If the input file doesn't already exist, create it with an example
        if not os.path.exists(self.input_file_path):
            with open(self.input_file_path, "w", encoding="utf-8") as file:
                file.write("# Add your records here.\n")  # Add a comment at the top of the file
                file.write(f"# Example for this category: {examples[choice]}\n")  # Add an example line
                gui.display_message(f"Input file '{self.input_file_path}' has been created. Please fill it with data.")  # Inform the user

    def normalize_text(self, text, capitalize_all_words=False):
        """
        Normalize the provided text:
        - Capitalize the first character of the text and any character following ". ".
        - If capitalize_all_words=True, also capitalize characters after spaces (for cities with multiple words).
        """
        normalized_text = text.lower()  # Convert the entire text to lowercase
        result = ""  # Initialize an empty string to store the normalized result
        capitalize_next = True  # Start by capitalizing the first letter

        for char in normalized_text:  # Iterate through each character in the text
            if capitalize_next:  # If the flag is set, capitalize the character
                result += char.upper()
                capitalize_next = False  # Reset the flag
            else:
                result += char  # Otherwise, add the character as is

            if char == ".":  # Set the flag after a period (end of a sentence)
                capitalize_next = True
            elif capitalize_all_words and char == " ":  # Set the flag after spaces if capitalize_all_words=True
                capitalize_next = True

        return result  # Return the fully normalized text

    def read_and_validate_records(self, choice, gui):
        # Process and validate records from the input file
        records = []  # List to store validated records

        # Check if the input file exists
        if not os.path.exists(self.input_file_path):
            gui.display_message("Input file not found. Please ensure the file exists.")
            return None

        # Read all valid lines (skip empty lines and comments)
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

        if not lines:  # If the file is empty, inform the user
            gui.display_message("Input file is empty. Please provide valid records.")
            return None

        for line in lines:  # Iterate through each line in the file
            try:
                parts = line.split(";")  # Split the line into components using `;`
                if choice == 1 and len(parts) == 2:  # News category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    city = self.normalize_text(parts[1], capitalize_all_words=True)  # Normalize the city name
                    records.append(News(text, city))
                elif choice == 2 and len(parts) == 2:  # Private Ad category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    expire_date = datetime.strptime(parts[1], "%Y-%m-%d").date()  # Validate expiration date
                    if expire_date <= datetime.now().date():  # Check if date is in the future
                        raise ValueError("Expiration date must be a future date.")
                    records.append(AdPrivate(text, expire_date))
                elif choice == 3 and len(parts) == 2:  # Book Review category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    rate = int(parts[1])  # Ensure the rate is a valid integer
                    if rate < 1 or rate > 5:  # Validate rating range (1-5)
                        raise ValueError("Rate must be between 1 and 5.")
                    records.append(BookReview(text, rate))
                else:
                    raise ValueError("Invalid format or missing fields.")
            except Exception as e:  # Handle any errors in processing
                gui.display_message(f"Error processing line '{line}': {e}")
                gui.display_message("Please correct the input file and try again.")
                return None

        return records  # Return the list of validated records

    def save_to_output_file(self, records, gui):
        # Save all validated records to the output file
        if not os.path.exists(self.output_file_path):
            # If the file doesn't exist, create it with a header
            with open(self.output_file_path, "w", encoding="utf-8") as file:
                file.write("News Feed App\n\n")

        # Append each record to the file
        with open(self.output_file_path, "a", encoding="utf-8") as file:
            for record in records:
                file.write(str(record) + "\n")  # Convert each record to a string and add it to the file
        gui.display_message(f"All records have been saved to '{self.output_file_path}'.")

    def remove_input_file(self, gui):
        # Delete the input file after successful processing
        try:
            os.remove(self.input_file_path)  # Remove the file from the directory
            gui.display_message(f"Input file '{self.input_file_path}' has been successfully deleted.")
        except Exception as e:  # Handle any errors during deletion
            gui.display_message(f"Error deleting the input file: {e}")


# Main execution logic
if __name__ == "__main__":
    gui = GUI()  # Create a GUI instance to display messages
    user = User(gui)  # Get the user's choice of category
    processor = FileProcessor()  # Create an instance of FileProcessor for file operations
    processor.create_input_file(user.choice, gui)  # Create an input file based on the user's category choice

    while True:  # Run the main loop until the user decides to exit
        gui.display_message("\nType '1' to process the input file after filling it.")  # Prompt to process the file
        gui.display_message("Type '2' to exit the application.")  # Prompt to exit the application
        user_action = input("Your choice: ").strip()  # Get the user's action

        if user_action == "1":  # If the user chooses to process the file
            records = processor.read_and_validate_records(user.choice, gui)  # Read and validate the records
            if records:  # If valid records exist
                processor.save_to_output_file(records, gui)  # Save the records to the output file
                processor.remove_input_file(gui)  # Remove the input file after processing
                gui.display_message("Processing completed. Exiting the application.")  # Inform the user
                break  # Exit the application
            else:  # No valid records were found
                gui.display_message("No valid records found. Please fix the input file.")  # Inform the user
        elif user_action == "2":  # If the user chooses to exit the application
            gui.display_message("Exiting application.")  # Inform the user of exiting
            break
        else:  # If the user's input is invalid
            gui.display_message("Invalid input. Please enter '1' or '2'.")  # Inform the user