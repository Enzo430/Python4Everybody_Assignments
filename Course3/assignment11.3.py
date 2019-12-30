import re                         #question see html file
handle = open('regex_sum_346105.txt')
tot = 0
for line in handle:
    a = re.findall("[0-9]+",line)   #one or more digits only
    for num in a:
        n = int(num)
        tot = tot + n
print(tot)
