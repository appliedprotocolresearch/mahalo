import numpy as np
import math
import random
import matplotlib.pyplot as plt

N = 10000
avg_latency = 100
#wait_fractions = [0,10,25,50,100,200,500,1000]
wait_fractions = np.linspace(0,1000,num=1000)
P_concensus_list = []

for wf in wait_fractions:
	concensus_count = 0
	for i in range(N):
		L1 = random.expovariate(1) * avg_latency/2
		L2 = random.expovariate(1) * wf
		L = L1 + L2
		R1 = random.expovariate(1) * avg_latency/2
		R2 = random.expovariate(1) * wf
		R3 = random.expovariate(1) * avg_latency
		R = R1 + R2 + R3
		if L>R:
			concensus_count +=1
	P_concensus = concensus_count/N
	P_concensus_list.append(P_concensus)

#print('wait_fractions:{}'.format(wait_fractions))
#print('P_concensus_list:{}'.format(P_concensus_list))

plt.plot(wait_fractions,P_concensus_list)
plt.show()