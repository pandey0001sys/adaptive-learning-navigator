import random

class Agent:
    def __init__(self):
        # Available actions
        self.actions = ["easy", "medium", "hard", "revise", "skip"]

    def choose_action(self, state):
        """
        Smart action selection based on current knowledge level
        """
        knowledge, time_spent = state

        # 🎯 Strategy based decisions
        if knowledge < 0.3:
            # Early stage → easier learning
            return random.choice(["easy", "medium"])

        elif knowledge < 0.7:
            # Mid stage → balanced learning
            return random.choice(["medium", "hard", "revise"])

        else:
            # Final stage → optimize & finish
            return random.choice(["hard", "revise", "skip"])