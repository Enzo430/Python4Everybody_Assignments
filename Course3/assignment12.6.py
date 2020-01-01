# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')   #http://py4e-data.dr-chuck.net/comments_42.html or http://py4e-data.dr-chuck.net/comments_346107.html
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
spans = soup('span')
count = 0
sum = 0
for span in spans:
    count = count + 1
    sum = sum + int(span.contents[0])  #string of the number between <span> </span>

print('Count', count)
print('sum', sum)
