import seoulai_gym as gym2
# from seoulai_gym.envs.checkers.agents import RandomAgentLight
# from seoulai_gym.envs.checkers.agents import RandomAgentDark
from seoulai_gym.envs.checkers.dynamicprogrammingagents import RandomAgentLight
from seoulai_gym.envs.checkers.dynamicprogrammingagents import RandomAgentDark
import time
# import gym

#checkers racing game
#Created by Manuel Retana
#07/07/2020

#checkers game
def main():
    env = gym2.make("Checkers")

    a1 = RandomAgentLight()
    # a2 = RandomAgentDark()

    # agent1 = Agent(alpha=0.000025, beta=0.00025, input_dims=[8], tau=0.001, env=env,
    #               batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2,
    #               chkpt_dir='tmp/ddpg_final1')

    obs = env.reset()
    current_agent = a1
    # next_agent = a2 
    next_agent = a1
    score1=0
    score2=0
    # x=eval(input("What is the goal x position  coordinate?4"))
    # y=eval(input("What is the goal y position  coordinate?1"))
    # # x1=eval(input("What is the goal x position  coordinate?4"))
    # y2=eval(input("What is the goal y position  coordinate?1"))

    while True:
        from_row, from_col, to_row, to_col = current_agent.act(obs)
        print(to_row, to_col)
        obs, rew, done, info = env.step(current_agent, from_row, from_col, to_row, to_col)
        current_agent.consume(obs, rew, done)
        env.render()
        time.sleep(1) #time delay
        
        if current_agent == RandomAgentLight():
            score1 += rew
            print(f"Reward:{rew}, total rewards: {score1} by: {current_agent}")
        else:
            score2 += rew
            print(f"Reward:{rew}, total rewards: {score2} by: {current_agent}")
        
        if done:
            print(f"Game over! {current_agent} agent wins.")
            obs = env.reset()

        # switch agents
        temporary_agent = current_agent
        current_agent = next_agent
        next_agent = temporary_agent


    env.close()


if __name__ == "__main__":
    main()