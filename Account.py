from Data import Data


class Account:

    def __init__(self, email):
        self.data = Data()
        self.user = self.data.get_user_info(email)

    def edit_full_name(self):
        while True:
            new_name = input("Please enter new full name: ")
            if new_name:
                self.data.update_user_full_name(new_name, self.user[0])
                break

    def edit_email(self):
        while True:
            new_email = input("Please enter new email: ")
            if new_email:
                self.data.update_user_full_name(new_email, self.user[0])
                break

    def edit_password(self):
        while True:
            new_password = input("Please enter new password: ")
            if new_password:
                self.data.update_user_full_name(new_password, self.user[0])
                break

    def edit_phone_number(self):
        while True:
            new_phone_number = input("Please enter new phone number")
            if new_phone_number:
                self.data.update_user_full_name(new_phone_number, self.user[0])
                break

    def show_user_info(self):
        print(f"Full name: {self.user[1]}")
        print(f"Email: {self.user[2]}")
        print(f"Phone number: {self.user[4]}")
