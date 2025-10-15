import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB, salt):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth, salt) VALUES (?,?,?,?)",
        (username, password, DoB, salt),
    )
    con.commit()
    con.close()


"""def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # parameterised
    #    cur.execute(f"SELECT * FROM users WHERE username = (?)",(username,))
    # original
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")

    if cur.fetchone() == None:
        # no such user exists
        con.close()
        return False
    else:
        # parameterised:
        # cur.execute(f"SELECT * FROM users WHERE password = (?)",(password,))
        # original

        # execute another SELECT to get the password and salt for this username
        cur.execute(f"SELECT password, salt from users WHERE username = '{username}'")

        # students to work out the SELECT query
        # cur.execute("SELECT ...")

        result = cur.fetchone()  # retrieve salt and hashed password for this user
        salt = result[1]
        hashedPw = result[0]

        print(salt, hashedPw)  # salt and hash of this user FROM the database
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

"""


def getSalt(username):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # get the salt from the database
    response = cur.execute("Select salt from users where username = (?)", (username,))
    salt = response.fetchone()[0]
    con.close()
    return salt


def getHashedPassword(salt, password):
    # using the salt, hash the password
    pw = password.encode()
    hash = bcrypt.hashpw(pw, salt)
    return hash


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = (?)", (username,))
    if cur.fetchone() == None:
        # no user with this username
        con.close()
        return False
    else:
        # valid username, continue.
        # get the salt
        salt = getSalt(username)
        hashpw = getHashedPassword(salt, password)
        print(hashpw)
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()


# debugging:
# retrieveUsers("user", "test")
