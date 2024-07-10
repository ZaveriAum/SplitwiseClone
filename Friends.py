import globals


class Friends:

    def __init__(self):
        self.data = globals.DATA
        pass

    def display_friends(self):
        friends = self.data.get_friends(globals.USER.user[0])
        friends_name = self.data.get_friend_name(friends)
        for friend, name in zip(friends, friends_name):
            print(f"Full name: {name}, Balance: {friend[1]} - Id: {friend[0]}")

    def settle_up(self):
        choice = int(input("Please enter the friend id you wanna settle up with: "))
        self.data.settle_up(globals.USER.user[0], choice)

    def add_friend(self, user_id):
        friend_email = input("Please enter your friend's email: ")
        user = self.data.get_user_info(friend_email)
        if not user:
            print("Friend is empty")
            return
        friend_id = user[0]
        self.data.add_friend(user_id, friend_id)


