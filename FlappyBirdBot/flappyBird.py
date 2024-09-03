import numpy as np
import random
from ple import PLE
from ple.games.flappybird import FlappyBird

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.random.uniform(low=-1, high=1, size=(state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        state = tuple(map(int, state))  # Convert state to tuple of integers
        next_state = tuple(map(int, next_state))  # Convert next_state to tuple of integers
        
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += self.learning_rate * (td_target - self.q_table[state][action])

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def get_state(game_state):
    return (
        game_state["player_y"],
        game_state["next_pipe_dist_to_player"],
        game_state["next_pipe_top_y"],
        game_state["next_pipe_bottom_y"]
    )

def train_agent(agent, env, actions, episodes=10000):
    for e in range(episodes):
        env.reset_game()
        state = get_state(env.getGameState())
        
        total_reward = 0
        while not env.game_over():
            action_idx = agent.get_action(state)
            action = actions[action_idx]
            
            reward = env.act(action)
            
            next_state = get_state(env.getGameState())
            
            agent.update_q_table(state, action_idx, reward, next_state)
            
            state = next_state
            total_reward += reward
            
        print(f"Episode: {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")

if __name__ == "__main__":
    # Initialize the game
    game = FlappyBird()
    env = PLE(game, fps=30, display_screen=True)

    # Define actions
    actions = env.getActionSet()

    # Reset environment
    env.init()

    # Initialize agent
    state_size = 4  # player_y, next_pipe_dist_to_player, next_pipe_top_y, next_pipe_bottom_y
    action_size = len(actions)
    agent = QLearningAgent(state_size, action_size)

    # Train agent
    train_agent(agent, env, actions)
