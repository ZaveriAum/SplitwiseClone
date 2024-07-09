from Data import Data


class User:

    def __init__(self, email):
        self.data = Data()
        self.user = self.data.get_user_info(email)
        # Here user is structured as user[0] = Id, user[1] = Full_name, user[2] = Email, user[3] = Phone_number,
        #                            user[4] = Password

    def edit_full_name(self):
        while True:
            new_name = input("Please enter new full name: ")
            if new_name:
                self.data.update_user_full_name(new_name, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def edit_email(self):
        while True:
            new_email = input("Please enter new email: ")
            if new_email:
                self.data.update_user_email(new_email, self.user[0])
                self.user = self.data.get_user_info(new_email)  # Update self.user with the latest info
                break

    def edit_password(self):
        while True:
            new_password = input("Please enter new password: ")
            if new_password:
                self.data.update_user_password(new_password, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def edit_phone_number(self):
        while True:
            new_phone_number = input("Please enter new phone number")
            if new_phone_number:
                self.data.update_user_phone_number(new_phone_number, self.user[0])
                self.user = self.data.get_user_info(self.user[2])  # Update self.user with the latest info
                break

    def show_user_info(self):
        print(f"Full name: {self.user[1]}")
        print(f"Email: {self.user[2]}")
        print(f"Phone number: {self.user[3]}")
