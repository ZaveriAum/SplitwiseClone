import globals
from Data import Data


class Friends:

    def __init__(self):
        self.data = Data()
        pass

    def display_friends(self):
        friends = self.data.get_friends(globals.USER.user[0])
        for friend in friends:
            print(f"Friend ID: {friend[0]}, Balance: {friend[1]}")


