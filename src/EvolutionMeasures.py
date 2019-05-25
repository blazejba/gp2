from src.utilities import average_tuple, std_tuple
import matplotlib.pyplot as plt


class EvolutionMeasures:
    def __init__(self, file_names):
        self.data = []
        self.plots = []
        self.mean_time, self.mean_gen, self.mean_eval = 0, 0, 0
        self.mean_time_std, self.mean_gen_std, self.mean_eval_std = 0, 0, 0
        self.times, self.generations, self.evaluations, self.reasons = [], [], [], []
        self.terminaton = []

        for file in file_names:
            self.fetch_data(file)

        for generation in self.data:
            generation.process()

        self.summarize_experiment()

    def summarize_experiment(self):
        self.mean_time = average_tuple(self.times)
        self.mean_gen = average_tuple(self.generations)
        self.mean_eval = average_tuple(self.evaluations)
        self.mean_time_std = std_tuple(self.times)
        self.mean_gen_std = std_tuple(self.generations)
        self.mean_eval_std = std_tuple(self.evaluations)
        self.termination = [self.reasons.count('fitness')*100/len(self.reasons),
                            self.reasons.count('generation') * 100 / len(self.reasons),
                            self.reasons.count('timeout') * 100 / len(self.reasons)]

    def fetch_data(self, file):
        f = open(file, 'r')
        plots = []
        for line in f.read().split('\n'):
            if len(line) == 0:
                continue

            line_split = line.split(',')

            if len(line_split) == 4: # this is a summary for an experiment, meaning last line of a file
                self.times += [float(line_split[0])]
                self.generations += [int(line_split[1])]
                self.evaluations += [int(line_split[2])]
                self.reasons += [line_split[3]]
                continue

            self.generation_based_seperation(line_split)
            plots = self.plot_based_seperation(line_split, plots)
        f.close()
        self.plots += plots

    def generation_based_seperation(self, line_split):
        generation_idx, island_idx, max_fitness, average_fitness, migration, diversity = line_split
        if len(self.data) > int(generation_idx):
            self.data[int(generation_idx)].samples += [
                Sample(float(diversity), float(max_fitness), float(average_fitness))]
        else:
            new_generation = Generation()
            new_generation.samples += [Sample(float(diversity), float(max_fitness), float(average_fitness))]
            self.data += [new_generation]

    def plot_based_seperation(self, line_split, plots):
        generation_idx, island_idx, max_fitness, average_fitness, migration, diversity = line_split
        if int(generation_idx) == 0:
            plots += [Plot()]

        plots[int(island_idx)].max_fitness += [float(max_fitness)]
        plots[int(island_idx)].average_fitness += [float(average_fitness)]

        return plots

    def plot_fitness_graph(self, path, name, runs):
        X = range(len(self.data))
        diversities = [generation.diversity for generation in self.data]
        max = [generation.max_fitness for generation in self.data]
        average = [generation.average_fitness for generation in self.data]
        std_plus = [generation.max_fitness + generation.std for generation in self.data]
        std_minus = [generation.max_fitness - generation.std for generation in self.data]

        fig, ax1 = plt.subplots()
        ln1 = ax1.plot(X, average, label='avg generation fitness', color='g', linestyle='-', linewidth=1, alpha=0.6)
        ln2 = ax1.plot(X, max, label='avg max fitness', color='b', linestyle='-', linewidth=1, alpha=0.6)
        #ax1.fill_between(X, std_plus, std_minus, facecolors='b', alpha=0.05)

        ax2 = plt.twinx(ax1)
        ln3 = ax2.plot(X, diversities, label='avg diversity', color='r', linestyle='-', linewidth=1, alpha=0.4)

        if len(self.plots) > 1:
            for plot in self.plots:
                X = range(len(plot.max_fitness))
                ln4 = ax1.plot(X, plot.max_fitness, color='grey', label='max fitness', alpha=0.20)
            lns = ln1 + ln2 + ln3 + ln4
        else:
            lns = ln1 + ln2 + ln3

        labs = [l.get_label() for l in lns]
        lgd = ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2, fancybox=True, shadow=True)

        plt.title(name, y=1.07)
        plt.suptitle('{:.2f}'.format(self.mean_time) + ' (± ' + '{:.2f}'.format(self.mean_time_std) + ') seconds, ' +
                     str(int(self.mean_gen)) + ' (± ' + str(int(self.mean_gen_std)) + ') generations, ' +
                     str(int(self.mean_eval)) + ' (± ' + str(int(self.mean_eval_std)) + ') evaluations' +
                     '\nbased on ' + str(runs) + ' iterations, ' + 'terminated based on ' + str(self.termination[0]) + '% fitness, ' +
                     str(self.termination[1]) + '% generation and ' + str(self.termination[2]) + '% timeouts.', y=0.93, fontsize=8)
        ax1.set_ylabel('fitness')
        ax2.set_ylabel('diversity')
        ax1.set_xlabel('generation')
        plt.grid(True)
        plt.savefig(path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.show()

    def min_mean_max(self):
        print('min/mean/max:',
              min([plot.max_fitness[-1] for plot in self.plots]),
              average_tuple([plot.max_fitness[-1] for plot in self.plots]),
              max([plot.max_fitness[-1] for plot in self.plots]))

class Plot:
    def __init__(self):
        self.max_fitness = []
        self.average_fitness = []


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
