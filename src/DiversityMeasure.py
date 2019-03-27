from collections import Counter
from math import log


class DiversityMeasure:
    @staticmethod
    def entropy(fitness_list):
        fitness_list = [round(fitness*10) for fitness in fitness_list]
        probabilities = [partition_k/len(fitness_list) for partition_k in Counter(fitness_list).values()]
        entropy = 0
        for p_k in probabilities:
            entropy += p_k * log(p_k, 10)
        return -entropy


if __name__ == '__main__':
    fitness_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dv = DiversityMeasure()
    print(dv.entropy(fitness_list))

