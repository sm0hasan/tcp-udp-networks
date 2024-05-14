#LAB1
import math
import random
import statistics
import heapq

#set these values depending on the parameters givin in the question
#recall that utilization = (length*rate)/transmission
#usually we are given length, transmission, and utilization, and have to calculate rate
def finiteSimulation(utilizationParameter, KParameter):
    rate = 0
    length = 2000 #bits
    transmission = 1*(10**6) #1 Mbps
    utilization = utilizationParameter
    K = KParameter

    T = 1000 #simulation time in seconds

    rate = (utilization*transmission)/length
    expectedMean = 1/rate

    events = []
    times = []
    packetLengths = []
    departures = []
    numObservers = 0
    numArrivals = 0

    # Initialize the 6 variables, Na, Nd, No, idleCounter, droppedCounter, generatedPackets
    arrivalCounter = 0
    departureCounter = 0
    observerCounter = 0
    idleCounter = 0
    droppedCounter = 0
    generatedPackets = 0

    averageNumInQueue = 0
    proportionIdle = 0

    currentTime = 0

    # Generate a set of random observation times according to a Poisson distribution
    while(currentTime < T):
        U1 = random.uniform(0,1)
        thisRandomVariable = -(1/(rate*5))*math.log(1-U1)
        currentTime += thisRandomVariable
        if(currentTime > T):
            break
        heapq.heappush(events, (currentTime, "Observer"))
        numObservers += 1


    currentTime = 0
    
    # Generate a set of packet arrivals according to a Poisson distribution
    while currentTime < T:
        U2 = random.uniform(0,1)
        thisRandomVariable = -(1/rate)*math.log(1-U2)
        currentTime += thisRandomVariable
        if(currentTime > T):
            break
        heapq.heappush(events, (currentTime, "Arrival"))
        numArrivals += 1
        times.append(thisRandomVariable)

    # Order/sort arrivals and observors within one array

    # Simulation
    listOfNumInQueue = []

    while(len(events) > 0):
        thisEvent = heapq.heappop(events)

        # Arrival event
        if(thisEvent[1] == "Arrival"):
            generatedPackets += 1
            # Check if buffer is full
            if ((arrivalCounter - departureCounter) - 1 >= K):
                droppedCounter += 1
            # Otherwise
            else:
                arrivalCounter += 1
                # Generate length of arriving packet
                U3 = random.uniform(0,1)
                packetLength = -length*math.log(1-U3)
                packetLengths.append(packetLength)

                # Calculate service time
                thisServiceTime = packetLength/transmission
                
                # Calculate departure time
                departureTime = 0
                #currentTime = events[i][1] # the time at which arrival event is created
                currentTime = thisEvent[0]
                
                # If this is the first departure in the simulation
                if(len(departures) == 0):
                    departureTime = currentTime + thisServiceTime
                    departures.append(["Departure", departureTime])
                # Otherwise
                else:
                    previousDepartureTime = departures[-1][1] # get the previous departure event time
                    # If the packet has to wait in queue for the previous packet to transmit
                    if(currentTime < previousDepartureTime): 
                        departureTime = previousDepartureTime + thisServiceTime
                        
                    # If the packet does not have to wait queue to transmit
                    else:
                        departureTime = currentTime + thisServiceTime
                    departures.append(["Departure", departureTime]) #append to departure array
                    
                heapq.heappush(events, (departureTime, "Departure"))
        # Departure event
        elif(thisEvent[1] == "Departure"):
            departureCounter += 1
        
        # Observer event
        elif(thisEvent[1] == "Observer"):
            # Update E[n]
            averageNumInQueue = ((averageNumInQueue*observerCounter) + (arrivalCounter - departureCounter))/(observerCounter + 1)
            # If both counters equate, the server is idle, thus increment the idle counter
            if (arrivalCounter == departureCounter):
                idleCounter += 1
            observerCounter += 1
        
    # Calculate P-idle and P-loss
    proportionIdle = idleCounter/observerCounter
    proportionLost = droppedCounter/generatedPackets

    # Theoretical values for E[n] and P-idle
    #theoNumQueue = (utilization/(1-utilization)) - utilization
    #theoPropIdle = 1 - rate*(length/transmission)
    
    # Print Statements
    print("Number of dropped packets: ", droppedCounter)
    print("Proportion of Lost Packets: ", proportionLost)
    print("Proportion Idle: ", proportionIdle)
    print("Average number of events in queue: ", averageNumInQueue)