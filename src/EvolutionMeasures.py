from src.utilities import average_tuple, std_tuple
import matplotlib.pyplot as plt


class EvolutionMeasures:
    def __init__(self, file_names):
        self.data = []
        self.plots = []
        self.mean_time, self.mean_gen, self.mean_eval = 0, 0, 0

        for file in file_names:
            self.fetch_data(file)

        for generation in self.data:
            generation.process()

    def summarize_experiment(self, time, generations, evaluations):
        self.mean_time = average_tuple(time)
        self.mean_gen = average_tuple(generations)
        self.mean_eval = average_tuple(evaluations)

    def fetch_data(self, file):
        f = open(file, 'r')
        for line in f.read().split('\n'):
            if len(line) == 0:
                continue

            generation_idx, island_idx, max_fitness, average_fitness, migration, diversity = line.split(',')

            if len(self.data) > int(generation_idx):
                self.data[int(generation_idx)].samples += [Sample(float(diversity), float(max_fitness), float(average_fitness))]
            else:
                new_generation = Generation()
                new_generation.samples += [Sample(float(diversity), float(max_fitness), float(average_fitness))]
                self.data += [new_generation]
        f.close()

    def plot_fitness_graph(self, path, name, runs):
        X = range(len(self.data))
        diversities = [generation.diversity for generation in self.data]
        max = [generation.max_fitness for generation in self.data]
        average = [generation.average_fitness for generation in self.data]
        std_plus = [generation.max_fitness + generation.std for generation in self.data]
        std_minus = [generation.max_fitness - generation.std for generation in self.data]

        fig, ax1 = plt.subplots()
        ln1 = ax1.plot(X, average, label='average fitness', color='g', linestyle='-', linewidth=1)
        ln2 = ax1.plot(X, max, label='max fitness', color='b', linestyle='-', linewidth=1)
        ax1.fill_between(X, std_plus, std_minus, facecolors='b', alpha=0.1)

        ax2 = plt.twinx(ax1)
        ln3 = ax2.plot(X, diversities, label='diversity', color='r', linestyle='-', linewidth=1, alpha=0.5)

        # added these three lines
        lns = ln1 + ln2 + ln3
        labs = [l.get_label() for l in lns]
        lgd = ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=3, fancybox=True, shadow=True)

        plt.title(name, y=1.07)
        plt.suptitle('mean {time ' + '{:.2f}'.format(self.mean_time) + ' seconds, , generations ' + str(int(self.mean_gen)) +
                     ', evaluations ' + str(int(self.mean_eval)) + '}, runs ' + str(runs), y=0.93, fontsize=8)
        ax1.set_ylabel('fitness')
        ax2.set_ylabel('diversity')
        ax1.set_xlabel('generation')
        plt.grid(True)
        plt.savefig(path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.show()


class Plot:
    def __init__(self):
        self.x = []
        self.y = []


class Generation:
    def __init__(self):
        self.diversity, self.average_fitness, self.max_fitness, self.std = 0, 0, 0, 0
        self.samples = []

    def process(self):
        self.diversity = average_tuple([sample.diversity for sample in self.samples])
        self.average_fitness = average_tuple([sample.average_fitness for sample in self.samples])
        self.max_fitness = average_tuple([sample.max_fitness for sample in self.samples])
        self.std = std_tuple([sample.max_fitness for sample in self.samples])


class Sample:
    def __init__(self, diversity, max_fitness, average_fitness):
        self.diversity, self.average_fitness, self.max_fitness = diversity, average_fitness, max_fitness
