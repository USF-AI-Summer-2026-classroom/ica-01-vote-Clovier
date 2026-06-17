from candidate import Candidate
from voter import Voter

import random
import heapq

class VotingSystem:
    def __init__(self):
        self.candidates = []
        self.voters = []

    def generate_candidates(self, count):
        names = ['Aang', 'Katara', 'Sokka', 'Zuko', 'Iroh', 'Appa', 'Momo', 'Toph', 'Azula', 'Suki', 'Ozai', 'Mai', 'Ty']
        self.candidates = [
            Candidate(
                name=names[i],
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def generate_voters(self, count):
        self.voters = [
            Voter(
                id=i + 1,
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def ballot_view(self):
        """Runs the ranked choice and return the candidat winner"""
        eliminated = set()

        ballots = [
            self.ranked_choice_votes(voter) for voter in self.voters
        ]

        round_number = 1
        while True:
            count = {}

            for ballot in ballots:
                while True:
                    _, _, candidate = ballot[0]
                    if candidate not in eliminated:
                        break
                    heapq.heappop(ballot)
                count[candidate] = count.get(candidate, 0) + 1

            results = []
            
            for candidate, votes in count.items():
                percentage = votes / len(self.voters) * 100
                results.append(f"{candidate.name}: {percentage:.0f}%")
            print(f"Round {round_number}:", results)

            # candidate with the majority % wins
            for candidate, votes in count.items():
                if votes / len(self.voters) > 0.5:
                    return candidate

            # if there is no majority, then drop the lowest %, move on to the next round
            least = min(count, key=count.get)
            eliminated.add(least)
            round_number += 1 # increment round 

    def ranked_choice_votes(self, voter: Voter):
        """Return the choices / votes from each Voter instance"""
        priorityQueue = []

        for i, candidate in enumerate(self.candidates):
            abs_distance = abs(voter.leaning - candidate.leaning)
            heapq.heappush(priorityQueue, (abs_distance, i, candidate))
        return priorityQueue
            

if __name__ == "__main__":
    voting_system = VotingSystem()

    voting_system.generate_candidates(5)
    voting_system.generate_voters(100)
    winner = voting_system.ballot_view()

    print("\nWinner:", winner)
