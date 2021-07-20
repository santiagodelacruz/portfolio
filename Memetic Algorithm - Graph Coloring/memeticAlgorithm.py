from random import seed
from random import randint
import random
import readGraph as rg
import numpy as np
'''
By: Santiago De La Cruz
    Daniel Felipe Quesada
**Algorithm Process
    1. Initial random population
    2. Tabu Search
    Loop (number of iterations)
        3. Evaluation
        4. Selection
        5. Cross
        6. Shannon entropy
            6.1. Reset the population (%)
                 % -> Depends on the  Graph size
'''
#Tabu search
colorsList = []
t = 5
graph = rg.buildGraph()
vertices = graph[0]
edges = graph[1]
adjacencyMatrix = graph[2]
valueEntropy = 0.3
valueRamains = 1 - valueEntropy
def numberColors(agent):
    unique_list = []
    # traverse for all elements
    for x in agent:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return len(unique_list)
def evalGraph(agent):
    penaltyRepeat = 0
    penaltyColors = 0
    numColors = numberColors(agent)
    numErrors = 0
    eval = 0
    i = 0
    while(i < len(adjacencyMatrix)):
        j = 0
        adjacencyColors = []
        while(j < len(adjacencyMatrix[i])):
            vertice = adjacencyMatrix[i][j]
            color = agent[vertice-1]
            if(color in adjacencyColors):
                #Color repeat
                #Penalty
                numErrors+=1
            adjacencyColors.append(color)
            j+=1
        i+=1
    #penalty for number of errors
    penaltyRepeat = (numErrors/(vertices-1)) * 100
    #Penalty for number of colors
    penaltyColors = (numColors/(vertices-1)) * 100
    eval = penaltyRepeat + penaltyColors
    return eval
def searchNewColor(agent,adjacencyColors):
    newColor = 0
    i = 0
    while(i < len(agent)):
        if(agent[i] not in adjacencyColors):
            newColor = agent[i]
            break
        i += 1
    return newColor
def improveAgent(agent,tabuList):

    i = 0
    while(i < len(adjacencyMatrix)):
        j = 0
        adjacencyColors = []
        while(j < len(adjacencyMatrix[i])):
            vertice = adjacencyMatrix[i][j]
            color = agent[vertice-1]
            if(color in adjacencyColors):
                #Fix the error
                newColor = searchNewColor(agent,adjacencyColors)
                change = [color,newColor,i]
                if(change not in tabuList):
                    #Replace the color
                    agent[vertice-1] = newColor
                    #Update tabuList
                    tabuList.append(change)
                    break
            adjacencyColors.append(color)
            j+=1
        i+=1
def chooseBetterAux(evaluationsList):

    evaluationsList.sort()
    eval = evaluationsList[0]
    return eval
def chooseBetter(population):
    betterAgent = []
    i = 0
    eval = 0
    while(i < len(population)):
        evalAux = evalGraph(population[i])
        if(i == 0):
            eval = evalAux
            betterAgent = population[i]
        else:
            if(evalAux < eval):
                eval = evalAux
                betterAgent = population[i]
        i += 1
    return betterAgent
def tabuSearch(agent):
    newAgent = []
    population = []
    tabuList = []
    i = 0
    #Initial population
    while(i < t):
        population.append(agent[:])
        i += 1
    #Improve the agents
    i = 0
    while (i < t):
        j = 0
        while(j < t):
            #Improve each agent
            improveAgent(population[j],tabuList)
            j += 1
        #Reset tabuList
        tabuList = []
        i += 1
    newAgent = chooseBetter(population)
    return newAgent
def randomPopulation(n,numGens,numColors):
    seed(64)
    population = []
    i = 0
    while(i < n):
        agent = [randint(0,numColors-1) for i in range(numGens)]
        population.append(agent)
        i += 1
    return population
def initPopulation(n,numGens,numColors):
    population = []
    randPopulation = []
    #Create random agents
    randPopulation = randomPopulation(n,numGens,numColors)
    i = 0
    #Improve each agent with Tabu search
    while(i < n):
        newAgent = tabuSearch(randPopulation[i])
        #Save the new agent in population
        population.append(newAgent)
        i += 1
    return population
def evaluations(population):
    evaluations = []
    i = 0
    while(i < len(population)):
        eval = evalGraph(population[i])
        evaluations.append(int(eval))
        i += 1
    return evaluations
def selRandom(evaluationsList,k):
    return [random.choice(evaluationsList) for i in range(k)]
def selTournament(population, tournsize, k, evaluationsList):
    chosen= []
    for _ in range(k):
        evaluationsAspirants = selRandom(evaluationsList, tournsize)
        evalBest = chooseBetterAux(evaluationsAspirants)
        ind = evaluationsList.index(evalBest)
        aspirantBest = population[ind]
        chosen.append((aspirantBest))
    return chosen
def cxTwoPoint(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    return ind1, ind2
def crossAgents(selected):
    i = 0
    newAgents = []
    while(i < len(selected)-1):
        ind1, ind2 = cxTwoPoint(selected[i], selected[i+1])
        newAgents.append(ind1)
        newAgents.append(ind2)
        i += 2
    return newAgents
def insertNewAgents(population, evaluationsList, newAgents):
    copyList = evaluationsList[:]
    copyList.sort()
    numAgent = len(newAgents)
    delta = len(evaluationsList)
    init = delta - numAgent
    evaluationsAgents = copyList[init:]
    i = 0
    while(i < len(evaluationsAgents)):
        ind = evaluationsList.index(evaluationsAgents[i])
        newEval = evalGraph(newAgents[i])
        if(evaluationsList[ind] > newEval):
            population[ind] = newAgents[i]
            evaluationsList[ind] = newEval
            #print("Changing")
        i += 1
def shannonEntropy(fitnessList):
    """
    :param individual: to calculate the fitness
    :var fitnessList: is a fitness list from the population
    :var size_fitness: is the size form the fitness list
    :var repeatCount:  how many times a valor repeats in the fitness list
    :var probability: list to be chosen
    :var size_probability: size form the probability list
    :returns: The shannon entropy, How diverse is the population
    """
    size_fitness = len(fitnessList)
    repeatCount = np.bincount(fitnessList)
    probability = repeatCount[np.nonzero(repeatCount)]/size_fitness
    size_probability = len(probability)
    if size_probability <= 1:
        return 0
    return - np.sum(probability * np.log(probability)) /np.log(size_probability)
def run(iterations, n, numGens, numColors, tournsize, k):
    evaluationsList = []
    population = initPopulation(n,numGens,numColors)
    i = 0
    while(i < iterations):
        print("Iteration: ",i+1)
        #Evaluation
        evaluationsList = evaluations(population)
        #Selection
        selected = selTournament(population, tournsize, k, evaluationsList)
        #Cross
        newAgents = crossAgents(selected[:])
        #Insert new agents in the population
        insertNewAgents(population,evaluationsList,newAgents)
        #Shannon entropy
        entropy = shannonEntropy(evaluationsList[:])
        if(entropy <= valueEntropy):
            #Choose the percentage of the population that remains
            porRamains = int(n * valueRamains)
            remains = selRandom(population,porRamains)
            #Choose the new population
            porNewPop = int(n * (1-valueRamains))
            newPopulation = initPopulation(porNewPop,numGens,numColors)
            #Reset the population
            population = remains + newPopulation
        i += 1
    return population
def ranking(results,top):
    rank = []
    agent = []
    evals = evaluations(results)
    evalsCopy = evals[:]
    evalsCopy.sort()
    i = 0
    while(i < top):
        ind = evals.index(evalsCopy[i])
        agentAux = results[ind]
        agent = []
        agent.append(agentAux)
        agent.append(evalsCopy[i])
        rank.append(agent)
        i += 1
    return rank
def numberColors(agent):
    unique_list = []
    # traverse for all elements
    for x in agent:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return len(unique_list)
def main():
    #Number of gens
    numGens = vertices
    #Population size
    n = numGens * 2
    #Number of colors in the worst of cases
    numColors = numGens - 1
    #Number of iterations
    iterations = 1000
    #Numbers of best solutions that you want to see
    top = 3
    #Operatos arguments
    tournsize = 3
    k = 2
    results = run(iterations, n, numGens, numColors, tournsize, k)
    rank = ranking(results,top)
    i = 0
    e = numberColors(list(rank[0][0]))
    print("Number of colors: ",e)
    while(i < top):
        print("Solution ",i+1)
        print(rank[i])
        i += 1

if __name__=="__main__":
    main()
