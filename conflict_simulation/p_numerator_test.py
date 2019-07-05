import numpy as np
import random

num_tries = 10000
count_positive = 0


for i in range(num_tries):
	l = np.random.uniform(0,100)
	e = np.random.uniform(0,100)
	#print(l**2)
	expr = -192*(l**9) + 400*(l**8)*(e**1) -596*(l**7)*(e**2) +608*(l**6)*(e**3) -455*(l**5)*(e**4) +180*(l**4)*(e**5) -3*(l**3)*(e**6) -12*(l**2)*(e**7) +0*(l**1)*(e**8)
	count_positive += (expr>0)

print(count_positive)


2 + 1/2/(1-x) + 2*(x**3)/(2*x-1)/(1+x) + 2*x**2/(2*x-1)/(1+x)/(x+2)**2 + 2*x**2/(2*x-1)/(2*x+1)**2 - 2*x**3/(1-x)/(1+x)**2 - x/2/(2*x-1)/(1+x) - 2*x**2/(2*x-1)/(1+x)/(3*x+1)**2 - x**2/2/(2*x-1)

(54 x^9 + 657 x^8 + 3030 x^7 + 7273 x^6 + 10186 x^5 + 8789 x^4 + 4710 x^3 + 1517 x^2 + 268 x + 20)\/(2 (x + 1)^2 (x + 2)^2 (2 x + 1)^2 (3 x + 1)^2)
