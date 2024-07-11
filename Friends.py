import globals


class Friends:

    def __init__(self):
        self.data = globals.DATA

    def get_friends_info(self):
        friends = self.data.get_friends(globals.USER.user[0])
        return self.data.get_friend_info(friends)

    def settle_up(self):
        choice = int(input("Please enter the friend id you wanna settle up with: "))
        self.data.settle_up(globals.USER.user[0], choice)
        for friend in globals.FRIENDS_LIST:
            if choice == friend[0]:
                friend[5] = 0

    def add_friend(self, user_id):
        friend_email = input("Please enter your friend's email: ")
        user = self.data.get_user_info(friend_email)
        friend = list(user)
        friend.append(0)
        globals.FRIENDS_LIST.append(friend)
        if not user:
            print("Friend is empty")
            return
        friend_id = user[0]
        self.data.add_friend(user_id, friend_id)

    def display_friends(self):
        for friend in globals.FRIENDS_LIST:
            if friend[5] > 0:
                print(f"{friend[1]} owes you ${friend[5]} - friend's id: {friend[0]}")
            else:
                print(f"You owe {friend[1]} ${abs(friend[5])} - friend's id: {friend[0]}")


