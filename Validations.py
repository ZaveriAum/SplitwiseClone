from Utilities import Utilities
import globals
from User import User


class Validations:

    def __init__(self):
        self.data = globals.DATA
        self.email = ""

    def sign_up(self):
        while True:
            full_name = input("Please enter your full name.")
            if full_name:
                break
        while True:
            email = input("Please enter email.")
            if Utilities.valid_email(email):
                break
        while True:
            password = input("Please enter password.")
            re_password = input("Please re enter password.")
            if password == re_password:
                break
        while True:
            phone_number = input("Please enter your phone number")
            if Utilities.validate_phone_number(phone_number):
                break
        self.data.create_user(full_name, email, password, phone_number)

    def login(self):
        email = input("Please enter your email :- ")
        password = input("Please enter your password :- ")
        user_id = self.data.get_user_id_if_password_matches(email, password)
        if user_id:
            print(f"Login successful. Your User id is {user_id}.")
            globals.USER = User(email)
            return True
        else:
            print("Invalid email or password.")
            return False
