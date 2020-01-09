import sqlite3

conn = sqlite3.connect('assignment15.5-orgdb.sqlite') #if no such file, auto creates one
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Organization_Counts') #if already exists same table drop it.

cur.execute('''
CREATE TABLE Organization_Counts (org TEXT, count INTEGER)''') #triple quote because long string

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
#if (len(fname) < 1): fname = 'mbox-short.txt' for testing
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    user_n_domain = email.split('@')
    org = user_n_domain[1]
    cur.execute('SELECT count FROM Organization_Counts WHERE org = ? ', (org,)) #not reading data, just open and make sure syntax is right. dangerous to put user-entered data in to SQL. ? is the place holder to make sure we dont allow SQL injection (email,) is a tuple with only email in it.
    row = cur.fetchone() #grab the first one
    if row is None:
        cur.execute('''INSERT INTO Organization_Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Organization_Counts SET count = count + 1 WHERE org = ?', #use update because might be multiple apps in one data base.
                    (org,))
    conn.commit() #transfer from memory to disk/drive can be commit every 10/100 times.
#tested, if commit is outside the loop, it can get the result in less than 0.1s, if inside as it is rn, it's taking more than 5 sec.

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Organization_Counts ORDER BY count DESC LIMIT 10' #DESC: descend #could also use SLECT *

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
