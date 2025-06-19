import random

def POX(p1, p2, parameters):
    """
    Predecence Operation Crossover
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(1, jobNumber+1)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def JBX(p1, p2, parameters):
    """
    Job-Based Crossover
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(0, jobNumber)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def TPC(p1, p2):
    """
    Two Point Crossover
    """
    pos1 = random.randint(0, len(p1) - 1)
    pos2 = random.randint(0, len(p1) - 1)

    if pos1 > pos2:
        pos2, pos1 = pos1, pos2

    offspring1 = p1
    if pos1 != pos2:
        offspring1 = p1[:pos1] + p2[pos1:pos2] + p1[pos2:]

    offspring2 = p2
    if pos1 != pos2:
        offspring2 = p2[:pos1] + p1[pos1:pos2] + p2[pos2:]

    return (offspring1, offspring2)

def CrossoverOS(p1, p2, parameters):
    if random.choice([True, False]):
        return POX(p1, p2, parameters)
    else:
        return JBX(p1, p2, parameters)

def CrossoverMS(p1, p2):
    return TPC(p1, p2)

def Crossover(population, parameters, config):
    newPop = []
    i = 0
    while i < len(population):
        (OS1, MS1) = population[i]
        (OS2, MS2) = population[i+1]

        if random.random() < config["pc"]:
            (oOS1, oOS2) = CrossoverOS(OS1, OS2, parameters)
            (oMS1, oMS2) = CrossoverMS(MS1, MS2)
            newPop.append((oOS1, oMS1))
            newPop.append((oOS2, oMS2))
        else:
            newPop.append((OS1, MS1))
            newPop.append((OS2, MS2))

        i = i + 2

    return newPop