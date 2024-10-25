### this program is an algorithm that generates random genes in individuals in a population, feeds them into a test function
### then enters in an experiment loop(10), which then goes through a loop of generations, selecting parents from the population
### doing a crossover and a mutation in their genes in a new offspring array, then switching worst person in offspring 
### with best person in population, and plotting best fitnesses and averages in a graph of two lines(when uncommented). it then will change
### the mutation rate [0 , 1] and mutation step [0 , 1] and run the code again from the start. all the data will be appended in a 
### text file in the form of tables. 

### equations 1 & 2 ###
### Suleima Abbara - 19020111
### Artificial Intelligence ii - December 2021

### Note: this code will take a really long time to finish
import matplotlib.pyplot as pythonn
import random
import copy
import math
P = 300
N = 20
generations = 400
f = open('secondProblem.txt', 'a')
MUTSTEP = 0.1
for s in range (0 , 10):
    MUTRATE = 0.1
    for r in range (0 , 10):
        MUTSTEP = round(MUTSTEP , 3)
        MUTRATE = round(MUTRATE , 3)
        bestFirstGen = 0
        bestLastGen = 0
        averageBestFirstGen = 0
        averageBestLastGen = 0
        gen = generations - 1
        experiment = 10
        print("MUTSTEP:  ", MUTSTEP)
        f.write("\n\n\nMUTSTEP: " + str(MUTSTEP)+ '\n')
        print("MUTRATE: ", MUTRATE)
        f.write("MUTRATE: "+ str(MUTRATE)+ '\n\n')
        class individual:
            def __init__(self):
                self.gene = [0] * N
                self.fitness = 0 
        f.write("E     G      Best            Average       G      Best          Average"+ '\n')
        for E in range (0 , experiment):
            MIN = -10
            MAX = 10

            averagefitnesses = []
            bestest = []

            population = []
            for x in range (0,P):
                    tempgene = []
                    for x in range (0,N):
                        tempgene.append(random.uniform(MIN,MAX))
                    newind = individual()
                    newind.gene = tempgene.copy() 
                    population.append(newind)

            # problem 2 test function
            def test_function(ind):
                s = 0
                solution = 0
                for i in range(1, N):
                    s += math.pow(((2 * ind.gene[i] * ind.gene[i]) - (ind.gene[i-1])), 2) * i
                solution = math.pow((ind.gene[0]-1),2) + s
                return solution

            # problem 1 test function
            #def test_function(ind):
                #s = 0
                #for i in range(0 , N):
                #    s += ((ind.gene[i] ** 4) - (16 * ind.gene[i] * ind.gene[i]) + (5 * ind.gene[i]))
                #solution = 0
                #solution = s / 2
                #return solution

            for j in range (0 , P):
                population[j].fitness = test_function(population[j])

            for G in range (generations):
                    offspring = []
                    #this is the selection process - parents are being selected from the population array
                    for i in range (0 , P):
                        parent1 = random.randint( 0 , P-1 )
                        off1 = population[parent1]
                        parent2 = random.randint( 0 , P-1 )
                        off2 = population[parent2]
                        if off1.fitness < off2.fitness:
                            offspring.append( off1 )
                        else:
                            offspring.append( off2 )
                    #this is the crossover - parents having their genes crossed
                    toff1=individual()
                    toff2=individual()
                    temp = individual()
                    for i in range (0 , P , 2):
                        toff1 = copy.deepcopy(offspring[i])
                        toff2 = copy.deepcopy(offspring[i+1])
                        temp = copy.deepcopy(offspring[i])
                        crosspoint = random.randint(1,N)
                        for j in range (crosspoint , N):
                            toff1.gene[j] = toff2.gene[j]
                            toff2.gene[j] = temp.gene[j]
                        offspring[i] = copy.deepcopy(toff1)
                        offspring[i+1] = copy.deepcopy(toff2)
                    #this is the mutation - genes of parents being altered creating the offspring
                    for i in range (0 , P):
                        for j in range (0 , N):
                            if (random.random() < MUTRATE):
                                alter = random.uniform (-MUTSTEP , MUTSTEP)
                                offspring[i].gene[j] = offspring[i].gene[j] + alter
                                if(offspring[i].gene[j] > MAX):
                                    offspring[i].gene[j] = MAX
                                if(offspring[i].gene[j] < MIN):
                                    offspring[i].gene[j] = MIN

                    bestind = individual()
                    worstind = individual()
                    bestind = copy.deepcopy(population[0])
                    worstind = copy.deepcopy(offspring[0])
                    worstPoss = 0
                    offspringtotal = 0
                    bestfitness = 0
                    
                    for j in range (0 , P):
                        #find the best in population and save it
                        if (population[j].fitness<bestind.fitness):
                            bestind = copy.deepcopy(population[j])
                        #find the worst in offspring and save its place in the array
                        if (offspring[j].fitness<worstind.fitness):
                            worstPoss = j

                    #replace the worst person in offspring with the best from population
                    offspring[worstPoss] = copy.deepcopy(bestind)

                    offspring[0].fitness = test_function(offspring[0])
                    bestfitness = offspring[0].fitness
                    bestNo = 0
                    for j in range (0 , P):
                        #add all the fitnesses in offspring to average them
                        offspring[j].fitness = test_function(offspring[j])
                        offspringtotal = offspringtotal + offspring[j].fitness
                        #find the best fitness in offspring and then put it in an array
                        if (offspring[j].fitness < bestfitness):
                            bestfitness = offspring[j].fitness
                            bestNo = j

                    average = offspringtotal / P

                    bestest.append(bestfitness)
                    averagefitnesses.append(average)

                    bestfitness = round (bestfitness, 4)
                    average = round(average, 4)
                    if (G == 0 ):
                        f.write(str(E)+"     "+str(G)+ "    " + str(bestfitness))
                        f.write("    " + str(average)+ '     ')
                        bestFirstGen = bestFirstGen + offspring[bestNo].fitness
                    elif (G == gen ):
                        f.write(str(G)+ "    " + str(bestfitness))
                        f.write("        " + str(average)+ '\n')
                        bestLastGen = bestLastGen + offspring[bestNo].fitness
                    
                    population = copy.deepcopy(offspring)
            ##if uncommented, these next lines will run with graphs, only use when code is running once
            #pythonn.plot(averagefitnesses, label = "line 2")
            #pythonn.plot(bestest, label = "line 1")
            #pythonn.show()
        averageBestFirstGen = bestFirstGen / experiment
        averageBestLastGen = bestLastGen / experiment
        averageBestFirstGen = round(averageBestFirstGen, 4)
        averageBestLastGen = round(averageBestLastGen, 4)
        f.write ("\n           " +str(averageBestFirstGen)+ "                          "+str(averageBestLastGen)+"\n") 
        MUTRATE = MUTRATE + 0.1
    MUTSTEP = MUTSTEP + 0.1
f.close()
