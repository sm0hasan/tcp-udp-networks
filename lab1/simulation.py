#LAB1

import math
import random

#set these values depending on the parameters givin in the question
#recall that utilization = (length*rate)/transmission
#usually we are given length, transmission, and utilization, and have to calculate rate

def infiniteSimulation(utilizationParameter):
    rate = 0
    length = 2000 #bits
    transmission = 1*(10**6) #1 Mbps
    utilization = utilizationParameter

    T = 1000 #simulation time in seconds

    rate = (utilization*transmission)/length

    events = []
    departures = []

    # Initialize the 4 variables, Na, Nd, No, proportionIdle
    arrivalCounter = 0
    departureCounter = 0
    observerCounter = 0

    averageNumInQueue = 0
    proportionIdle = 0

    currentTime = 0

    # Generate a set of packet arrivals according to a Poisson distribution
    while currentTime < T:
        U = random.uniform(0,1)
        thisRandomVariable = -(1/rate)*math.log(1-U)
        currentTime += thisRandomVariable
        if(currentTime > T):
            break
        # Generate length of arriving packet
        U2 = random.uniform(0,1)
        packetLength = -length*math.log(1-U2)
        events.append(["Arrival", packetLength, currentTime])

        # Calculate service time
        thisServiceTime = packetLength/transmission
        departureTime = 0

        # If this is the first departure in the simulation
        if(len(departures) == 0):
            departureTime = currentTime + thisServiceTime
            departures.append(["Departure", 0, departureTime])
        # Otherwise
        else:
            previousDepartureTime = departures[-1][2] #get the previous departure event time
            # If the packet has to wait in queue for the previous packet to transmit
            if(currentTime < previousDepartureTime): 
                departureTime = previousDepartureTime + thisServiceTime
            # If the packet does not have to wait queue to transmit
            else:
                departureTime = currentTime + thisServiceTime
            departures.append(["Departure", 0, departureTime]) #append to departure array

    
    currentTime = 0
    
    # Generate a set of random observation times according to a Poisson distribution
    while(currentTime < T):
        U = random.uniform(0,1)
        thisRandomVariable = -(1/(rate*5))*math.log(1-U)
        currentTime += thisRandomVariable
        if(currentTime > T):
            break

        events.append(["Observer", 0, currentTime])

    # Create a new array by appending both the events and departure arrays together, then sort them
    finalEvents = events + departures
    finalEvents = sorted(finalEvents, key=lambda x: x[2])

    idleCounter = 0

    for event in finalEvents:
        # Arrival event
        if(event[0] == "Arrival"):
            arrivalCounter += 1
        # Departure event
        elif(event[0] == "Departure"):
            departureCounter += 1
        # Observer event
        else:
            # Update E[n]
            averageNumInQueue = ((averageNumInQueue*observerCounter) + (arrivalCounter - departureCounter))/(observerCounter + 1)
            # If both counters equate, the server is idle, thus increment the idle counter
            if(arrivalCounter == departureCounter):
                idleCounter += 1
            # Update P-idle
            proportionIdle = idleCounter/(observerCounter + 1)
            observerCounter += 1     

    # Theoretical values for E[n] and P-idle
    theoNumQueue = (utilization/(1-utilization)) - utilization
    theoPropIdle = 1 - rate*(length/transmission)

    # Print Statements
    print("Theoretical proportion Idle: ", theoPropIdle)
    print("Proportion Idle: ", proportionIdle)
    print("Theoretical num in queue with server: ", theoNumQueue + utilization)
    print("Average number of events in queue: ", averageNumInQueue)


