import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

#api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro
a = input('Enter location: ')
#if api_key is False:
api_key = 42
serviceurl = a
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#parms = dict()
url = serviceurl #+ urllib.parse.urlencode(parms)
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read()
print('Retrieved',len(data),'characters')
#d = data.decode()
tree = ET.fromstring(data)
lst = tree.findall('comments/comment')  #comment from comments
print('Count:',len(lst))
sum = 0
for item in lst:
    #print('Count', item.find('count').text)
    sum = sum + int(item.find('count').text)
print('Sum:',sum)

# counts = tree.findall('.//count') can also use the XPath selector string
