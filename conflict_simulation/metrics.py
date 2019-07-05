#!/usr/bin/python3
import os
import numpy as np

from parameters import *
from utils import exponential_latency
from network import Network
from validator import VoteValidator

from tqdm import tqdm



def print_metrics_latency(num_tries,latencies,wait_averages,n_validators, num_blocks,validator_set):
    for latency in latencies:

        wait_average_list = []
        delay_list = []
        P_consensus_list = []

        concensus_to_non_concensus_list = []
        time_given_concensus_list = []
        time_given_non_concensus_list = []
        num_justified = np.zeros(num_blocks)

        for wait_average in wait_averages:
        
            sum_justification = np.zeros(num_blocks)
            sum_delay = 0
            time_given_concensus = []
            time_given_non_concensus = []
            concensus_events = 0
            non_concensus_events = 0


            for i in tqdm(range(num_tries)):
                concensus_bool = False
                non_concensus_delay=0
                #while concensus_bool == False:
                    #print(concensus_bool)
                #print('Average network Latency:{}'.format(latency))
                network = Network(exponential_latency(latency),n_validators,num_blocks)
                #print('Debug2')
                validators = [VoteValidator(network,wait_average,num_blocks, i) for i in validator_set]

                R1 = np.random.randint(n_validators)
                R2 = np.random.randint(n_validators)


                for t in range(BLOCK_PROPOSAL_TIME * EPOCH_SIZE * NUM_EPOCH):
                    if network.next_tick_permission==True:
                        if(t==0):
                            validators[R1].network.broadcast(0)
                            validators[R2].network.broadcast(1)
                            validators[R1].network.broadcast(num_blocks+0)
                            validators[R1].network.report_vote(num_blocks+0)
                            validators[R1].voted= True
                            validators[R2].network.broadcast(num_blocks+1)
                            validators[R2].network.report_vote(num_blocks+1)
                            validators[R2].voted= True
                        network.tick()
                        if network.next_tick_permission==False:
                            non_concensus_delay += t
                            time_given_non_concensus.append(t)
                            non_concensus_events+=1
                            break

                    if(np.sum(network.justified)>=1):
                        concensus_bool = True
                        #break


                    if(network.all_votes_cast==True):
                        break

                '''
                for t in range(BLOCK_PROPOSAL_TIME * EPOCH_SIZE * NUM_EPOCH):
                    if network.next_tick_permission==True:
                        if(t==0):
                            for blk in range(num_blocks):
                                validators[R1].network.broadcast(int(blk))
                                if(int(blk)==0):
                                    #validators[R1].network.broadcast(num_blocks+int(blk))
                                    #validators[R1].network.report_vote(num_blocks+int(blk))
                                    #validators[R1].voted=True
                                    pass
                                #print(int(blk))

                        network.tick()
                        if network.next_tick_permission==False:
                            non_concensus_delay += t
                            time_given_non_concensus.append(t)
                            non_concensus_events+=1
                            break

                    if(np.sum(network.justified)>=1):
                        concensus_bool = True
                        #break


                    if(network.all_votes_cast==True):
                        break
                '''
                    #print('Network_ticks')
                    # if t % (BLOCK_PROPOSAL_TIME * EPOCH_SIZE) == 0:
                    #     filename = os.path.join(LOG_DIR, 'plot_{:03d}.png'.format(t))
                    #     plot_node_blockchains(validators, filename)


                #print(network.all_votes_cast)

                for val in validators:
                    pass    


                sum_justification += network.justified

                if(np.sum(network.justified)>=1):
                    for blk in range(num_blocks):
                        num_justified[int(blk)] += network.justified[int(blk)]
                    concensus_events+=1
                    sum_delay +=  non_concensus_delay + network.justification_delay
                    time_given_concensus.append(network.justification_delay)

            print(num_justified)        
            P_consensus_list.append((np.sum(sum_justification))/num_tries )
            delay_list.append(sum_delay/(np.sum(sum_justification)))
            wait_average_list.append(wait_average/latency)
            time_given_concensus_list.append(sum(time_given_concensus)/float(len(time_given_concensus)))
            #time_given_non_concensus_list.append(sum(time_given_non_concensus)/float(len(time_given_non_concensus)))
            #concensus_to_non_concensus_list.append(concensus_events/non_concensus_events)

            print('Concensous events:{}'.format(concensus_events))
            print('non_concensus_events:{}'.format(non_concensus_events))

            print(num_justified)
            print('=== Statistics ===')
            print('Latency: {}'
                    .format(latency))
            print('wait_average: {}'.format(wait_average))
            print('P(concensus): {}'.format((np.sum(sum_justification))/num_tries ))
            print('Delay :{}'.format(sum_delay/(np.sum(sum_justification))))
            #print('sum_justification:{}'.format(sum_justification))
            

        print('P(concensus): {}'.format(P_consensus_list))
        print('Concensus Delay: {}'.format(delay_list))
        print('wait_average/latency: {}'.format(wait_average_list))
        #print('concensus_to_non_concensus_list:{}'.format(concensus_to_non_concensus_list))
        print('time_given_concensus_list:{}'.format(time_given_concensus_list))
        #print('time_given_non_concensus_list:{}'.format(time_given_non_concensus_list))

        f1.write('SUPER_MAJORITY: {} \n'.format(SUPER_MAJORITY))
        f1.write('n_validators: {}\n'.format(n_validators))
        f1.write('P(concensus): {}\n'.format(P_consensus_list))
        f1.write('Concensus Delay: {}\n'.format(delay_list))
        f1.write('wait_average/latency: {}\n'.format(wait_average_list))
        #f1.write('concensus_to_non_concensus_list:{}\n'.format(concensus_to_non_concensus_list))
        f1.write('time_given_concensus_list:{}\n'.format(time_given_concensus_list))
        #f1.write('time_given_non_concensus_list:{}\n'.format(time_given_non_concensus_list))
        f1.write('\n')


if __name__ == '__main__':
    # LOG_DIR = 'metrics'
    # if not os.path.exists(LOG_DIR):
        # os.makedirs(LOG_DIR)

    # Uncomment to have fractions of disconnected nodes
    # fractions = np.arange(0.0, 0.4, 0.05)
    # fractions = [0.31, 0.32, 0.33]
    fractions = [0.0]

    f1 = open('final_conflict_data/conflict_log_1.txt', 'a+')
    f1.write('No information cascade setup\n')
    #f1.write('Written')



    N_VALIDATORS = [100] #[500,1000]      
    num_blocks = 2
    print('``````````````````')
    print("""running test
            NUM_BLOCKS: {}""".
            format(num_blocks))
    print('``````````````````')

    for n_validators in N_VALIDATORS:
        print('num_validators:{}'.format(n_validators))
        for fraction_disconnected in fractions:
            num_validators = int((1.0 - fraction_disconnected) * n_validators)
            validator_ids = list(range(0, n_validators * 2))
            validator_set = validator_ids[:num_validators]
            
            #print("height of connected of nodes: {}".format(len(validator_set)))

            # Uncomment to have different latencies
            #latencies = [i for i in range(10, 300, 20)] + [500, 750, 1000]
            latencies = [100]
            wait_fraction = [1]
            wait_averages = [i*latencies[0] for i in wait_fraction]
            #print(wait_averages)

            num_tries = 1000

            print_metrics_latency(num_tries,latencies,wait_averages,n_validators,num_blocks, validator_set)

    f1.close()