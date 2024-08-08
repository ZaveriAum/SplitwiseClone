import os
import sqlite3
import globals
import json

DB_LOCATION = os.environ.get('DB_LOCATION')


class Data:

    def __init__(self):
        self.conn = sqlite3.connect(DB_LOCATION)
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

    def check_friend_relationship(self, user_id, friend_id):
        # Query to check if the user_id and friend_id pair exists in the FriendBalances table
        query = """
        SELECT COUNT(*)
        FROM FriendBalances
        WHERE (User_id = ? AND Friend_id = ?) OR (User_id = ? AND Friend_id = ?);
        """
        self.cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        count = self.cursor.fetchone()[0]

        # Return True if the relationship exists, False otherwise
        return count > 0

    def add_friend(self, user_id, friend_id):
        if not self.check_friend_relationship(user_id, friend_id) and user_id != friend_id:
            try:
                query = '''INSERT INTO FriendBalances (User_id, Friend_id, Balance)
                           VALUES (?, ?, ?)'''
                data = (user_id, friend_id, 0)
                self.cursor.execute(query, data)
                self.conn.commit()
                print("Friend successfully added.")
            except sqlite3.Error as e:
                print(f"Error occurred: {e}")
                self.conn.rollback()  # Rollback the transaction if there's an error

    # ========================================= Group Creation =============================================

    def extract_user_groups(self):
        # Query to get groups created by or involving the current user
        group_query = """
        SELECT g.Id AS Group_id, g.Group_name, g.Created_by AS Creator_id, u.Full_name AS Creator_name, 
        u.Email AS Creator_email
        FROM Groups g
        LEFT JOIN Users u ON g.Created_by = u.Id
        WHERE g.Created_by = ? OR g.Id IN (
            SELECT Group_id FROM GroupMembers WHERE Member_id = ?
        )
        ORDER BY g.Id;
        """
        self.cursor.execute(group_query, (globals.USER.Id, globals.USER.Id))
        group_rows = self.cursor.fetchall()

        # Process the group query results
        for group_row in group_rows:
            group_id = group_row[0]
            group_name = group_row[1]
            creator_id = group_row[2]
            creator_name = group_row[3]
            creator_email = group_row[4]

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

            # Query to get all members for the current group
            member_query = """
            SELECT gm.Group_id, gm.Member_id, mu.Full_name AS Member_name, mu.Email AS Member_email
            FROM GroupMembers gm
            LEFT JOIN Users mu ON gm.Member_id = mu.Id
            WHERE gm.Group_id = ?;
            """
            self.cursor.execute(member_query, (group_id,))
            member_rows = self.cursor.fetchall()

            # Process the member query results
            for member_row in member_rows:
                member_id = member_row[1]
                member_name = member_row[2]
                member_email = member_row[3]

                globals.GROUPS_LIST[group_id]["members"][member_id] = {
                    "full_name": member_name,
                    "email": member_email
                }
        print(globals.GROUPS_LIST)

    def create_group(self, group_name):
        try:
            self.cursor.execute('''SELECT Id FROM Groups ORDER BY Id DESC LIMIT 1 ''')
            last_id = self.cursor.fetchone()
            query = '''INSERT INTO Groups (Group_name,Created_by)
                    Values(?, ?)'''
            self.cursor.execute(query, (group_name, globals.USER.Id))
            self.conn.commit()
            # Create the new group entry
            new_group = {
                "group_name": group_name,
                "created_by": {
                    "user_id": globals.USER.Id,
                    "full_name": globals.USER.full_name,
                    "email": globals.USER.email,
                    "is_current_user": True  # Assume the creator is not the current user
                },
                "members": {}
            }

            # Insert the new group into the data dictionary
            globals.GROUPS_LIST[last_id[0]] = new_group
            print("Your new group was successfully created")
        except Exception as e:
            print(e)

    def add_member(self, group_id, member_id):
        try:
            # 1. Insert into the database table
            self.cursor.execute('''INSERT INTO GroupMembers (Group_id, Member_id) VALUES (?, ?)''',
                                (group_id, member_id))
            self.conn.commit()

            # 2. Fetch the member information from the Users table
            member_query = '''
            SELECT u.Id, u.Full_name, u.Email
            FROM Users u
            WHERE u.Id = ?;
            '''
            self.cursor.execute(member_query, (member_id,))
            member_info = self.cursor.fetchone()

            if member_info:
                member_id, member_name, member_email = member_info

                # Ensure the group exists in globals.GROUPS_LIST
                if group_id in globals.GROUPS_LIST:
                    globals.GROUPS_LIST[group_id]["members"][member_id] = {
                        "full_name": member_name,
                        "email": member_email
                    }

                # 3. Insert the user and the member into Friend for every member of the group, including the creator
                for existing_member_id in globals.GROUPS_LIST[group_id]["members"]:
                    self.add_friend(int(existing_member_id), member_id)

                # Also add the relationship with the creator if not already included in the members list
                creator_id = globals.GROUPS_LIST[group_id]["created_by"]["user_id"]
                if creator_id not in globals.GROUPS_LIST[group_id]["members"]:
                    self.add_friend(int(creator_id), member_id)
            else:
                print(f"Member with ID {member_id} not found in Users table")

        except Exception as e:
            print(f"An error occurred: {e}")

    # ======================================= Activity Operations ===========================================

    def fetch_user_transactions(self):
        query = '''
        SELECT 
            t.Id AS transaction_id,
            t.Title AS title,
            t.Amount AS amount,
            t.Paid_by AS paid_by,
            p.Full_name AS paid_name,
            c.Contributor_id AS contributor_id,
            u.Full_name AS contributor_name
        FROM Transactions t
        JOIN Users p ON t.Paid_by = p.Id
        LEFT JOIN Contributors c ON t.Id = c.Transaction_id
        LEFT JOIN Users u ON c.Contributor_id = u.Id
        WHERE t.Paid_by = ? OR t.Id IN (
            SELECT Transaction_id 
            FROM Contributors 
            WHERE Contributor_id = ?
        );
        '''

        self.cursor.execute(query, (globals.USER.Id, globals.USER.Id))
        rows = self.cursor.fetchall()

        for row in rows:
            transaction_id, title, amount, paid_by, paid_name, contributor_id, contributor_name = row
            if transaction_id not in globals.TRANSACTIONS:
                globals.TRANSACTIONS[transaction_id] = {
                    "title": title,
                    "amount": amount,
                    "paid_by": paid_by,
                    "paid_name": paid_name,
                    "contributors": {}
                }
            if contributor_id:
                globals.TRANSACTIONS[transaction_id]["contributors"][contributor_id] = {
                    "name": contributor_name
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

    # ------ Update users info ------
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
