import globals


class User:

    def __init__(self, email):
        self.data = globals.DATA
        self.user = self.data.get_user_info(email)
        self.Id = self.user[0]
        self.full_name = self.user[1]
        self.email = self.user[2]
        self.phone_number = self.user[3]
        self.password = self.user[4]

    def edit_full_name(self):
        while True:
            new_name = globals.UTI.get_valid_string("Please enter new full name: ")
            if new_name:
                self.data.update_user_full_name(new_name, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def edit_email(self):
        while True:
            new_email = globals.UTI.get_valid_string("Please enter new email: ")
            if new_email:
                self.data.update_user_email(new_email, self.user[0])
                self.user = self.data.get_user_info(new_email)  # Update self.user with the latest info
                break

    def edit_password(self):
        while True:
            new_password = globals.UTI.get_valid_string("Please enter new password: ")
            if new_password:
                self.data.update_user_password(new_password, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def edit_phone_number(self):
        while True:
            new_phone_number = globals.UTI.get_valid_string("Please enter new phone number")
            if new_phone_number:
                self.data.update_user_phone_number(new_phone_number, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def show_user_info(self):
        print(f"Full name: {self.user[1]}")
        print(f"Email: {self.user[2]}")
        print(f"Phone number: {self.user[3]}")
