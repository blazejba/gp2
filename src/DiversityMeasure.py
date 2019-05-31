from collections import Counter
from math import log
from numpy import zeros, c_
from scipy.cluster.vq import kmeans, vq, whiten


class DiversityMeasure:
    def __init__(self, population, metric):
        self.population = population
        self.num_of_clusters = int(population / 3)
        self.entropy = 0
        self.metric = metric

    def fitness_control(self, fitness_list):
        distance_matrix = c_[fitness_list]
        clx = self.kmeans_clustering(distance_matrix)
        return self.shared_weight(clx)

    def edit_distance_control(self, forest):
        distance_matrix = self.calculate_distance_matrix(forest)
        clx = self.kmeans_clustering(distance_matrix)
        return self.shared_weight(clx)

    def shared_weight(self, clx):
        weights = []
        for num in range(self.num_of_clusters):
            occurrences = clx.count(num)
            weights.append(1 / occurrences if occurrences != 0 else 0)
        return [weights[cluster] for cluster in clx]

    def kmeans_clustering(self, distance_matrix):
        centroids, _ = kmeans(distance_matrix, self.num_of_clusters)
        clx, _ = vq(distance_matrix, centroids)
        return list(clx)

    def calculate_distance_matrix(self, forest):
        distance_matrix = zeros((population, population))
        for y, tree_y in enumerate(forest):
            for x, tree_x in enumerate(forest):
                distance_matrix[x, y] = self.ordered_edit_distance(tree_y, tree_x)
        return whiten(distance_matrix)

    def calculate_entropy(self, fitness_list):
        fitness_list = [round(fitness * 100) for fitness in fitness_list]
        probabilities = [partition_k / len(fitness_list) for partition_k in Counter(fitness_list).values()]
        entropy = 0
        for p_k in probabilities:
            entropy += p_k * log(p_k, 10)
        self.entropy = -entropy / log(len(probabilities), 10) if len(probabilities) > 1 else 0

    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    @staticmethod
    def ordered_edit_distance(t1, t2):
        if t1 == t2:
            return 0

        distance = 0
        for index in range(len(t1.nodes)):
            node_1 = t1.nodes[index].value
            node_2 = t2.nodes[index].value
            if node_1 == node_2:  # distance between identical nodes is 0
                continue
            else:
                distance += 1
        return distance


if __name__ == '__main__':
    fitness = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 7.0, 8.0]
    fitness_array = c_[fitness]
    population = 6
    dm = DiversityMeasure(population, 'fitness')
    dm.calculate_entropy(fitness)
    print(dm.kmeans_clustering(fitness_array))