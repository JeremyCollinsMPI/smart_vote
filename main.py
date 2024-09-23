from Voting import Voting
from scenarios import scenarios

for scenario in scenarios:
    voting = Voting(scenario['votes'])
    voting.run()
    print(scenario['name'])
    print(voting.winner)
    print('Condorcet winner based on real preferences ', scenario['condorcet_winner'])
