import csv
from random import shuffle
import pants
import math
from pprint import pprint

NUM_PARTS = 12

DISTANCE_TOOL_CHANGE = 5
DISTANCE_ORIENTATION_CHANGE = 5
DISTANCE_SATISFY_PRECEDENCE = 0
DISTANCE_NOT_SATISFY_PRECEDENCE = 500
DISTANCE_INCENTIVE = 0

#Precedence Matrix
precedence_list = []
with open('precedence_matrix_12.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        precedence_list.append(row)

weigh = []
for each_precedence in precedence_list:
    c = each_precedence.count('1')
    weigh.append(c)

#Directions / Orientations
orientations = ['-z','-z','-z','-z','-z','+z','-z','+x','-z','-y','-z','-z']
#Tool Grippers
tools_grippers = ['A','A','A','A','A','A','B','C','D','E','F','G']

# orientations = ['-z','+x','-z','-z','-z','-z','-z','-z','-z','-z','+y','+y','-y','-y','+x','+x']
# tools_grippers = ['A','B','C','C','D','D','D','D','E','E','E','E','E','E','F','F']

nodes = [ x for x in range(NUM_PARTS) ]
nodes.extend(['NODE'])
# shuffle(nodes)
# print (nodes)

def distance(a,b):
    # print (a,b)
    # print (precedence_list[a][b])
    dist = 0
    if (a == 'NODE'):
        # print(a,b, DISTANCE_INCENTIVE)
        return DISTANCE_INCENTIVE
    if (b == 'NODE'):
        # print(a,b, DISTANCE_INCENTIVE)
        return DISTANCE_INCENTIVE
    if (precedence_list[a][b] == '1'):
        dist = dist + DISTANCE_NOT_SATISFY_PRECEDENCE*abs(weigh[a]-weigh[b])
    else:
        dist = dist + DISTANCE_SATISFY_PRECEDENCE
    if (orientations[a] != orientations[b]):
        dist = dist + DISTANCE_ORIENTATION_CHANGE
    if (tools_grippers[a] != tools_grippers[b]):
        dist = dist + DISTANCE_TOOL_CHANGE
    # print (a,b,dist)
    return dist


def check_precedence_criteria(sequence):
    for i,part in enumerate(sequence):
        to_search = precedence_list[part]
        done_sequence = sequence[0:i]
        to_search_final = [x for j, x in enumerate(to_search) if j not in done_sequence]
        for a in to_search_final:
            if (a == '1'):
                return False
    return True

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

# Run Ant Colony Algorithm
'''
:param float alpha: relative importance of pheromone (default=1)
solver = pants.Solver(ant_count=20)
:param float beta: relative importance of distance (default=3)
:param float rho: percent evaporation of pheromone (0..1, default=0.8)
:param float q: total pheromone deposited by each :class:`Ant` after each iteration is complete (>0, default=1)
:param float t0: initial pheromone level along each :class:`Edge` of the :class:`World` (>0, default=0.01)
:param int limit: number of iterations to perform (default=100)
:param float ant_count: how many :class:`Ant`\s will be used (default=10)
:param float elite: multiplier of the pheromone deposited by the elite :class:`Ant` (default=0.5)
'''

world = pants.World(nodes, distance)
# solver = pants.Solver()
solver = pants.Solver(ant_count=20, limit=150, q=3,beta=5)
solution = solver.solve(world)
# print('Distance: ', solution.distance)
# print(solution.tour)    # Nodes visited in order
# print(solution.path)    # Edges taken in order

final_sequence = solution.tour

answer = []
print ("Final ", final_sequence)
if (final_sequence[1] == 'NODE'):
    a = final_sequence[0]
    final_sequence = final_sequence[2:]
    # print (final_sequence)
    for r in range(NUM_PARTS):
        sequence_to_check = final_sequence[0:r] + [ a ] + final_sequence[r:]
        print ([ m+1 for m in sequence_to_check ])
        if (check_precedence_criteria(sequence_to_check) is True):
            answer = sequence_to_check
            # print ("Answer: ", [ m+1 for m in answer])
            break
            
    if (len(answer) != 0 and check_precedence_criteria(answer) == True):
        print ("Final Sequence: " , answer)
        print ("Tool Changes: ", calc_tool_changes(answer))
        print ("Orientation Changes: ", calc_orientation_changes(answer))
else:
    print ("Ant Colony Algorithm - UNSUCCESSFUL!")

