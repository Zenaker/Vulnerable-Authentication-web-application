import sqlite3

def createAccount(email, password):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("INSERT INTO users VALUES(?, ?)", (email, password,),)
    db.commit()
    conn.close()


def getPassword(email):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("SELECT password FROM users WHERE email=?", (email,))
    password = conn.fetchone()[0]
    db.commit()
    conn.close()

    return password

def changePassword(email, password):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("UPDATE users SET password=? WHERE email=?", (password, email,))
    db.commit()
    conn.close()


def addEmailHash(email, hash):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("INSERT INTO forgot_password VALUES(?, ?)", (email, hash,))
    db.commit()
    conn.close()


def getEmailFromHash(hash):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("SELECT email FROM forgot_password WHERE hash=?", (hash,))
    email = conn.fetchone()
    db.commit()
    conn.close()

    if email:
        return email[0]

    return False


def removeHashEntry(hash):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("DELETE FROM forgot_password WHERE hash=?", (hash,))
    db.commit()
    conn.close()


def emailExist(email):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    conn.execute("SELECT email FROM users WHERE email=?", (email,))
    email = conn.fetchone()

    if email:
        return True
    
    return False
