from Voting import Voting
from scenarios import scenarios

for scenario in scenarios:
    voting = Voting(scenario['votes'], scenario.get('alliances', []))
    voting.run()
    print(scenario['name'])
    if voting.condorcet_winner:
        print('Condorcet winner: ' + voting.condorcet_winner)
    else:
        print('No Condorcet winner')
        print('Candidates for final round:')
        print(voting.alliance_candidates)
    print('Condorcet winner based on real preferences ', scenario['condorcet_winner'])
