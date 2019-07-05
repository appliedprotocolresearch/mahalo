import numpy as np
import matplotlib.pyplot as plt

N = 1000
wait = np.linspace(101,1000,num=1000)
Et_list = []
avg_latency = 100
l = 1/avg_latency #lambda

for w in wait:
	e = 1/w
	x1 = 2/l
	x2 = e/2/l/(e-l)
	x3 = 2*l*l/e/(2*l-e)/(e+l)
	x4 = 2*l*e*e/(2*l-e)/(l+e)/(l+2*e)/(l+2*e)
	x5 = 2*l*e/(2*l-e)/(2*l+e)/(2*l+e)
	x6 = -1*2*l*l/(e-l)/(e+l)/(e+l)
	x7 = -1*e/2/(2*l-e)/(l+e)
	x8 = -1*2*l*e*e/(2*l-e)/(l+e)/(3*l+e)/(3*l+e)
	x9 = -1*l/2/e/(2*l-e)
	temp = x1+x2+x3+x4+x5+x6+x7+x8+x9
	Et_list.append(temp)

plt.plot(wait,Et_list)
plt.show()
