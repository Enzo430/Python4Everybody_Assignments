import json
import sqlite3

conn = sqlite3.connect('assignment15.9-rosterdb.sqlite')
cur = conn.cursor() #cursor is like a file handle to a db server

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')
#can also copy this and run in sqlite browser
#executescript means can run multiple sql command in one time.
#The member table is a connector table(many-to-many) which has 2 foreign keys
#UNIQUE means if you are filling the same table with same name twice it will fail the second time

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'

#roster file looks like this:
# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0]; #3 members in one json array/list
    title = entry[1];
    role = entry[2];
    print((name, title, role))

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )                                #not inserting one string twice by using INSERT OR IGNORE
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))    #use SELECT to know the auto incremented primary key
    user_id = cur.fetchone()[0]                                     #[0]: if theres multiple things we selected then choose the first one,or if we got repetitive value, get the old value

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ?)''',
        ( user_id, course_id, role) )

    conn.commit()
