import re


class Utilities:
    def __init__(self):
        pass

    @staticmethod
    def get_valid_integer(prompt):
        while True:
            user_input = input(prompt)
            try:
                # Attempt to convert the input to an integer
                value = int(user_input)
                return value  # Return the valid integer
            except ValueError:
                # If conversion fails, prompt the user again
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_valid_string(prompt="Enter a non-empty string: "):
        while True:
            user_input = input(prompt).strip()  # Strip leading and trailing whitespace
            if user_input:  # Check if the input is not an empty string
                return user_input  # Return the valid string
            else:
                print("Invalid input. The string cannot be empty.")

    @staticmethod
    def valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Use the match function to see iuf the email matches the pattern
        if re.match(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def validate_phone_number(phone_number):
        """
        Validate a phone number.

        :param phone_number: The phone number to validate.
        :return: True if the phone number is valid, otherwise False.
        """
        pattern = r'^(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$'

        # Use the match function to see if the phone number matches the pattern
        if re.match(pattern, phone_number):
            return True
        else:
            return False
