import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

# Find the ids that send out page rank - we only are interested
# in pages in the SCC that have in and out links
cur.execute('''SELECT DISTINCT from_id FROM Links''')  #DISTINCT throws out any duplicates, slow run
from_ids = list()
for row in cur:
    from_ids.append(row[0])

# Find the ids that receive page rank
to_ids = list()
links = list()
cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id : continue
    if from_id not in from_ids : continue
    if to_id not in from_ids : continue # we don't want links that point to nowhere
    links.append(row)
    if to_id not in to_ids : to_ids.append(to_id) #strongly connected component
#for every id theres a path from every ID to every other ID eventually
# Get latest page ranks for strongly connected component
prev_ranks = dict()
for node in from_ids:
    cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0] #dictionary based on the primary key(id) (node), = row[0] (rank) a dic of id map to new rank
    #so prev_ranks contains both id and rank
sval = input('How many iterations:')
many = 1
if ( len(sval) > 0 ) : many = int(sval)

# Sanity check
if len(prev_ranks) < 1 :
    print("Nothing to page rank.  Check data.")
    quit()

# Lets do Page Rank in memory so it is really fast
for i in range(many):
    # print prev_ranks.items()[:5]
    next_ranks = dict(); #take the previous ranks, and loop through them
    total = 0.0
    for (node, old_rank) in list(prev_ranks.items()): #node: id, old_rank: previous rank)
        total = total + old_rank #for each node, total rank is total+old_rank
        next_ranks[node] = 0.0
    # print total

    # Find the number of outbound links and sent the page rank down each
    for (node, old_rank) in list(prev_ranks.items()):
        # print node, old_rank
        give_ids = list() #out bound Links
        for (from_id, to_id) in links:
            if from_id != node : continue #not link to itself
           #  print '   ',from_id,to_id

            if to_id not in to_ids: continue
            give_ids.append(to_id) #ids that node is going to share goodness, applies like a filter
        if ( len(give_ids) < 1 ) : continue
        amount = old_rank / len(give_ids) #how much goodness is going to share outbounds based on old_rank and the nuumber of outbound links we have
        # print node, old_rank,amount, give_ids

        for id in give_ids:
            next_ranks[id] = next_ranks[id] + amount
            #all the ids we giving it to, we started the next_ranks being 0,
            #these receiving end, add the amount of page rank to each one
            #eventually all the incoming links will have been granted each new link value
    newtot = 0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank #calculate the new total
    evap = (total - newtot) / len(next_ranks) #evap: in page rank algorithm there are dysfunctional shapes in which pagerank can be trapped
    #evaporation is taking a fraction away from everyone and giving it back to everyone else.

    # print newtot, evap
    for node in next_ranks:
        next_ranks[node] = next_ranks[node] + evap

    newtot = 0
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank

    # Compute the per-page average change from old rank to new rank
    # As indication of convergence of the algorithm
    totdiff = 0
    for (node, old_rank) in list(prev_ranks.items()): #calculating the average difference between the page ranks
        new_rank = next_ranks[node]      #tell us the stability of the page rank
        diff = abs(old_rank-new_rank)    #from 1 iteration to the next, the more it changes, the least stable it is
        totdiff = totdiff + diff         #the more iterations we run, the more stablized the ranks are.

    avediff = totdiff / len(prev_ranks)  #whats the avg diff in the page rank per node
    print(i+1, avediff)

    # rotate
    prev_ranks = next_ranks
#not updating to the db through iterations, but do it at the very end.
# Put the final ranks back into the database
print(list(next_ranks.items())[:5])
cur.execute('''UPDATE Pages SET old_rank=new_rank''')
for (id, new_rank) in list(next_ranks.items()) :
    cur.execute('''UPDATE Pages SET new_rank=? WHERE id=?''', (new_rank, id))
conn.commit()
cur.close()
