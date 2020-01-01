# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')  #http://py4e-data.dr-chuck.net/known_by_Fikret.html or http://py4e-data.dr-chuck.net/known_by_Mia.html
print("Retriving:",url)
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
count = int(input('Enter count: '))
position = int(input('Enter position: '))
tags = soup('a')
n = 0
c = 0
while c < count:
    c = c + 1
    for tag in tags:
        n = n + 1
        #print (n)
        if n == position:
            url = tag.get('href', None)
            print("Retriving:",url)
            html = urllib.request.urlopen(url, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')
            tags = soup('a')
            break
    #print (c)
    n = 0 #forgot to add this got me stucked but deugged by printing
