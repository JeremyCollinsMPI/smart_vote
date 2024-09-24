from copy import deepcopy

scenarios = []


'''
1. Three-way races
'''

'''
Scenario 1.1: A is Condorcet winner
'''


'''
Scenario 1.2: B is Condorcet winner
'''

'''
1.2.1 Preferences expressed sincerely
'''

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 2, 'Charlie': 3})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 2, 'Charlie': 3})
for i in range(10):
    votes.append({'Charlie': 1, "Bob": 2, 'Alice': 3})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.1"})

'''
1.2.2 A voters bury B vote
'''

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 3, 'Charlie': 2})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 2, 'Charlie': 3})
for i in range(10):
    votes.append({'Charlie': 1, "Bob": 2, 'Alice': 3})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.2"})


'''
Scenario 1.3: C is Condorcet winner
'''

'''
1.3.1 C voters' second choice is A
'''

'''
1.3.1.1 Preferences expressed sincerely
'''

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 3, 'Charlie': 2})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 3, 'Charlie': 2})
for i in range(10):
    votes.append({'Charlie': 1, "Bob": 3, 'Alice': 2})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Charlie", "name": "1.3.1.1"})

'''
1.2.2 A voters bury C vote
'''

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 2, 'Charlie': 3})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 3, 'Charlie': 2})
for i in range(10):
    votes.append({'Charlie': 1,  'Alice': 2, "Bob": 3})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Charlie", "name": "1.3.1.2"})



'''
vote splitting

top > centre > bottom 25
centre > top > bottom 15
centre > bottom > top 15
bottom > centre > top 39

sincere preferences

'''

votes = []
for i in range(25):
    votes.append({"Top": 1, 'Centre': 2, 'Bottom': 3})
for i in range(15):
    votes.append({"Top": 2, 'Centre': 1, 'Bottom': 3})
for i in range(15):
    votes.append({"Top": 3, 'Centre': 1, 'Bottom': 2})
for i in range(39):
    votes.append({"Top": 3, 'Centre': 2, 'Bottom': 1})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Centre", "name": "vote splitting"})


'''
vote splitting

top > centre > bottom 31
centre > top > bottom 15
centre > bottom > top 15
bottom > centre > top 39

add some more top votes

'''

votes = []
for i in range(31):
    votes.append({"Top": 1, 'Centre': 2, 'Bottom': 3})
for i in range(15):
    votes.append({"Top": 2, 'Centre': 1, 'Bottom': 3})
for i in range(15):
    votes.append({"Top": 3, 'Centre': 1, 'Bottom': 2})
for i in range(39):
    votes.append({"Top": 3, 'Centre': 2, 'Bottom': 1})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Centre", "name": "vote splitting with more top voters"})
