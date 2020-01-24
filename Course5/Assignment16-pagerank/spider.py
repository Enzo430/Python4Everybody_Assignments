#slow because from the web, can be restarted, send links to the db.
#page rank is a separate step that we are going to do after creating the db.
import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup           #parse with beautifulsoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
     error INTEGER, old_rank REAL, new_rank REAL)''')   #takes the old rank, computes the new rank and replaces the new rank with the old rank and does it over and over again

cur.execute('''CREATE TABLE IF NOT EXISTS Links
    (from_id INTEGER, to_id INTEGER)''')                                #many to many

cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''') #in case we have more than one web, doesn't make any difference.

# Check to see if we are already in progress...
cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1') #html is NULL is a indicator which a page has yet been retrieved "order by random" is a nice feature by sqlite.
#Limit 1 means randomly pick a record in this database where the previous statement is true
row = cur.fetchone()        #fetch a row
if row is not None:         #means table has existing data
    print("Restarting existing crawl.  Remove spider.sqlite to start a fresh crawl.")
else :                            #prime this by inserting the URL we start with and insert into it.
    starturl = input('Enter web url or enter: ')
    if ( len(starturl) < 1 ) : starturl = 'http://www.dr-chuck.com/'
    if ( starturl.endswith('/') ) : starturl = starturl[:-1]  #no slash
    web = starturl
    if ( starturl.endswith('.htm') or starturl.endswith('.html') ) :
        pos = starturl.rfind('/')
        web = starturl[:pos]

    if ( len(web) > 1 ) :
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( starturl, ) ) #null at html
        conn.commit()

# Get the current webs (should be called websites)
cur.execute('''SELECT url FROM Webs''') #uses the web table to limit the links, it only does links to the sites that you tell it to do links. the best for page rank is to stick with one site
webs = list()
for row in cur:
    webs.append(str(row[0]))  #the list of the legit urls

print(webs)

many = 0
while True:
    if ( many < 1 ) :
        sval = input('How many pages:')              #find "many" pages
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1

    cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        # print row
        fromid = row[0] #page we started with, which is the primary key
        url = row[1]
    except:
        print('No unretrieved HTML pages found')
        many = 0
        break

    print(fromid, url, end=' ')

    # If we are retrieving this page, there should be no links from it before
    cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) ) #wipe out from the links (connection table) because it's unretrieved
    try:
        document = urlopen(url, context=ctx)

        html = document.read()            #no need for decode because using beautifulsoup
        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )

        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")                    #not gon retrieve if it's jpeg
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue

        print('('+str(len(html))+')', end=' ')

        soup = BeautifulSoup(html, "html.parser")
    except KeyboardInterrupt: #if ctrl+z on win, or ctrl+c on Mac
        print('')
        print('Program interrupted by user...')
        break
    except:
        print("Unable to retrieve or parse page") #if beautifulsoup or something else blew up
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue

    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( url, ) ) #got the new url, set page rank to 1. Give all the pages a normal value and alter that.
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) )
    conn.commit()

    # Retrieve all of the anchor tags
    tags = soup('a')  #use beautifulsoup to pull out all the anchor tags.
    count = 0
    for tag in tags:                      #for loop to pull out all the href
        href = tag.get('href', None)      #get href (the next link)
        if ( href is None ) : continue
        # Resolve relative references like href="/contact"
        up = urlparse(href)
        if ( len(up.scheme) < 1 ) :              #scheme is HTTP or HTTPS
            href = urljoin(url, href)           #if it's a relative references, taking the current URL and hooking it up
        ipos = href.find('#') #check to see if there's an anchor: the # at the end of the url
        if ( ipos > 1 ) : href = href[:ipos] #if we do, delete everything later than the # including the #.
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue     #skip pics
        if ( href.endswith('/') ) : href = href[:-1]      #if we have slash at the end we delete the / [-1] means delete the last element
        # print href
        if ( len(href) < 1 ) : continue

		# Check if the URL is in any of the webs
        found = False
        for web in webs:
            if ( href.startswith(web) ) :           #if not the link in the site, we skip it.
                found = True
                break
        if not found : continue

        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )  #null because we haven't retrieve html
        count = count + 1
        conn.commit()

        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))            #id either was there or we just created
        try:
            row = cur.fetchone() #grab that with fetchone
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue
        # print fromid, toid      from id is og to id is the new link
        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) ) #fromid is the primary key of the page we looking through and length and toid is the id we just created


    print(count)

cur.close()
