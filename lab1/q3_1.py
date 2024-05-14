import simulation

utilizations = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

for x in utilizations:
    print("Utilization: ", x)
    simulation.infiniteSimulation(x)
    print()