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

votes = [
    {"Alice": 1, "Bob": 2, "Charlie": 3},
    {"Bob": 1, "Charlie": 2, "Alice": 3},
    {"Charlie": 1, "Alice": 2, "Bob": 3},
    {"Alice": 1, "Charlie": 2, "Bob": 3}
]

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 2, 'Charlie': 3})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 2, 'Charlie': 3})
for i in range(10):
    votes.append({'Charlie': 1, "Bob": 2, 'Alice': 3})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.1"})

'''
1.2.2 A voter bury B vote
'''

votes = [
    {"Alice": 1, "Bob": 2, "Charlie": 3},
    {"Bob": 1, "Charlie": 2, "Alice": 3},
    {"Charlie": 1, "Alice": 2, "Bob": 3},
    {"Alice": 1, "Charlie": 2, "Bob": 3}
]

votes = []
for i in range(46):
    votes.append({"Alice": 1, 'Bob': 3, 'Charlie': 2})
for i in range(44):
    votes.append({'Bob': 1, "Alice": 2, 'Charlie': 3})
for i in range(10):
    votes.append({'Charlie': 1, "Bob": 2, 'Alice': 3})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.2"})


