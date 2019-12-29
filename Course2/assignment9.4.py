#9.4 Write a program to read through the mbox-short.txt and figure out who has sent the greatest number of mail messages. The program looks for 'From ' lines and takes the second word of those lines as the person who sent the mail. The program creates a Python dictionary that maps the sender's mail address to a count of the number of times they appear in the file. After the dictionary is produced, the program reads through the dictionary using a maximum loop to find the most prolific committer.
name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
pool = dict()
for line in handle:
    if "From " in line:
        w = line.split()
        email = w[1]
        pool[email] = pool.get(email,0)+1
most = None  #most send email address
maxva = None #most value
for email,value in pool.items():
    if maxva is None or value > maxva:  #or maxva = 0 /n if value > maxva:
       most = email                     #which makes the code shorter
       maxva = value
print(most,maxva)
