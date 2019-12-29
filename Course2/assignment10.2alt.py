#10.2 Write a program to read through the mbox-short.txt and figure out the distribution by hour of the day for each of the messages. You can pull the hour out from the 'From ' line by finding the time and then splitting the string a second time using a colon.
#From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
#Once you have accumulated the counts for each hour, print out the counts, sorted by hour as shown below.
name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
h = open(name)
store = dict()
for line in h:
    if "From " in line:
        line = line.rstrip()
        a = line.split()
        time = a[5]
        b = time.split(":")
        hour = b[0]
        store[hour] = store.get(hour,0)+1
s = sorted(store.items())
for h,val in s:
    print(h,val)
