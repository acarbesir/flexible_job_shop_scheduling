import itertools
import random

def SwappingMutation(p):
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring = p[:pos1] + [p[pos2]] + \
          p[pos1+1:pos2] + [p[pos1]] + \
          p[pos2+1:]

    return offspring

def NeighbourhoodMutation(p):
    pos3 = pos2 = pos1 = random.randint(0, len(p) - 1)

    while p[pos2] == p[pos1]:
        pos2 = random.randint(0, len(p) - 1)

    while p[pos3] == p[pos2] or p[pos3] == p[pos1]:
        pos3 = random.randint(0, len(p) - 1)

    sortedPositions = sorted([pos1, pos2, pos3])
    pos1 = sortedPositions[0]
    pos2 = sortedPositions[1]
    pos3 = sortedPositions[2]

    e1 = p[sortedPositions[0]]
    e2 = p[sortedPositions[1]]
    e3 = p[sortedPositions[2]]

    permutations = list(itertools.permutations([e1, e2, e3]))
    permutation  = random.choice(permutations)

    offspring = p[:pos1] + [permutation[0]] + \
          p[pos1+1:pos2] + [permutation[1]] + \
          p[pos2+1:pos3] + [permutation[2]] + \
          p[pos3+1:]

    return offspring

def HalfMutation(p, parameters):
    o = p
    jobs = parameters['jobs']

    size = len(p)
    r = int(size/2)

    positions = random.sample(range(size), r)

    i = 0
    for job in jobs:
        for op in job:
            if i in positions:
                o[i] = random.randint(0, len(op)-1)
            i = i+1

    return o

def MutationOS(p):
    if random.choice([True, False]):
        return SwappingMutation(p)
    else:
        return NeighbourhoodMutation(p)

def mutationMS(p, parameters):
    return HalfMutation(p, parameters)

def Mutation(population, parameters, config):
    newPop = []

    for (OS, MS) in population:
        if random.random() < config["pm"]:
            oOS = MutationOS(OS)
            oMS = mutationMS(MS, parameters)
            newPop.append((oOS, oMS))
        else:
            newPop.append((OS, MS))

    return newPop