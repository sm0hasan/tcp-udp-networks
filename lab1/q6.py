import simulation_finite_heap

utilizations = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]

print("10 PACKETS *******************************************")
for utilization in utilizations:
    print("Utilization: ", utilization)
    print()
    simulation_finite_heap.finiteSimulation(utilization, 10)
    print()

print("25 PACKETS *******************************************")
for utilization in utilizations:
    print("Utilization: ", utilization)
    print()
    simulation_finite_heap.finiteSimulation(utilization, 25)
    print()

print("50 PACKETS *******************************************")
for utilization in utilizations:
    print("Utilization: ", utilization)
    print()
    simulation_finite_heap.finiteSimulation(utilization, 50)
    print()

