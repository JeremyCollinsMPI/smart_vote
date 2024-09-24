
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
        self.first_past_the_post_winner = self.find_first_past_the_post_winner(self.votes)
        self.condorcet_winner = self.find_condorcet_winner(self.votes)
        if self.condorcet_winner:
            self.winner = self.condorcet_winner
        else:
            candidates = self.find_candidates_preferred_to_first_past_the_post_candidate(self.votes)
            if len(candidates) == 1:
                self.winner = candidates[0]
            else:
                # how should this part be implemented?
                # find the condorcet winner among those candidates if possible..
                raise Exception("Not yet supported")    

    def find_all_candidates(self, votes):
        # Use a set to avoid duplicates
        candidates_set = set()
        for vote in votes:
            candidates_set.update(vote.keys())
        
        # Convert set to list and store in self.candidates
        return list(candidates_set)

    def find_first_past_the_post_winner(self, votes):
        # Step 1: Initialize a list of candidates
        candidates = self.find_all_candidates(votes)
        remaining_candidates = candidates[:]
        
        # Step 2: Count first-preference votes for each candidate
        first_preference_counts = {candidate: 0 for candidate in remaining_candidates}
        for vote in votes:
            # Find the candidate ranked first in this vote
            first_preference_candidate = min(vote, key=vote.get)
            first_preference_counts[first_preference_candidate] += 1
        
        # Step 3: Find the candidate with the most first-preference votes
        winner = max(first_preference_counts, key=first_preference_counts.get)
        
        return winner

    def find_condorcet_winner(self, votes):
        # Step 1: Get the list of candidates
        candidates = set()
        for vote in votes:
            candidates.update(vote.keys())
        candidates = list(candidates)
        candidates = sorted(candidates)
        
        # Step 2: Create a matrix to store pairwise comparisons
        # wins_matrix[i][j] will count how many voters prefer candidate[i] over candidate[j]
        n = len(candidates)
        wins_matrix = [[0] * n for _ in range(n)]
        
        # Step 3: Populate the pairwise victories matrix
        for x, vote in enumerate(votes):
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

    def find_candidates_preferred_to_first_past_the_post_candidate(self, votes):
        # Step 1: Find the first-past-the-post winner
        fptp_winner = self.first_past_the_post_winner
        
        # Step 2: Initialize a list to hold candidates preferred by a majority over the FPTP winner
        candidates_preferred_over_fptp = []
        
        # Step 3: Find all other candidates
        other_candidates = [candidate for candidate in self.candidates if candidate != fptp_winner]

        # Step 4: Compare pairwise between FPTP winner and other candidates
        for candidate in other_candidates:
            # Count how many voters prefer this candidate over the FPTP winner
            count_prefer_candidate = 0
            for vote in votes:
                if vote[candidate] < vote[fptp_winner]:  # Candidate ranked higher than FPTP winner
                    count_prefer_candidate += 1
            
            # Step 5: If more than half the voters prefer this candidate, add them to the list
            if count_prefer_candidate > len(votes) / 2:
                candidates_preferred_over_fptp.append(candidate)

        return candidates_preferred_over_fptp


