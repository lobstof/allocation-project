import numpy as np
import pandas as pd
import time
import json


class q_learning_decision_center:

    def converter(self,x,y):
        return x*10 + y

    # we will use decimal to represent the state
    # ex: (x,y) => 10*x + y 
    def generate_state_cases(self,n_pods_total):
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
                    temp_state1 = self.converter(j,i-j)
                    temp_state2 = self.converter(i-j,j)
                    NAME_STATES.append(temp_state1)
                    NAME_STATES.append(temp_state2)
            else:
                # i is even
                mid_value = int(i / 2)
                for j in range(mid_value):
                    temp_state1 = self.converter(j,i-j)
                    temp_state2 = self.converter(i-j,j)
                    NAME_STATES.append(temp_state1)
                    NAME_STATES.append(temp_state2)
                temp_state_last = self.converter(mid_value,mid_value)
                NAME_STATES.append(temp_state_last)
        return NAME_STATES

    def build_q_table(self,states, actions):
        table = pd.DataFrame(
            np.zeros((len(states), len(actions))),
            columns=actions,
            index=states
        )
        table.at[:,'y0_n0'] = -0.005
        # print(table)
        return table

    def __init__(self,N_PODS_TOTAL=4,EPSILON=0.1,ALPHA=0.1,GAMMA=0.9,real_time_state=11):
        np.random.seed(2)  # reproducible

        self.N_PODS_TOTAL = N_PODS_TOTAL    # the total pods that we can deploy (the max volume amount)
        self.STATES = self.generate_state_cases(self.N_PODS_TOTAL)
        self.N_STATES = len(self.STATES)
        self.LARGE_NEGATIVE_NUMBER = -9999
        self.ENV_CHANGE_RECORD = 0
        self.ENV_CHANGE_FREQUENCE = 60

        # default setting
        self.WEIGHT_YOUTUBE = 0.2
        self.WEIGHT_NETFLIX = 0.8

        # the actions youtube and netfix
        # ya1 = add one pod to youtube 
        # na1 = add one pod to netflix 
        # yd1 = delete one pod from youtube
        # nd1 = delete one pod from netflix 
        # y0 = remain unchanged
        # n0 = remain unchanged
        self.ACTIONS = ['ya1_na1', 'ya1_nd1', 'ya1_n0', 'yd1_na1', 'yd1_nd1', 'yd1_n0', 'y0_na1', 'y0_nd1', 'y0_n0']
        self.N_ACTIONS = len(self.ACTIONS)
        self.EPSILON = EPSILON   # greedy police
        self.ALPHA = ALPHA     # learning rate
        self.GAMMA = GAMMA    # discount factor
        self.MAX_EPISODES = 1   # maximum episodes
        self.q_table = self.build_q_table(self.STATES, self.ACTIONS)

        # for training record
        self.step_counter = 0
        self.real_time_state = real_time_state
        self.real_time_score = 0 
        self.action_next = ''
        self.state_next = 0
        self.score_list = []
        self.state_list = []
        

    def action_interpreter(self,S,A,q_table):
        # action dict
        action_dict = {}
        S_ = S

        A_split = A.split("_")
        sub_action1 = A_split[0]
        sub_action2 = A_split[1] 

        # the number of youtube or netflix pod cant be negative
        # sub_action1
        if sub_action1 == 'ya1':
            action_dict.update({"youtube" : "add"})
            S_ = S_ + 10
        elif sub_action1 == 'yd1':
            # we have no more youtube to be deleted
            if(int(S / 10) == 0):
                # update the q_table 
                new_df = pd.DataFrame({A: [self.LARGE_NEGATIVE_NUMBER]}, index=[S])
                q_table.update(new_df)
                return (False, False)
            else:
                action_dict.update({"youtube" : "delete"})
                S_ = S_ - 10
        else:
            action_dict.update({"youtube" : "still"})
        
        # sub_action2
        if sub_action2 == 'na1':
            action_dict.update({"netflix" : "add"})
            S_ = S_ + 1
        elif sub_action2 == 'nd1':
            # we have no more netflix pod to be deleted
            if(int(S % 10) == 0):
                # update the q_table 
                new_df = pd.DataFrame({A: [self.LARGE_NEGATIVE_NUMBER]}, index=[S])
                q_table.update(new_df)
                return (False, False)
            else:
                action_dict.update({"netflix" : "delete"})
                S_ = S_ - 1
        else:
            action_dict.update({"netflix" : "still"})
        
        return action_dict, S_,


    def is_action_allowed(self,state,action,q_table):
        (action_dict, state_next) = self.action_interpreter(state,action,q_table)
        if(action_dict == False):
            # action is baned during the interpretation
            return False
        # else continue -> 
        n_youtube = int(state_next / 10)
        n_netflix = int(state_next % 10)
        # print(n_youru)
        # And we must obey the total pods limitation (as the resourcese are limited)
        if ((n_youtube + n_netflix) > self.N_PODS_TOTAL):
            # update the q_table 
            new_df = pd.DataFrame({action: [self.LARGE_NEGATIVE_NUMBER]}, index=[state])
            q_table.update(new_df)
            return False
        else:
            return True



    # todo avoid some actions which leads to negative states or over demands pods
    def choose_action(self,state, q_table):
        # Q table dynamic maintenance
        # This is how to choose an action
        state_actions = q_table.loc[state, :]
        # act non-greedy
        if (np.random.uniform() > 1 - self.EPSILON):  
            # to filtre the action unalllowed
            for i in range(150):
                action_name = np.random.choice(self.ACTIONS)
                # verify that is this action is allowed
                if(self.is_action_allowed(state, action_name, q_table)):
                    return action_name
                else:
                    continue
        
        else:   # act greedy
            for i in range(150):
                action_names = state_actions[state_actions == state_actions.max()].index
                action_name = np.random.choice(action_names)
                # verify that is this action is allowed
                if(self.is_action_allowed(state, action_name, q_table)):
                    return action_name
                else: 
                    continue
        # error
        return False

    def environment_simulator_feedback(self,action_dict, S_, S, score_last):
        score_list = [0, 40, 65, 85, 93]

        # score_last = self.WEIGHT_YOUTUBE * score_list[int(S/10)] + self.WEIGHT_NETFLIX * score_list[int(S%10)]
        score_now = self.WEIGHT_YOUTUBE * score_list[int(S_/10)] + self.WEIGHT_NETFLIX * score_list[int(S_%10)]
        
        R = score_now - score_last

        self.ENV_CHANGE_RECORD +=  1
        if ((self.ENV_CHANGE_RECORD % self.ENV_CHANGE_FREQUENCE) == 0):
            # self.WEIGHT_YOUTUBE = np.random.uniform()
            self.WEIGHT_YOUTUBE = 0.8
            self.WEIGHT_NETFLIX = 1 - self.WEIGHT_YOUTUBE
            print("ENV changed ......")
        return R

    def get_env_feedback(self,S, A, q_table,score_last):
        # This is how agent will interact with the environment
        (action_dict, S_) = self.action_interpreter(S,A,q_table)
        R = self.environment_simulator_feedback(action_dict, S_, S, score_last)
        return S_, R


    def rl(self):
        # main part of RL loop
        print(self.WEIGHT_YOUTUBE)
        print(self.WEIGHT_NETFLIX)
        for episode in range(self.MAX_EPISODES):
            print('episode start = ' + str(episode))
            step_counter = 0
            S = 0
            score_real_time = 0 
            # while (score_real_time < 73):
            while (step_counter < 119):
                print('state start: ' + str(S))
                A = self.choose_action(S, self.q_table)
                S_, R = self.get_env_feedback(S, A,self.q_table,score_real_time)  # take action & get next state and reward
                score_real_time = score_real_time + R
                q_predict = self.q_table.loc[S, A]
                # 
                q_target = R + self.GAMMA * self.q_table.loc[S_, :].max()
                self.q_table.loc[S, A] += self.ALPHA * (q_target - q_predict)  # update
                S = S_  # move to next state
                step_counter += 1
                print('action taken' + str(A))
                print('state now: ' + str(S))
                print('score real time = ' + str(score_real_time))

            # conclude the decision
            print('episode = ' + str(episode))
            print('state end = ' + str(S))
            print('score end = ' + str(score_real_time))
            print(self.q_table)
            print(self.WEIGHT_YOUTUBE)
            print(self.WEIGHT_NETFLIX)

    def rl_by_step(self,next_step_score):

        # update score list
        self.score_list.append(next_step_score)
        A = self.action_next
        next_step_state = self.state_next
        R = next_step_score - self.real_time_score

        self.real_time_score = next_step_score
        q_predict = self.q_table.loc[self.real_time_state, A]
        # 
        q_target = R + self.GAMMA * self.q_table.loc[next_step_state, :].max()
        self.q_table.loc[self.real_time_state, A] += self.ALPHA * (q_target - q_predict)  # update

        self.real_time_state = next_step_state  # move to next state
        # update the state list
        self.state_list.append(self.real_time_state)
        print('state after: ' + str(self.real_time_state))
        self.step_counter += 1
    
    def action_generate(self):
        A = self.choose_action(self.real_time_state, self.q_table)
        self.action_next = A
        
        (action_dict,S_) = self.action_interpreter(self.real_time_state,self.action_next,self.q_table)
        print("*********")
        print("action generated:")
        print(action_dict)
        print("*********")
        self.state_next = S_
        return action_dict

    def data_record(self):
        
        data_list1 = self.state_list
        data_list2 = self.score_list
        dict_state_score = {}

        for i in range(min(len(data_list1),len(data_list2))):
            dict_state_score.update({data_list1[i] : data_list2[i]})

        file = open('state_score.json', 'w')
        json_data = json.dumps(dict_state_score)
        file.write(json_data)
        file.close()

if __name__ == "__main__":
    q_learning_decision_center_instance = q_learning_decision_center()
    # print(q_learning_decision_center_instance.q_table)
    q_learning_decision_center_instance.rl()

    # list_s = [-12,15,77,-22,-44,55,11,42,-12,-22]
    # for i in range(10):
    #     print("----------------------------")
    #     print("state_now :")
    #     print(q_learning_decision_center_instance.real_time_state)

    #     decision_dict = q_learning_decision_center_instance.action_generate()
    #     print("action taken:")
    #     print(decision_dict)
    #     q_learning_decision_center_instance.rl_by_step(list_s[i])
    #     print("state after :")
    #     print(q_learning_decision_center_instance.real_time_state)
    #     print("----------------------------")







