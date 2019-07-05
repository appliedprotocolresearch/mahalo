from parameters import *
import numpy as np

class Network(object):
	"""Networking layer controlling the delivery of messages between nodes.

	self.msg_arrivals is a table where the keys are the time of arrival of
	messages and the values is a list of the objects received at that time
	"""	
	def __init__(self, latency_fn,n_validators,num_blocks):
		self.nodes = []
		self.time = 0
		self.msg_arrivals = {}
		self.latency_fn = latency_fn
		self.num_blocks = num_blocks
		self.num_votes = np.zeros(self.num_blocks)
		self.justified = np.zeros(self.num_blocks)
		self.justification_delay = None
		self.all_votes_cast = False
		self.next_tick_permission = True
		self.n_validators = n_validators
		'''
		self.log_delay_list = []
		self.log_vote_report_time = []
		self.log_first_block_time = []
		self.log_block_A_arrival_time = []
		self.log_block_B_arrival_time = []
		#print('Network_initialized')
		'''

	def broadcast(self, msg):

		for node in self.nodes:
            # Create a different delay for every receiving node i
            # Delays need to be at least 1
			delay = self.latency_fn()
			#self.log_delay_list.append(delay)
			assert delay >= 1, "delay is 0, which will lose some messages !"
			if self.time + delay not in self.msg_arrivals:
				self.msg_arrivals[self.time + delay] = []
			self.msg_arrivals[self.time + delay].append((node.id, msg))


	def tick(self):

		if self.time in self.msg_arrivals:
			for node_index, msg in self.msg_arrivals[self.time]:
				self.nodes[node_index].on_receive(msg)
			del self.msg_arrivals[self.time]
		for n in self.nodes:
			n.tick(self.time)
		self.time += 1

		if(np.sum(self.num_votes) >= self.n_validators):
			self.all_votes_cast = True
			#print('All votes cast time:{}'.format(self.time))

		for i in range(self.num_blocks):
			temp1 = self.num_votes[i]
			temp2 = np.sum(self.num_votes) - self.num_votes[i]
			if((temp1>self.n_validators*(1-SUPER_MAJORITY)) and (temp2>self.n_validators*(1-SUPER_MAJORITY))):
				self.next_tick_permission = False


   

    
	def report_vote(self,vote):
		#self.log_vote_report_time.append(self.time)
		vote_num = int(vote%self.num_blocks)
		#print('vote_num')
		#print(vote_num)
		self.num_votes[vote_num] += 1

		if(self.num_votes[vote_num]>self.n_validators*SUPER_MAJORITY):
			if(self.justified[vote_num]==0):
				self.justification_delay = self.time
				self.justified[vote_num] = 1
