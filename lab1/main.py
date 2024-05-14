import simulation
import simulation_finite_heap
import sys

utilization = float(sys.argv[1])
K = sys.argv[2]

print("Arguments passed: ", utilization, " ", K)

if (K == "infinite"):
    simulation.infiniteSimulation(utilization)
else:
    simulation_finite_heap.finiteSimulation(utilization, int(K))
#queueType = str(sys.argv[2])

