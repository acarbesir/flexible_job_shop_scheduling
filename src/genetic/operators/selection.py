import random

from src.genetic.objective import CalculateFitness

def ElitistSelection(population, parameters, methodIndex, weights, config):
    keptPopSize = int(config["pr"] * len(population))
    sortedPop = sorted(population, key=lambda cpl: CalculateFitness(cpl, parameters, methodIndex, weights))
    return sortedPop[:keptPopSize]

def TournamentSelection(population, parameters, methodIndex, weights):
    b = 2
    selectedIndividuals = []
    for i in range(b):
        randomIndividual = random.randint(0, len(population) - 1)
        selectedIndividuals.append(population[randomIndividual])

    return min(selectedIndividuals, key=lambda cpl: CalculateFitness(cpl, parameters, methodIndex, weights))

def Selection(population, parameters, method, weights, config):
    newPop = ElitistSelection(population, parameters, method, weights, config)
    while len(newPop) < len(population):
        newPop.append(TournamentSelection(population, parameters, method, weights))

    return newPop