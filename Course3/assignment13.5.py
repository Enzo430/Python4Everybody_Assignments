import urllib.request, urllib.parse, urllib.error
import json
import ssl

url = input('Enter Location:')
#url = 'http://py4e-data.dr-chuck.net/comments_42.json'
#url = 'http://py4e-data.dr-chuck.net/comments_346110.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read()
info = json.loads(data)            #parse the data and make a structured object
print('Retrieved',len(data),'characters')
#print(json.dumps(data, indent=4))
items = info['comments']           #names and counts are in the comments dictionary
#print(items)
count = 0
sum = 0
for item in items:
    #print(item['name'])
    count = count + 1
    sum = sum + int(item['count'])

print('count:',count)
print('sum:',sum)
