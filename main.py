
'''
input is a list of people's rankings
which are just ordered lists
output is ordering of winners


algorithm is:
see if there is a condorcet winner
if there is, see if there is a way of voting tactically to stop there being a condorcet winner
if there is, then have IRV as the tie-breaker;
the voters are again given the opportunity to change their vote.

structure of a vote is {"candidate name": ranking (1-N)}
'''

import copy

class Voting:

    def __init__(self, votes=[]):
        self.votes = votes
        self.condorcet_winner = None

    def run(self):
        self.candidates = self.find_all_candidates(self.votes)
        self.condorcet_winner = self.find_condorcet_winner(self.votes)
        self.find_tactical_voting_strategies_to_prevent_condorcet_winner()
        for tactical_voting_strategy in self.tactical_voting_strategies_to_prevent_condorcet_winner:
            modified_votes = self.apply_promotion_to_votes(tactical_voting_strategy, self.votes)
            print(self.instant_runoff_voting(modified_votes))
        # finally need a step of checking whether there is a strategy to prevent the IRV winner
    
    def find_all_candidates(self, votes):
        # Use a set to avoid duplicates
        candidates_set = set()
        for vote in votes:
            candidates_set.update(vote.keys())
        
        # Convert set to list and store in self.candidates
        return list(candidates_set)

    def find_condorcet_winner(self, votes):
        # Step 1: Get the list of candidates
        candidates = set()
        for vote in self.votes:
            candidates.update(vote.keys())
        candidates = list(candidates)
        
        # Step 2: Create a matrix to store pairwise comparisons
        # wins_matrix[i][j] will count how many voters prefer candidate[i] over candidate[j]
        n = len(candidates)
        wins_matrix = [[0] * n for _ in range(n)]
        
        # Step 3: Populate the pairwise victories matrix
        for vote in votes:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        # Compare candidate[i] vs candidate[j] in the current vote
                        candidate_i = candidates[i]
                        candidate_j = candidates[j]
                        if vote[candidate_i] < vote[candidate_j]:
                            wins_matrix[i][j] += 1

        # Step 4: Determine if there's a Condorcet winner
        for i in range(n):
            is_winner = True
            for j in range(n):
                if i != j and wins_matrix[i][j] <= len(votes) // 2:
                    is_winner = False
                    break
            if is_winner:
                condorcet_winner = candidates[i]
                return condorcet_winner

        # If no Condorcet winner is found
        return None

    def find_tactical_voting_strategies_to_prevent_condorcet_winner(self):
        self.tactical_voting_strategies_to_prevent_condorcet_winner = []
        possible_promotions = self.find_possible_promotions()
        for possible_promotion in possible_promotions:
            votes = self.apply_promotion_to_votes(possible_promotion, self.votes)
            if self.find_condorcet_winner(votes) == None:
                self.tactical_voting_strategies_to_prevent_condorcet_winner.append(possible_promotion)

    def find_possible_promotions(self):
        # Step 1: Create an empty list to store all pairs
        possible_promotions = []
        
        # Step 2: Generate all unique pairs of candidates
        for i in range(len(self.candidates)):
            for j in range(len(self.candidates)):
                if i != j:  # Ensure we don't pair a candidate with itself
                    possible_promotions.append([self.candidates[i], self.candidates[j]])
        
        return possible_promotions
    
    def apply_promotion_to_votes(self, promotion, votes):
        # Create a deep copy of the votes to avoid modifying the original self.votes
        modified_votes = copy.deepcopy(votes)

        # promotion[0]: the candidate to promote
        # promotion[1]: the candidate that will be ranked below the promoted one

        promoted_candidate = promotion[0]
        demoted_candidate = promotion[1]

        for vote in modified_votes:
            # Check if the first preference is the condorcet winner; if so, skip the vote
            first_preference = min(vote, key=vote.get)  # Candidate with rank 1
            if first_preference == self.condorcet_winner:
                continue

            # Get current ranks of promoted_candidate and demoted_candidate
            promoted_rank = vote[promoted_candidate]
            demoted_rank = vote[demoted_candidate]

            # Only promote if promoted_candidate is ranked below demoted_candidate
            if promoted_rank > demoted_rank:
                # Promote promoted_candidate: set its rank to one above demoted_candidate
                vote[promoted_candidate] = demoted_rank

                # Shift all other candidates' ranks accordingly to ensure 1 to N numbering
                for candidate, rank in vote.items():
                    if candidate != promoted_candidate:
                        if rank < demoted_rank:  # Candidates ranked above demoted stay the same
                            continue
                        elif rank >= demoted_rank and rank < promoted_rank:  # Shift down by 1
                            vote[candidate] += 1

        return modified_votes

    def instant_runoff_voting(self, votes):
        # Step 1: Initialize a list of candidates
        candidates = self.find_all_candidates(votes)
        remaining_candidates = candidates[:]
        
        # Step 2: Continue eliminating candidates until we have a winner
        while len(remaining_candidates) > 1:
            # Count first-preference votes for each candidate
            first_preference_counts = {candidate: 0 for candidate in remaining_candidates}
            for vote in votes:
                for candidate in remaining_candidates:
                    if vote[candidate] == 1:  # The candidate is ranked first in this vote
                        first_preference_counts[candidate] += 1
            
            # Check if any candidate has a majority (more than half of the first preference votes)
            total_votes = len(votes)
            for candidate, count in first_preference_counts.items():
                if count > total_votes / 2:
                    return candidate  # We have a winner

            # Step 3: Eliminate the candidate with the fewest first-preference votes
            min_votes = min(first_preference_counts.values())
            candidates_to_eliminate = [candidate for candidate, count in first_preference_counts.items() if count == min_votes]
            
            # Eliminate all candidates with the minimum vote count
            for candidate in candidates_to_eliminate:
                remaining_candidates.remove(candidate)
            
            # Step 4: Adjust the votes to remove the eliminated candidates
            for vote in votes:
                for candidate in candidates_to_eliminate:
                    del vote[candidate]
                # Re-rank the remaining candidates to ensure ranks are sequential from 1 to N
                sorted_candidates = sorted(vote, key=vote.get)
                for i, candidate in enumerate(sorted_candidates):
                    vote[candidate] = i + 1
    
        # Return the last remaining candidate as the winner
        return remaining_candidates[0]



# votes = [
#     {"Alice": 1, "Bob": 2, "Charlie": 3},
#     {"Bob": 1, "Charlie": 2, "Alice": 3},
#     {"Charlie": 1, "Alice": 2, "Bob": 3},
#     {"Alice": 1, "Charlie": 2, "Bob": 3}
# ]

# voting = Voting(votes)
# voting.run()
# print(voting.condorcet_winner)

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

voting = Voting(votes)
voting.run()
