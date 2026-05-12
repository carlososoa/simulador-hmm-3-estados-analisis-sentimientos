import numpy as np

STATE_NAMES = ["Positivo", "Neutral", "Negativo"]
STATE_EMOJIS = ["(^_^)", "(-_-)", "(T_T)"]
STATE_COLORS = [(76, 175, 80), (255, 193, 7), (244, 67, 54)]

OBS_NAMES = ["palabra positiva", "palabra neutra", "palabra negativa"]


class SimulationResult:
    def __init__(self):
        self.states = []
        self.observations = []
        self.tweets = []
        self.vectors = []
        self.n = 0


class HMM:
    def __init__(self):
        self.n_states = 3
        self.n_obs = 3

        self.A = np.array([
            [0.6, 0.3, 0.1],
            [0.2, 0.6, 0.2],
            [0.1, 0.3, 0.6]
        ])

        self.B = np.array([
            [0.7, 0.2, 0.1],
            [0.2, 0.6, 0.2],
            [0.1, 0.2, 0.7]
        ])

        self.pi = np.array([0.2, 0.6, 0.2])

    def set_matrices(self, A, B, pi):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.pi = np.array(pi, dtype=float)

    def generate_sequence(self, n, tweet_generator):
        result = SimulationResult()
        result.n = n

        state = np.random.choice(self.n_states, p=self.pi)
        obs = np.random.choice(self.n_obs, p=self.B[state])

        result.states.append(state)
        result.observations.append(obs)
        result.tweets.append(tweet_generator(obs))
        result.vectors.append(self.pi.copy())

        for i in range(1, n):
            state = np.random.choice(self.n_states, p=self.A[state])
            obs = np.random.choice(self.n_obs, p=self.B[state])

            result.states.append(state)
            result.observations.append(obs)
            result.tweets.append(tweet_generator(obs))

            dist = result.vectors[-1] @ self.A
            result.vectors.append(dist.copy())

        return result
