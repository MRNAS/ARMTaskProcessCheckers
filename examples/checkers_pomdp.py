import seoulai_gym as gym2
import random
import time
from seoulai_gym.envs.checkers.dynamicprogrammingagents import AgentLight
from seoulai_gym.envs.checkers.dynamicprogrammingagents import AgentDark
from seoulai_gym.envs.checkers.agents import RandomAgentDark
from seoulai_gym.envs.checkers.agents import RandomAgentLight
from seoulai_gym.envs.checkers.humanagents import HumanLight
from seoulai_gym.envs.checkers.humanagents import HumanDark
import seoulai_gym.envs.checkers.board
from seoulai_gym.envs.checkers.rules import Rules
#for learning
# import gym

#checkers racing game with n players
#robot operates with 100% DP and human is 50% DP and 50% random
#Created by Manuel Retana
#07/30/2020

#checkers game
def main():
    env = gym2.make("Checkers")

    #robot agents
    a1 = AgentLight() 
    # a2 = AgentDark()

    #human agents
    a3 = HumanLight()
    # a4 = HumanDark()

    #random agents
    a5 = RandomAgentLight()
    # a6 = RandomAgentDark()

    obs = env.reset()

    #classify board
    whiteplayers = 0
    blackplayers = 0
    emptycells = 0
    size = len(obs)
    for i in range(size):
        for j in range(size):
                if obs[i][j] == None:
                    emptycells += 1
                elif obs[i][j].ptype == 1:
                    whiteplayers += 1
                elif obs[i][j].ptype == 2:
                    blackplayers += 1
                
    print("white players:",whiteplayers)
    print("black players:",blackplayers)
    print("amount of empty cells in 8x8 board:",emptycells)

    #activates DP robots and Humans
     #do you want to activate the human model?
    # if false agent is 100% random. human is 50% DP 50% Random
    robotflag = True 
    humanflag = True

    if robotflag == True:
        print("Robot DP Activated")
    else: 
        print("Robot DP Deactivated")

    if humanflag == True:
        print("Human Model Activated")
    else:
        print("Human Model Deactivated")

    robots = 1
    humans = 1
    nplayers = 64 - emptycells # change if board size changes
    print("nplayers in the game:", nplayers)
    
    #creates and requests list of objectives
    glist = []
    for i in range(0,nplayers):
        goal=(input("type (x,y) 6365 objective in xy format for each goal and press enter:"))
        glist.append(goal)
    glist=tuple(glist)
    print(glist)


    # current_agent = a1 #robot agent
    # next_agent = a2

    # next_agent = a4 #just moving a single piece
        # agent1 = Agent(alpha=0.000025, beta=0.00025, input_dims=[8], tau=0.001, env=env,
    #               batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2,
    #               chkpt_dir='tmp/ddpg_final1')

    #end of game condition
    Whitedone = False
    Blackdone = False

    # to do: create the number of scores to the number of nplayers
    score1=0
    score2=0
    counter = 0
    
    #begin with robot first and human second
    current_agent = a1
    next_agent = a3

    while True:

        #  #required to for agent's goals in DP
        # if current_agent == a1:
        #     flag = True
        #     # print("a")
        # elif current_agent == a3:
        #     flag = False
        #     # print("b")
        # elif current_agent == a5:
        #     flag = False
        #     # print("b")
        
        from_row, from_col, to_row, to_col = current_agent.act(obs,glist)
        obs, rew, done, info = env.step(current_agent, from_row, from_col, to_row, to_col)
        current_agent.consume(obs, rew, done)

        env.render()
        time.sleep(1) #time delay
        counter += 1
        
        if current_agent == a1:
            score1 += rew
            print(f"Reward:{rew}, total rewards: {score1} by: {current_agent}")
        # elif current_agent == a4:
        #     score1 += rew
        #     print(f"Reward:{rew}, total rewards: {score1} by: {current_agent}")
        # elif current_agent == a2:
        #     score2 += rew
        #     print(f"Reward:{rew}, total rewards: {score2} by: {current_agent}")
        elif current_agent == a3:
            score2 += rew
            print(f"Reward:{rew}, total rewards: {score2} by: {current_agent}")

        # print(from_row,from_col,"status")
        # stopping conditions for switch if got to goal
        print("objective location:",from_row, from_col,"counter:",counter)
        if from_row == 6 and from_col == 3:
            print("white is done")
            Whitedone = True
        elif from_row == 6 and from_col == 5:
            print("black is done")
            Blackdone = True

        if done:
            print(f"Game over! {current_agent} agent wins.")
            # obs = env.reset()
        elif Whitedone == True and Blackdone == True:
            print(f"Game over! {current_agent} agent wins.")
            # obs = env.reset()
            env.close()

        # switch agents
        #sequence of agents based on inputs
        #alternate between humans and robots
        if robotflag == True and humanflag == True:
            turns = nplayers
            if counter % turns == 0: #human (even turn)
                #select any piece of the board at random
                temporary_agent = current_agent
                current_agent = next_agent
                next_agent = temporary_agent
                if Whitedone == True:
                    print("white is done agents")
                    current_agent = a3
                elif Blackdone ==True:
                    print("black is done agents")
                    current_agent = a1
            else: #robot (odd turn)
                current_agent = a1
                next_agent = a3
        #alternate between humans
        elif robotflag == False and humanflag == True:
            turns = nplayers
            current_agent = 0
            next_agent = 0
        #alternate between random agents
        elif robotflag == False and humanflag == False: 
            temporary_agent = current_agent
            current_agent = next_agent
            next_agent = temporary_agent


    env.close()


if __name__ == "__main__":
    main()