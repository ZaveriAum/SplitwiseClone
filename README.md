Hello everyone,

This is a console Splitwise clone which only contamplates the core usage of splitewise app.
Although it has most of the functionality the splitwise app has but we have focused towards the main aspect which is corrent distribution of the money between individuals which are connected.

To run this to your machine you will require a SQLITE DB we have given script for that below.

"""""
CREATE TABLE Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Full_name TEXT,
    Email TEXT UNIQUE,
    Phone_number TEXT UNIQUE,
    Password TEXT
);

CREATE TABLE Transactions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    Amount REAL,
    Date TEXT,
    Paid_by INTEGER,
    Transaction_type TEXT,  -- 'friend' or 'group'
    Split_method TEXT,      -- 'split_equally', 'full_repayment', etc.
    Group_id INTEGER,       -- NULL if it's a friend transaction
    FOREIGN KEY (Paid_by) REFERENCES Users(Id),
    FOREIGN KEY (Group_id) REFERENCES Groups(Id)
);


CREATE TABLE FriendBalances (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    User_id INTEGER,
    Friend_id INTEGER,
    Balance REAL,
    FOREIGN KEY (User_id) REFERENCES Users(Id),
    FOREIGN KEY (friend_id) REFERENCES Users(id)
);


CREATE TABLE Groups (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Group_name TEXT,
    Created_by INTEGER,
    FOREIGN KEY (Created_by) REFERENCES Users(Id)
);

CREATE TABLE GroupMembers (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Group_id INTEGER,
    Member_id INTEGER,
    FOREIGN KEY (Group_id) REFERENCES Groups(Id),
    FOREIGN KEY (Member_id) REFERENCES Users(Id)
);

CREATE TABLE GroupParticipants (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Transaction_id INTEGER,
    User_id INTEGER,
    FOREIGN KEY (Transaction_id) REFERENCES Transactions(Id),
    FOREIGN KEY (User_id) REFERENCES Users(Id)
);

"""""
