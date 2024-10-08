import copy
import networkx as nx

class Voting:

    def __init__(self, votes=[], alliances=[]):
        self.votes = votes
        self.condorcet_winner = None
        self.alliances = alliances
        self.sort_alliances_in_reverse_order_by_length()

    def sort_alliances_in_reverse_order_by_length(self):
        self.alliances = sorted(self.alliances, key=lambda x:len(x), reverse=True)

    def run(self):
        self.candidates = self.find_all_candidates(self.votes)
        self.condorcet_winner = self.find_condorcet_winner(self.votes, self.candidates)
        if self.condorcet_winner:
            self.winner = self.condorcet_winner
        else:
            smith_set_candidates = self.find_smith_set(self.votes)
            for alliance in self.alliances:
                self.alliance_candidates = self.find_alliance_candidates(smith_set_candidates, alliance)

    def find_all_candidates(self, votes):
        # Use a set to avoid duplicates
        candidates_set = set()
        for vote in votes:
            candidates_set.update(vote.keys())
        
        # Convert set to list and store in self.candidates
        return list(candidates_set)

    def find_condorcet_winner(self, votes, candidates):
        # Step 1: Get the list of candidates
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
    
    def find_alliance_candidates(self, smith_set_candidates, alliance):
        return [x for x in smith_set_candidates if x in alliance]
