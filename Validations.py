import globals
from User import User


class Validations:

    def __init__(self):
        self.data = globals.DATA
        self.email = ""

    def sign_up(self):
        full_name = globals.UTI.get_valid_string("Please enter your full name.")
        while True:
            email = globals.UTI.get_valid_string("Please enter email.")
            if globals.UTI.valid_email(email):
                break
        while True:
            password = input("Please enter password.")
            re_password = input("Please re enter password.")
            if password == re_password:
                break
        while True:
            phone_number = input("Please enter your phone number")
            if globals.UTI.validate_phone_number(phone_number):
                break
        self.data.create_user(full_name, email, password, phone_number)

    def login(self):
        email = globals.UTI.get_valid_string("Please enter your email :- ")
        password = globals.UTI.get_valid_string("Please enter your password :- ")
        user_id = self.data.get_user_id_if_password_matches(email, password)
        if user_id:
            print(f"Login successful")
            globals.USER = User(email)
            return True
        else:
            print("Invalid email or password.")
            return False
