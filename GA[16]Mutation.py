import csv
from random import shuffle
from pyevolve import G1DList, GSimpleGA, Consts, Initializators, Selectors, Mutators, Crossovers
import matplotlib.pyplot as plt
import numpy


#Number of Parts
NUM_PARTS = 16

#Precedence Matrix
with open('precedence_matrix_16.csv', 'rb') as csvfile:
    precedence_list = []
    for line in csvfile.readlines():
        array = line.strip().encode('utf-8').split(',')
        precedence_list.append(array)

#Directions / Orientations
orientations = ['-z','+x','-z','-z','-z','-z','-z','-z','-z','-z','+y','+y','-y','-y','+x','+x']
#Tool Grippers
tools_grippers = ['A','B','C','C','D','D','D','D','E','E','E','E','E','E','F','F']

def check_precedence_criteria(sequence):
    for i,part in enumerate(sequence):
        to_search = precedence_list[part]
        done_sequence = sequence[0:i]
        to_search_final = [x for j, x in enumerate(to_search) if j not in done_sequence]
        for a in to_search_final:
            if a == '1':
                return False
    return True

def check_precedence_swaps(sequence):
    score = 0
    for i,part in enumerate(sequence):
        to_search = precedence_list[part]
        done_sequence = sequence[0:i]
        to_search_final = [x for j, x in enumerate(to_search) if j not in done_sequence]
        for a in to_search_final:
            if a == '1':
                score += 1
    return score

def fitness_func(chromosome):
    chromosome = list(chromosome)
    if check_precedence_criteria(chromosome):
        return 0.0005*(calc_tool_changes(chromosome) + calc_orientation_changes(chromosome))
    else:
        return check_precedence_swaps(chromosome)*0.01

def calc_orientation_changes(sequence):
    orien_changes = 0
    current_orientation = orientations[sequence[0]]
    for part in sequence[1:]:
        if orientations[part] != current_orientation:
            orien_changes += 1
            current_orientation = orientations[part]
    return orien_changes

def calc_tool_changes(sequence):
    tool_changes = 0
    current_tool = tools_grippers[sequence[0]]
    for part in sequence[1:]:
        if tools_grippers[part] != current_tool:
            tool_changes += 1
            current_tool = tools_grippers[part]
    return tool_changes

def init_pop(genome, **args):
    genome.genomeList = range(0, NUM_PARTS)
    shuffle(genome.genomeList)

genome = G1DList.G1DList(NUM_PARTS)
genome.setParams(rangemin=0, rangemax=NUM_PARTS-1)

genome.initializator.set(init_pop)

# Set mutator function
genome.mutator.set(Mutators.G1DListMutatorSwap)

# Set Crossover function
genome.crossover.set(Crossovers.G1DListCrossoverCutCrossfill)

genome.evaluator.set(fitness_func)

mutation_rate = []
fitness_value = []
for x in numpy.arange(0.002,0.05,0.001):
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(200)
    ga.setPopulationSize(50)
    ga.setCrossoverRate(0.9)
    ga.selector.set(Selectors.GTournamentSelector)
    # Set type of objective/ fitness function: Convergence
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setMutationRate(x)
    ga.evolve()
    best = ga.bestIndividual()
    # print best.score
    if check_precedence_criteria(list(best)) == True:
        print "X: ", x, best.fitness
        mutation_rate.append(x)
        fitness_value.append(best.fitness)

plt.plot(mutation_rate, fitness_value)
plt.xlabel('Mutation rate')
plt.ylabel('Fitness Value')
plt.title('Mutation rate v/s Fitness value')
plt.grid(True)
plt.show()

