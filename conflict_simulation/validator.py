from parameters import *
import random
import numpy as np

class Validator(object):
    """Abstract class for validators."""

    def __init__(self, network,num_blocks, id):
        self.network = network
        network.nodes.append(self)


        ########
        self.id = id
        self.num_blocks = num_blocks
        self.received_block = np.zeros(self.num_blocks)
        self.num_votes = np.zeros(self.num_blocks)
        self.wait_start = False
        self.wait_timer=None
        self.voted = False


    # Called every round
    def tick(self, time):
        if self.voted == False:
            self.vote_on_delay()



class VoteValidator(Validator):
    """Add the vote messages + slashing conditions capability"""

    def __init__(self, network, wait_average,num_blocks, id):
        super(VoteValidator, self).__init__(network, num_blocks,id)
        self.wait_average = wait_average


    def find_majority_votes(self):
        arg_max = np.argmax(self.num_votes)
        maximum = self.num_votes[arg_max]
        arg_max = np.array([])
        for i in range(self.num_blocks):
            if self.num_votes[i] >= maximum:
                arg_max = np.append(arg_max,i)
        num_contenders = arg_max.size


        choice_priority = np.random.choice(arg_max,num_contenders,replace=False)
        #print(choice_priority)
        for temp_choice in choice_priority:
            #print(temp_choice)
            #print('debug1')
            #print(self.received_block[int(temp_choice)])
            if self.received_block[int(temp_choice)]==1:
                return temp_choice,True

        return temp_choice,False




    def vote_on_delay(self):
        if self.wait_start==True:
            
            if self.network.time >= self.wait_timer:
                maximal_vote,temp_vote_permission = self.find_majority_votes()
                #print(maximal_vote,temp_vote_permission)
                if(temp_vote_permission==True):
                    self.network.broadcast(self.num_blocks+maximal_vote)
                    self.network.report_vote(self.num_blocks+maximal_vote)
                    self.voted = True

            

        return None
                            

    def on_receive(self, obj):
        #print(self.id,obj)
        if(obj/self.num_blocks<1):
            #print(obj)
            block_num = int(obj%self.num_blocks)
            #IMMEDIATE VOTE SETTING
            #self.network.broadcast(self.num_blocks+block_num)
            #self.network.report_vote(self.num_blocks+block_num)
            #self.voted=True
            #immediate vote setting end
            self.received_block[block_num]= 1
            #print(self.received_block)
            if(self.wait_start==False):
                self.wait_start = True
                randomness = int(random.expovariate(1) * self.wait_average)
                self.wait_timer = self.network.time + 0 + randomness                

        if(obj/self.num_blocks>=1):
            vote_num = int(obj%self.num_blocks)
            self.num_votes[vote_num] +=1
        
