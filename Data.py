import sqlite3

import globals


class Data:

    def __init__(self):
        self.conn = sqlite3.connect('SpliwiseCloneDB.db')
        self.cursor = self.conn.cursor()

    # ========================================= Friend Creation =============================================
    def get_friends(self, user_id):
        query = """
            SELECT 
                user_id AS friend_id, 
                balance 
            FROM FriendBalances 
            WHERE friend_id = ?

            UNION

            SELECT 
                friend_id, 
                balance 
            FROM FriendBalances 
            WHERE user_id = ?;
            """

        self.cursor.execute(query, (user_id, user_id))
        friends = self.cursor.fetchall()

        return friends

    def get_friend_info(self, friends_id):
        friends = []
        for friend in friends_id:
            query = '''SELECT * FROM Users WHERE Id = ?'''
            self.cursor.execute(query, (friend[0],))
            result = self.cursor.fetchone()
            if result:
                result = list(result)
                result.append(friend[1])
                friends.append(result)  # Append the name only, not the tuple
        return friends

    def settle_up(self, user_id, friend_id):
        query = """
            UPDATE FriendBalances
            SET Balance = 0
            WHERE (user_id = ? AND friend_id = ?)
               OR (user_id = ? AND friend_id = ?);
            """
        try:
            self.cursor.execute(query, (user_id, friend_id, friend_id, user_id))
            self.conn.commit()
        except Exception as e:
            print(e)

    def add_friend(self, user_id, friend_id):
        try:
            query = '''INSERT INTO FriendBalances (User_id, Friend_id, Balance)
                       VALUES (?, ?, ?)'''
            data = (user_id, friend_id, 0)
            self.cursor.execute(query, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction if there's an error

    # ========================================= Group Creation =============================================

    def extract_user_groups(self):
        # Query to get groups created by or involving the current user
        query = """
        SELECT g.Id AS Group_id, g.Group_name, g.Created_by AS Creator_id,
         u.Full_name AS Creator_name, u.Email AS Creator_email, 
               gm.Member_id, mu.Full_name AS Member_name, mu.Email AS Member_email
        FROM Groups g
        JOIN GroupMembers gm ON g.Id = gm.Group_id
        JOIN Users u ON g.Created_by = u.Id
        JOIN Users mu ON gm.Member_id = mu.Id
        WHERE g.Created_by = ?
           OR g.Id IN (SELECT Group_id FROM GroupMembers WHERE Member_id = ?);
        """
        self.cursor.execute(query, (globals.USER.Id, globals.USER.Id))
        rows = self.cursor.fetchall()

        # Process the query results
        for row in rows:
            group_id = row[0]
            group_name = row[1]
            creator_id = row[2]
            creator_name = row[3]
            creator_email = row[4]
            member_id = row[5]
            member_name = row[6]
            member_email = row[7]

            if group_id not in globals.GROUPS_LIST:
                globals.GROUPS_LIST[group_id] = {
                    "group_name": group_name,
                    "created_by": {
                        "user_id": creator_id,
                        "full_name": creator_name,
                        "email": creator_email,
                        "is_current_user": creator_id == globals.USER.Id
                    },
                    "members": {}
                }
            globals.GROUPS_LIST[group_id]["members"][member_id] = {
                "full_name": member_name,
                "email": member_email
            }

    # ========================================= User Operations =============================================
    def create_user(self, full_name, email, password, phone_number):
        query = '''INSERT INTO Users (Full_name, Email, Password, Phone_number)
                Values(?, ?, ?, ?)'''
        data = (full_name, email, password, phone_number)
        self.cursor.execute(query, data)
        self.conn.commit()

    def validate_user_info(self, email):
        query = "SELECT 1 FROm Users Where email = ? LIMIT 1"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        return result is not None

    def get_user_info(self, email):
        self.cursor.execute('SELECT * FROM Users WHERE Email = ?', (email,))
        return self.cursor.fetchone()

    def get_user_id_if_password_matches(self, email, entered_password):
        self.cursor.execute('SELECT id, password FROM users WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        if user:
            user_id, password = user
            if entered_password == password:
                return user_id
        return None

    # ------ Update users info
    def update_user_full_name(self, full_name, user_id):
        self.cursor.execute('''UPDATE USERS
        SET Full_name = ? WHERE Id = ?''', (full_name, user_id))
        self.conn.commit()

    def update_user_email(self, email, user_id):
        self.cursor.execute('''UPDATE USERS
        SET Email = ? WHERE Id = ?''', (email, user_id))
        self.conn.commit()

    def update_user_password(self, password, user_id):
        self.cursor.execute('''UPDATE USERS
        SET Password = ? WHERE Id = ?''', (password, user_id))
        self.conn.commit()

    def update_user_phone_number(self, phone_number, user_id):
        self.cursor.execute('''UPDATE USERS
        SET phone_number = ? WHERE Id = ?''', (phone_number, user_id))
        self.conn.commit()

    # ========================================= Good bye =============================================
    def close_connection(self):
        self.cursor.close()
        self.conn.close()
