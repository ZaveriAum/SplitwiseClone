import sqlite3


class Data:

    def __init__(self):
        self.conn = sqlite3.connect('SpliwiseCloneDB.db')
        self.cursor = self.conn.cursor()

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
        self.cursor.execute('SELECT * FROM Users WHERE Email = ?', (email, ))
        return self.cursor.fetchone()

    def get_user_id_if_password_matches(self, email, entered_password):
        self.cursor.execute('SELECT id, password FROM users WHERE email = ?', (email, ))
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

    # ========================================= Friend Creation =============================================

    # ========================================= Group Creation =============================================

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
