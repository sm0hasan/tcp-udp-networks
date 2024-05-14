# Project 1: M/M/1 and M/M/1/K Queue Simulation

## Introduction

We have decided to use Python for this Lab. Within the zip file attached within our submission we have a Makefile, and several python files. The main ones are the  '**simulation_finite.py**' and '**simulation_infinite_heap.py**'.

## Usage

To run the simulation the user will have to use the below command in the terminal...

    make U=<utilization> K=<queueSize>

'utilization' must be a float, and 'queueSize' must be a positive integer, unless you want to run the infinite queue simulation.
Note that if you wish to run the infinite simulation case, please type in "infinite" (all lowercase) for the 'queueSize'.

For example, if you want to run a simulation with an infinite queue and utilization of 0.5, you would type:

    make U=0.5 K=infinite

If you want to run a simulation with a utilization of 0.5 and a finite queue with K=10, you would type:

    make U=0.5 K=10

## Extras

We also wrote scripts for questions 3 and 6 that could be run by directly referencing their python file

If you want to run question 3, type:

    python3 q3_1.py

If you want to run question 6, type:

    python3 q6.py


