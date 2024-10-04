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
    votes.append({"Alice": 100, 'Bob': 50, 'Charlie': 0})
for i in range(44):
    votes.append({'Bob': 100, "Alice": 50, 'Charlie': 0})
for i in range(10):
    votes.append({'Charlie': 100, "Bob": 50, 'Alice': 0})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.1"})

'''
1.2.2 A voters bury B vote
'''

'''
1.2.2.1 A voters have a higher score for C than the other candidates have
'''

votes = []
for i in range(46):
    votes.append({"Alice": 100, 'Bob': 0, 'Charlie': 55})
for i in range(44):
    votes.append({'Bob': 100, "Alice": 50, 'Charlie': 0})
for i in range(10):
    votes.append({'Charlie': 100, "Bob": 50, 'Alice': 0})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.2.1"})


'''
1.2.2.2 A voters have a lower score for C than the other candidates have
'''

votes = []
for i in range(46):
    votes.append({"Alice": 100, 'Bob': 0, 'Charlie': 50})
for i in range(44):
    votes.append({'Bob': 100, "Alice": 50, 'Charlie': 0})
for i in range(10):
    votes.append({'Charlie': 100, "Bob": 55, 'Alice': 0})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Bob", "name": "1.2.2.2"})





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
    votes.append({"Alice": 100, 'Bob': 0, 'Charlie': 50})
for i in range(44):
    votes.append({'Bob': 100, "Alice": 0, 'Charlie': 50})
for i in range(10):
    votes.append({'Charlie': 100, "Bob": 0, 'Alice': 50})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Charlie", "name": "1.3.1.1"})

'''
1.2.2 A voters bury C vote
'''

votes = []
for i in range(46):
    votes.append({"Alice": 100, 'Bob': 50, 'Charlie': 0})
for i in range(44):
    votes.append({'Bob': 100, "Alice": 0, 'Charlie': 50})
for i in range(10):
    votes.append({'Charlie': 100,  'Alice': 50, "Bob": 0})

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
    votes.append({"Top": 100, 'Centre': 50, 'Bottom': 0})
for i in range(15):
    votes.append({"Top": 50, 'Centre': 100, 'Bottom': 0})
for i in range(15):
    votes.append({"Top": 0, 'Centre': 100, 'Bottom': 50})
for i in range(39):
    votes.append({"Top": 0, 'Centre': 50, 'Bottom': 100})

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
    votes.append({"Top": 100, 'Centre': 50, 'Bottom': 0})
for i in range(15):
    votes.append({"Top": 50, 'Centre': 100, 'Bottom': 0})
for i in range(15):
    votes.append({"Top": 0, 'Centre': 100, 'Bottom': 50})
for i in range(39):
    votes.append({"Top": 0, 'Centre': 50, 'Bottom': 100})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "Centre", "name": "vote splitting with more top voters"})

'''
four candidate condorcet cycle

40 voters prefer the order: A > B > C > D
35 voters prefer: B > C > D > A
25 voters prefer: C > D > A > B
10 voters prefer: D > A > B > C

first past the post winner is A

the challengers would be ones preferred to A;
which in this case are D and C.
my recursive method;
fptp winner of B, C, D is B.
who is preferred to B.

maybe you just look at the challengers who are available, 
and you find the condorcet winner among just those challengers
in this case the challengers are D and C;

'''

votes = []
for i in range(40):
    votes.append({"A": 100, "B": 75, "C": 50, "D": 25})
for i in range(35):
    votes.append({"A": 25, "B": 100, "C": 75, "D": 50})
for i in range(25):
    votes.append({"A": 50, "B": 25, "C": 100, "D": 75})
for i in range(10):
    votes.append({"A": 75, "B": 50, "C": 25, "D": 100})

scenarios.append({"votes": deepcopy(votes), "condorcet_winner": "None", "name": "four way condorcet cycle"})
