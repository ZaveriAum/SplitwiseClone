import shutil
import sys

from Validations import Validations
from Account import Account


class Menu:

    def __init__(self):
        self.val = Validations()
        self.acc = None

    @staticmethod
    def print_menu():
        menu_title = "Welcome to SplitWiseClone"
        menu_options = [
            "1. Signup",
            "2. Login",
            "3. Exit"
        ]

        # Print the menu title centered
        print("=" * shutil.get_terminal_size().columns)
        print(menu_title.center(shutil.get_terminal_size().columns))
        print("=" * shutil.get_terminal_size().columns)

        # Print menu options
        for option in menu_options:
            print(option.center(shutil.get_terminal_size().columns))

        print("=" * shutil.get_terminal_size().columns)

    def menu(self):
        while True:
            Menu.print_menu()

            try:
                choice = int(input("Please enter your choice: "))
                if choice == 1:
                    self.val.sign_up()
                elif choice == 2:
                    if self.val.login():
                        self.acc = Account(self.val.email)
                        self.submenu()
                    else:
                        continue
                elif choice == 3:
                    print("Exiting SplitWiseClone. Goodbye!")
                    sys.exit()
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def print_submenu():
        menu_options = [
            "1. Friends",
            "2. Groups",
            "3. Add expanses"
            "4. Activity"
            "5. Account"
            "6. Go Back"
        ]

        print("=" * shutil.get_terminal_size().columns)

        # Print menu options
        for option in menu_options:
            print(option.center(shutil.get_terminal_size().columns))

        print("=" * shutil.get_terminal_size().columns)

    def submenu(self):
        while True:
            Menu.print_submenu()

            try:
                choice = int(input("Please enter your choice: "))
                if choice == 1:
                    self.val.sign_up()
                elif choice == 2:
                    self.val.login()
                elif choice == 3:
                    print("Exiting SplitWiseClone. Goodbye!")
                elif choice == 4:
                    print("Exiting SplitWiseClone. Goodbye!")
                elif choice == 5:
                    self.account_menu()
                elif choice == 6:
                    self.menu()
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def account_menu(self):
        while True:
            Menu.printed_menu_account()

            try:
                choice = int(input("Please enter your choice: "))
                if choice == 1:
                    self.acc.edit_full_name()
                elif choice == 2:
                    self.acc.edit_email()
                elif choice == 3:
                    self.acc.edit_password()
                elif choice == 4:
                    self.acc.edit_phone_number()
                elif choice == 5:
                    self.acc.show_user_info()
                elif choice == 6:
                    self.submenu()
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def printed_menu_account():
        menu_options = [
            "1. Edit Full name",
            "2. Edit Email",
            "3. Edit Password",
            "4. Edit Phone number",
            "5. Show Info"
            "6. Go Back"
        ]

        print("=" * shutil.get_terminal_size().columns)

        # Print menu options
        for option in menu_options:
            print(option.center(shutil.get_terminal_size().columns))

        print("=" * shutil.get_terminal_size().columns)
