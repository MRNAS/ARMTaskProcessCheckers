# Set-up an environment for the Moon Lander Game
import gym

env=gym.make('LunarLanderContinuous-v2')

agent = Agent(alpha=0.000025, beta=0.00025, input_dims=[8], tau=0.001, env=env,
                  batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2,
                  chkpt_dir='tmp/ddpg_final1')

for i in range(3000):
    obs = env.reset()
    done = False
    score = 0
    while not done:
        act = agent.choose_action(obs)
        new_state, reward, done, info = env.step(act)
        agent.remember(obs, act, reward, new_state, int(done))
        agent.learn()
        score += reward
        obs = new_state
        env.render()
    score_history.append(score)
    print('episode ', i, 'score %.2f' % score, 'trailing 100 games avg %.3f' % np.mean(score_history[-100:]))