#!/usr/bin/env python
# coding: utf-8

# In[45]:


def generate_randomdist():
# randomly generates a sequence of board states.
    global nQueens
    init_distribution = np.arange(nQueens)
    np.random.shuffle(init_distribution)
    return init_distribution

def initial_Population(population_size = 100):
    global POPULATION

    POPULATION = population_size

    initial_population = [EightQueensPosition() for i in range(population_size)]
    for i in range(population_size):
        initial_population[i].setSequence(generate_randomdist())
        initial_population[i].setFitness(calc_fitness(initial_population[i].sequence))

    return initial_population
    


# In[46]:


def calc_fitness(population = None):
    conflicts = 0;
    row_col_conflicts = abs(len(population) - len(np.unique(population)))
    conflicts += row_col_conflicts

# calculate diagonal clashes
    for i in range(len(population)):
        for j in range(len(population)):
            if ( i != j):
                dx = abs(i-j)
                dy = abs(population[i] - population[j])
                if(dx == dy):
                    conflicts += 1


    return 28 - conflicts


# In[47]:


def crossover(parent1, parent2):
    globals()
    n = len(parent1.sequence)
    c = np.random.randint(n, size=1)
    child = QueenPosition()
    child.sequence = []
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    child.setFitness(calc_fitness(child.sequence))
    return child


def mutate(child):
    if child.survival < MUTATE:
        c = np.random.randint(8)
        child.sequence[c] = np.random.randint(8)
    return child


# In[48]:


def select_Parent():
    globals()
    parent1, parent2 = None, None
# parent is decided by random probability of survival.
# since the fitness of each board position is an integer >0, 
# we need to normaliza the fitness in order to find the solution

    summation_fitness = np.sum([x.fitness for x in population])
    for each in population:
        each.survival = each.fitness/(summation_fitness*1.0)

    while True:
        parent1_random = np.random.rand()
        parent1_rn = [x for x in population if x.survival <= parent1_random]
        try:
            parent1 = parent1_rn[0]
            break
        except:
            pass

    while True:
        parent2_random = np.random.rand()
        parent2_rn = [x for x in population if x.survival <= parent2_random]
        try:
            t = np.random.randint(len(parent2_rn))
            parent2 = parent2_rn[t]
            if parent2 != parent1:
                break
            else:
                print("equal parents")
                continue
        except:
            print("exception")
            continue

    if parent1 is not None and parent2 is not None:
        return parent1, parent2
    else:
        sys.exit(-1)


# In[49]:


def Genetic_Algo(iteration):
    globals()
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = select_Parent()
        child = crossover(parent1, parent2)
        
        if(MUTATE_FLAG):
            child = mutate(child)
        newpopulation.append(child)
    return newpopulation


def stop():
    globals()
    fitnessvals = [pos.fitness for pos in population]
    if STOP_CTR in fitnessvals:
        return True
    if MAX_ITER == iteration:
        return True
    return False


# In[50]:


import numpy as np
import sys
nQueens = 8
STOP_CTR = 28
MUTATE = 0.000001
MUTATE_FLAG = True
MAX_ITER = 100000
POPULATION = None

class EightQueensPosition:
    def __init__(self):
        self.sequence = None
        self.fitness = None
        self.survival = None
    def setSequence(self, val):
        self.sequence = val
    def setFitness(self, fitness):
        self.fitness = fitness
    def setSurvival(self, val):
        self.survival = val
    def getAttr(self):
        return {'sequence':sequence, 'fitness':fitness, 'survival':survival}


# In[54]:


population = initial_Population(1000)

print("POPULATION size : ", population)

iteration = 0;
while not stop():
# keep iteratin till  you find the best position
    population = Genetic_Algo(iteration)
    iteration +=1 

print("Iteration number : ", iteration)
for each in population:
    if each.fitness == 28:
        print("Sequence is {0}".format(each.sequence))

