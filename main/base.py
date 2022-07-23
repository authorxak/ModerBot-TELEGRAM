import sqlite3
import time

db = sqlite3.connect("users.db")
cur= db.cursor()

def creat_table():
    cur.execute('CREATE TABLE IF NOT EXISTS chat(id PRIMARY KEY, user TEXT,nick TEXT)')
    db.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS mute(id PRIMARY KEY, timenow INTEGER,time INTEGER,name TEXT)')
    db.commit()

def banned(id,user,nick):
     cur.execute(f'INSERT INTO chat VALUES(?,?,?)',(id,"@"+user,nick))
     db.commit()

def unbaning(id):
    cur.execute('DELETE FROM chat WHERE id==?',(id,))
    db.commit()

def BlackList():
    list=cur.execute("SELECT * FROM chat").fetchall()
    return list

def mute(id):
    try:
        mit = cur.execute("SELECT * FROM mute WHERE id==?", (id,)).fetchone()
        if not bool(int(mit[1]) >= int(time.time())):
            cur.execute('DELETE FROM mute WHERE id==?', (id,))
            db.commit()
            return False
        else:
            return True
    except:
        error=0

def add_mute(id,num,fname):
    try:
        timer = int(time.time())
        numer = int(num) + timer
        cur.execute(f'INSERT INTO mute VALUES(?,?,?,?)', (id, numer,num,fname))
        db.commit()
    except:
        error=0

def del_mute(id):
    try:
        cur.execute('DELETE FROM mute WHERE id==?', (id,))
        db.commit()
    except:
        error=0
