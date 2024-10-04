import copy
import networkx as nx

class Voting:

    def __init__(self, votes=[]):
        self.votes = votes
        self.condorcet_winner = None

    def run(self):
        self.candidates = self.find_all_candidates(self.votes)
        self.condorcet_winner = self.find_condorcet_winner(self.votes)
        if self.condorcet_winner:
            self.winner = self.condorcet_winner
        else:
            smith_set_candidates = self.find_smith_set(self.votes)
            self.winner = self.find_candidate_with_highest_mean_score_of_second_preferences(smith_set_candidates, self.votes)

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
                        if vote[candidate_i] > vote[candidate_j]:
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

    def find_smith_set(self, votes):
        # Step 1: Get the list of all candidates
        candidates = self.find_all_candidates(votes)

        # Step 2: Create a directed graph to represent pairwise victories
        pairwise_wins_graph = nx.DiGraph()

        # Add candidates as nodes
        pairwise_wins_graph.add_nodes_from(candidates)

        # Step 3: Populate the graph with edges based on pairwise victories
        num_voters = len(votes)
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                candidate_i = candidates[i]
                candidate_j = candidates[j]
                
                # Count pairwise victories
                i_wins = sum(1 for vote in votes if vote[candidate_i] > vote[candidate_j])
                j_wins = num_voters - i_wins

                # Add directed edge from the winner to the loser
                if i_wins > j_wins:
                    pairwise_wins_graph.add_edge(candidate_i, candidate_j)
                elif j_wins > i_wins:
                    pairwise_wins_graph.add_edge(candidate_j, candidate_i)

        # Step 4: Find the strongly connected components (SCCs) of the graph
        # The Smith set is the top-most SCC in terms of dominance
        sccs = list(nx.strongly_connected_components(pairwise_wins_graph))

        # Step 5: Sort the SCCs to identify the "top" SCCs
        # We create a condensation graph of SCCs to find the minimal SCC containing the Smith set
        condensation_graph = nx.condensation(pairwise_wins_graph)
        scc_order = list(nx.topological_sort(condensation_graph))
        
        # Step 6: Return the Smith set, which is the smallest SCC containing all dominant candidates
        smith_scc = sccs[scc_order[0]]  # The first SCC in topological order is the Smith set
        return list(smith_scc)
    
    def find_candidate_with_highest_mean_score_of_second_preferences(self, smith_set_candidates, votes):
        # Step 1: Initialize dictionaries to track total second-preference score and count
        second_preference_scores = {candidate: 0 for candidate in smith_set_candidates}
        second_preference_counts = {candidate: 0 for candidate in smith_set_candidates}

        # Step 2: Iterate over each vote to find second preferences
        for vote in votes:
            # Step 3: Find the candidate with the second-highest score (excluding the first preference)
            sorted_candidates = sorted(vote.items(), key=lambda item: item[1], reverse=True)  # Sort by score, highest first
            if len(sorted_candidates) > 1:
                # Get the second-preference candidate
                second_preference_candidate = sorted_candidates[1][0]
                second_preference_score = sorted_candidates[1][1]

                # If the second-preference candidate is in the Smith set, accumulate their score
                if second_preference_candidate in smith_set_candidates:
                    second_preference_scores[second_preference_candidate] += second_preference_score
                    second_preference_counts[second_preference_candidate] += 1

        # Step 4: Calculate mean scores for second preferences
        mean_scores = {}
        for candidate in smith_set_candidates:
            if second_preference_counts[candidate] > 0:
                mean_scores[candidate] = second_preference_scores[candidate] / second_preference_counts[candidate]
            else:
                mean_scores[candidate] = float('-inf')  # If no second preferences, set to negative infinity
        print(mean_scores)
        # Step 5: Find the candidate with the highest mean score for second preferences
        highest_mean_candidate = max(mean_scores, key=mean_scores.get)
        
        return highest_mean_candidate
