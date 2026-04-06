import random

class LearningEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.knowledge = 0.0
        self.time_spent = 0
        self.energy = 1.0   # 🔋 learner energy (new feature)
        self.streak = 0     # 🔥 consistency tracker
        self.done = False
        return self.get_state()

    def get_state(self):
        return (
            round(self.knowledge, 2),
            self.time_spent,
            round(self.energy, 2)
        )

    def step(self, action):
        reward = 0

        # 🎯 EASY (safe, low energy use)
        if action == "easy":
            gain = random.uniform(0.08, 0.12)
            self.knowledge += gain
            self.time_spent += 1
            self.energy -= 0.05
            self.streak += 1
            reward = gain

        # 🎯 MEDIUM (balanced)
        elif action == "medium":
            gain = random.uniform(0.15, 0.25)
            self.knowledge += gain
            self.time_spent += 2
            self.energy -= 0.1
            self.streak += 1
            reward = gain - 0.05

        # 🎯 HARD (risky + energy heavy)
        elif action == "hard":
            self.time_spent += 3
            self.energy -= 0.2
            if random.random() > 0.4:
                gain = random.uniform(0.3, 0.5)
                self.knowledge += gain
                self.streak += 1
                reward = gain - 0.1
            else:
                self.streak = 0
                reward = -0.4

        # 🎯 REVISE (boost consistency)
        elif action == "revise":
            gain = random.uniform(0.04, 0.08)
            self.knowledge += gain
            self.time_spent += 1
            self.energy -= 0.03
            self.streak += 2   # revision boosts streak
            reward = gain + 0.05

        # 🎯 SKIP (penalty)
        elif action == "skip":
            self.time_spent += 1
            self.energy -= 0.02
            self.streak = 0
            reward = -0.15

        # 🔥 STREAK BONUS (consistency reward)
        if self.streak >= 3:
            reward += 0.1

        # 🔋 ENERGY PENALTY
        if self.energy <= 0:
            reward -= 0.5
            self.done = True

        # 🎯 CAP VALUES
        if self.knowledge > 1:
            self.knowledge = 1.0
        if self.energy < 0:
            self.energy = 0

        # 🎯 SUCCESS CONDITION
        if self.knowledge >= 1.0:
            self.done = True
            if self.time_spent < 10:
                reward += 0.5  # fast learner bonus

        return self.get_state(), round(reward, 2), self.done