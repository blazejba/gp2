import sys
import matplotlib.pyplot as plt

name = sys.argv[1]

file = open('../exp/logs/' + name + '.log')

is_1 = []
is_2 = []
mig_1 = []
mig_2 = []

for line in file:
	line = line.split(',')
	print(line)
	if line[1] == '0':
		is_1.append([int(line[0]),int(line[2]),float(line[3])])
		if line[4] == 'True':
			mig_1.append([int(line[0]), float(line[3])])
	else:
		is_2.append([int(line[0]),int(line[2]),float(line[3])])
		if line[4] == 'True':
			mig_2.append([int(line[0]), float(line[3])])

plt.plot([x[0] for x in is_1], [x[1] for x in is_1], label='best fitness, island 1', color='r', linestyle='-')
plt.plot([x[0] for x in is_1], [x[2] for x in is_1], label='average population fitness, island 1', color='r', linestyle='--')
plt.plot([x[0] for x in mig_1], [x[1] for x in mig_1], 'ro')

plt.plot([x[0] for x in is_2], [x[1] for x in is_2], label='best fitness, island 2', color='b', linestyle='-')
plt.plot([x[0] for x in is_2], [x[2] for x in is_2], label='average population fitness, island 2', color='b', linestyle='--')
plt.plot([x[0] for x in mig_2], [x[1] for x in mig_2], 'bo')

plt.legend()
plt.title('Evolution in One Max')
plt.ylabel('fitness')
plt.xlabel('generation')
plt.grid(True)
plt.show()