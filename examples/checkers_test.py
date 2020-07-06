import seoulai_gym as gym
from seoulai_gym.envs.checkers.agents import RandomAgentLight
from seoulai_gym.envs.checkers.agents import RandomAgentDark


def main():
    env = gym.make("Checkers")

    obs = env.reset()
    timer = 0

    while timer < 2000:
        env.render()
        timer+=1

    env.close()


if __name__ == "__main__":
    main()