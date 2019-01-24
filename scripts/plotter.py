import sys
import matplotlib.pyplot as plt

name = sys.argv[1]

file = open('../exp/logs/' + name + '.log')

is_1 = []
is_2 = []
is_3 = []

mig_1 = []
mig_2 = []
mig_3 = []

for line in file:
	line = line.split(',')
	print(line)
	if line[1] == '0':
		is_1.append([int(line[0]),int(line[2]),float(line[3])])
		if line[4] == 'True':
			mig_1.append([int(line[0]), float(line[3])])
	elif line[1] == '1':
		is_2.append([int(line[0]),int(line[2]),float(line[3])])
		if line[4] == 'True':
			mig_2.append([int(line[0]), float(line[3])])
	else:
		is_3.append([int(line[0]),int(line[2]),float(line[3])])
		if line[4] == 'True':
			mig_3.append([int(line[0]), float(line[3])])

plt.plot([x[0] for x in is_1], [x[1] for x in is_1], label='best fitness, island 1', color='r', linestyle='-', linewidth=1.5)
plt.plot([x[0] for x in is_1], [x[2] for x in is_1], label='average population fitness, island 1', color='r', linestyle=':', linewidth=1)

plt.plot([x[0] for x in is_2], [x[1] for x in is_2], label='best fitness, island 2', color='b', linestyle='-', linewidth=1.5)
plt.plot([x[0] for x in is_2], [x[2] for x in is_2], label='average population fitness, island 2', color='b', linestyle=':', linewidth=1)

if len(is_3) != 0:
	plt.plot([x[0] for x in is_3], [x[1] for x in is_3], label='best fitness, island 3', color='g', linestyle='-', linewidth=1.5)
	plt.plot([x[0] for x in is_3], [x[2] for x in is_3], label='average population fitness, island 3', color='g', linestyle=':', linewidth=1)
	plt.plot([x[0] for x in mig_3], [x[1] for x in mig_3], 'go')

plt.plot([x[0] for x in mig_2], [x[1] for x in mig_2], 'bo')
plt.plot([x[0] for x in mig_1], [x[1] for x in mig_1], 'ro')


plt.legend(loc=4)
plt.title('Evolution in One Max')
plt.ylabel('fitness')
plt.xlabel('generation')
plt.grid(True)
plt.show()