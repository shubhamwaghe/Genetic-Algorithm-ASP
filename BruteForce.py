#Assembly sequence planning - Brute Force
import csv
import itertools
import time
start_time = time.time()
with open("opt.txt", "w") as text_file:
    text_file.write("Script started...\n")
#Number of Parts
NUM_PARTS = 4
# NUM_PARTS = 12
# NUM_PARTS = 16

#Precedence Matrix
if NUM_PARTS==4:
    file = 'precedence_matrix.csv'
elif NUM_PARTS==12:
    file = 'precedence_matrix_12.csv'
elif NUM_PARTS==16:
    file = 'precedence_matrix_16.csv'
else:
    print "Error!!"
with open(file, 'rb') as csvfile:
    precedence_list = []
    for line in csvfile.readlines():
        array = line.strip().encode('utf-8').split(',')
        precedence_list.append(array)
# print precedence_list

#Directions / Orientations
if NUM_PARTS==4:
    orientations = ['+z','-z','+z','-z']
elif NUM_PARTS==12:
    orientations = ['-z','-z','-z','-z','-z','+z','-z','+x','-z','-y','-z','-z']
elif NUM_PARTS==16:
    orientations = ['-z','+x','-z','-z','-z','-z','-z','-z','-z','-z','+y','+y','-y','-y','+x','+x']
else:
    print "Error!!"


#Tool Grippers
if NUM_PARTS==4:
    tools_grippers = ['A','B','C','A']
elif NUM_PARTS==12:
    tools_grippers = ['A','A','A','A','A','A','B','C','D','E','F','G']
elif NUM_PARTS==16:
    tools_grippers = ['A','B','C','C','D','D','D','D','E','E','E','E','E','E','F','F']
else:
    print "Error!!"

#Parts Naming
parts = [ i for i in range(0,NUM_PARTS) ]

#OUTPUT
#Probable Sequences
prob_sequences = []

def check_precedence_criteria(sequence):
    for i,part in enumerate(sequence):
        to_search = precedence_list[part]
        done_sequence = sequence[0:i]
        to_search_final = [x for j, x in enumerate(to_search) if j not in done_sequence]
        for a in to_search_final:
            if a == '1':
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



for i in itertools.permutations(parts):
    sequence = list(i)
    # print sequence
    if check_precedence_criteria(sequence) == True:
        prob_sequences.append(sequence)
        print "Sequence: " + str(sequence)
        print "Orientation changes: " + str(calc_orientation_changes(sequence))
        print "Tool gripper changes: " + str(calc_tool_changes(sequence))
        print
    # break

print "Total sequences: " + str(len(prob_sequences))
print "Total Time Taken", str(round(time.time() - start_time, 1))

with open("opt.txt", "a") as text_file:
    for seq in prob_sequences:
        text_file.write("Sequence:  %s\n" % str(seq))
        text_file.write("Orientation changes:   %s\n" % str(calc_orientation_changes(seq)))
        text_file.write("Tool gripper changes:  %s\n\n" % str(calc_tool_changes(seq)))
    text_file.write("Total sequences:   %s\n" % str(len(prob_sequences)))
    text_file.write("Total Time Taken:  %s" % str(round(time.time() - start_time, 1)))
