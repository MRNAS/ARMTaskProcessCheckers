import seoulai_gym as gym2
# from seoulai_gym.envs.checkers.agents import RandomAgentLight
# from seoulai_gym.envs.checkers.agents import RandomAgentDark
from seoulai_gym.envs.checkers.dynamicprogrammingagents import AgentLight
from seoulai_gym.envs.checkers.dynamicprogrammingagents import AgentDark
from seoulai_gym.envs.checkers.agents import RandomAgentDark
from seoulai_gym.envs.checkers.agents import RandomAgentLight
import time
# import gym

#checkers racing game
# robot operates with 100% DP and human is 50% DP and 50% random
#Created by Manuel Retana
#07/07/2020

#checkers game
def main():
    env = gym2.make("Checkers")

    a1 = AgentLight()
    a2 = AgentDark()
    a3 = RandomAgentDark()
    a4 = RandomAgentLight()

    # agent1 = Agent(alpha=0.000025, beta=0.00025, input_dims=[8], tau=0.001, env=env,
    #               batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2,
    #               chkpt_dir='tmp/ddpg_final1')

    #do you want to activate the human model?
    # if false agent is 100% random. human is 50% DP 50% Random
    humanflag = True

    obs = env.reset()
    current_agent = a1
    # next_agent = a2 
    next_agent = a4



    score1=0
    score2=0
    # x=eval(input("What is the goal x position  coordinate?4"))
    # y=eval(input("What is the goal y position  coordinate?1"))
    # # x1=eval(input("What is the goal x position  coordinate?4"))
    # y2=eval(input("What is the goal y position  coordinate?1"))

    while True:
         #required to for agent's goals in DP
        if current_agent == a1:
            flag = True
            # print("a")
        elif current_agent == a2:
            flag = False
            # print("b")
        
        #dynamic vs random agents
        if current_agent == a1:
            print("dyn")
            from_row, from_col, to_row, to_col = current_agent.act(obs,flag,humanflag)
        elif current_agent == a2:
            print("dyn")
            from_row, from_col, to_row, to_col = current_agent.act(obs,flag,humanflag)
        elif current_agent == a3:
            print("ran")
            from_row, from_col, to_row, to_col = current_agent.act(obs)
        elif current_agent == a4:
            print("ran")
            from_row, from_col, to_row, to_col = current_agent.act(obs)
        else:
            print("error choosing agents")
            
        # print(to_row, to_col)
        obs, rew, done, info = env.step(current_agent, from_row, from_col, to_row, to_col)
        current_agent.consume(obs, rew, done)
        env.render()
        time.sleep(1) #time delay
        
        if current_agent == a1:
            score1 += rew
            print(f"Reward:{rew}, total rewards: {score1} by: {current_agent}")
        elif current_agent == a4:
            score1 += rew
            print(f"Reward:{rew}, total rewards: {score1} by: {current_agent}")
        elif current_agent == a2:
            score2 += rew
            print(f"Reward:{rew}, total rewards: {score2} by: {current_agent}")
        elif current_agent == a3:
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