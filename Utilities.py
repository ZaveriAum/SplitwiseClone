import re

from Data import Data


class Utilities:
    def __init__(self):
        self.data = Data()

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






