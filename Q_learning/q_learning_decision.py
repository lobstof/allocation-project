import numpy as np
import pandas as pd
import time

np.random.seed(2)  # reproducible


def converter(x,y):
    return x*10 + y

# we will use decimal to represent the state
# ex: (x,y) => 10*x + y 
def generate_state_cases(n_pods_total):
    NAME_STATES = []
    for i in range(n_pods_total + 1):
        # if i equals to 0
        if i == 0:
            temp_state = 0
            NAME_STATES.append(temp_state)

        # if i is odd
        elif (i+2) % 2 == 1:
            mid_value = int(i / 2)
            for j in range(mid_value+1):
                temp_state1 = converter(j,i-j)
                temp_state2 = converter(i-j,j)
                NAME_STATES.append(temp_state1)
                NAME_STATES.append(temp_state2)
        else:
            # i is even
            mid_value = int(i / 2)
            for j in range(mid_value):
                temp_state1 = converter(j,i-j)
                temp_state2 = converter(i-j,j)
                NAME_STATES.append(temp_state1)
                NAME_STATES.append(temp_state2)
            temp_state_last = converter(mid_value,mid_value)
            NAME_STATES.append(temp_state_last)
    return NAME_STATES

N_PODS_TOTAL = 5    # the total pods that we can deploy (the max volume amount)
STATES = generate_state_cases(N_PODS_TOTAL)
N_STATES = len(STATES)

# the actions youtube and netfix
# ya1 = add one pod to youtube 
# na1 = add one pod to netflix 
# yd1 = delete one pod from youtube
# nd1 = delete one pod from netflix 
# y0 = remain unchanged
# n0 = remain unchanged
ACTIONS = ['ya1_na1', 'ya1_nd1', 'ya1_n0', 'yd1_na1', 'yd1_nd1', 'yd1_n0', 'y0_na1', 'y0_nd1', 'y0_n0']
N_ACTIONS = len(ACTIONS)
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 10   # maximum episodes

FRESH_TIME = 0.3    # fresh time for one move // may be we can call this detection interval

def build_q_table(states, actions):
    table = pd.DataFrame(
        np.zeros((len(states), len(actions))),
        columns=actions,
        index=states
    )
    # print(table)
    return table

# todo avoid some actions which leads to negative states or over demands pods
def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:   # act greedy
        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name

def action_interpreter(S,A):
    # action dict
    action_dict = {}
    S_ = S

    A_split = A.split("_")
    sub_action1 = A_split[0]
    sub_action2 = A_split[1] 

    # sub_action1
    if sub_action1 == 'ya1':
        action_dict.update({"youtube" : "add"})
        S_ = S_ + 10
    elif sub_action1 == 'yd1':
        action_dict.update({"youtube" : "delete"})
        S_ = S_ - 10
    else:
        action_dict.update({"youtube" : "still"})
    
    # sub_action2
    if sub_action2 == 'na1':
        action_dict.update({"netflix" : "add"})
        S_ = S_ + 1
    elif sub_action2 == 'nd1':
        action_dict.update({"netflix" : "delete"})
        S_ = S_ - 1
    else:
        action_dict.update({"netflix" : "still"})
    
    return action_dict, S_,


def environment_simulator_feedback(action_dict, S_, S):
    score_list = [0, 40, 65, 85, 93]

    weight_youtube = 0.8
    weight_netflix = 0.2

    score_last = weight_youtube * score_list[int(S/10)] + weight_netflix * score_list[int(S/10)]
    score_now = weight_youtube * score_list[int(S_/10)] + weight_netflix * score_list[int(S_/10)]
    
    R = score_now - score_last
    return R

def get_env_feedback(S, A):
    # This is how agent will interact with the environment
    (action_dict, S_) = action_interpreter(S,A)
    R = environment_simulator_feedback(action_dict, S_, S)
    return S_, R

def update_env(S, episode, step_counter):
    # This is how environment be updated
    pass

def rl():
    # main part of RL loop
    q_table = build_q_table(STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            S = S_  # move to next state

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table

if __name__ == "__main__":
    q_table = rl()
    print(q_table)
            