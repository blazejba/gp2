from random import random, randint
from src.utilities import normalize_tuple, accumulate_tuple


def roulette_wheel(quantity, scores):
	# Probability of being selected depends on the fitness
	indexes = []
	for _ in range(quantity):
		indexes.append(roll(scores))
	return indexes


def roll(scores):
	R = random()
	anl = accumulate_tuple(normalize_tuple(scores))
	for index, entry in enumerate(anl):
		if entry >= R:
			return index


def rank_based(quantity, population_size):
	# Probability of being selected depends on position in the rank
	indexes = []
	for _ in range(quantity):
		R = random()
		anl = accumulate_tuple(normalize_tuple([x for x in range(population_size, 0, -1)]))
		for index, entry in enumerate(anl):
			if entry >= R:
				indexes.append(index)
	return indexes


def truncation(quantity):
	return [i for i in range(quantity)]


def tournament(quantity, scores):
	indexes = []
	for _ in range(quantity):
		parent1 = randint(0, len(scores) - 1)
		parent2 = randint(0, len(scores) - 1)
		while parent1 == parent2:
			parent2 = randint(0, len(scores) - 1)
		if scores[parent1] > scores[parent2]:
			indexes.append(parent1)
		elif scores[parent1] == scores[parent2]:
			indexes.append(parent1 if randint(0,1) == 1 else parent2)
		else:
			indexes.append(parent2)
	return indexes


def sort_by_scores(scores):
	tmp_scores = scores
	scores = []
	while len(tmp_scores) > 0:
		best_score = 0
		best_score_index = 0
		for index, score in enumerate(tmp_scores):
			if score[1] > best_score:
				best_score = score[1]
				best_score_index = index
		scores.append(tmp_scores[best_score_index])
		tmp_scores.remove(tmp_scores[best_score_index])
	return scores