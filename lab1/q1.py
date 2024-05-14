import math
import random
import statistics

variables = []
sum = 0

for i in range(0, 1000):
    U = random.uniform(0,1)
    thisRandomVariable = -(1/75)*math.log(1-U)
    variables.append(thisRandomVariable)

mean = statistics.mean(variables)

deviations = []
for x in variables:
    deviations.append((x-mean)**2)

variance = statistics.mean(deviations)

print("Mean: ", mean)
print("Variance: ", variance)

