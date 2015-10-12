import random
import copy

from deap import base
from deap import creator
from deap import tools

from service.tca_service import TCAService


def get_normalized_lights(traffic_lights):
    '''
    Recieves an array of intersection dicts
    Returns a dict with the form {id: [normalized ids]}
    '''
    #Get the max amount of lights on any intersection
    max_lights = max(len(_['lights']) for _ in traffic_lights)
    #Build a normalized list of IDs for each light
    intersections = {}
    for intersection in traffic_lights:
        intersections[intersection['id']] = [l % max_lights for l in intersection['lights']]
    return intersections

def build_rand_chromosome(individual, intersections, period, getrand):
    '''
    Receives a normalized intersection lights dict, a period and a random choice function
    Returns an array with a chromosome form
    '''
    chromosome = []
    for id, lights in intersections.items():
        for _ in range(period):
            chromosome.append(getrand(lights))
    return individual(chromosome)

def fixed_choice(alist):
    random.seed = 1992
    return random.choice(alist)

def evaluate(individual):
    #Decode individual
    #Run simulation
    print(individual)
    return sum(individual),

def fill_toolbox(intersections, period):
    '''
    Returns a DEAP toolbox with required components
    '''
    #Register toolbox components
    toolbox = base.Toolbox()
    #Population building components
    toolbox.register("attr_light", fixed_choice)
    toolbox.register("individual", build_rand_chromosome, creator.Individual, intersections, period, toolbox.attr_light)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #Register operator
    toolbox.register("select", tools.selBest)
    toolbox.register("mate", tools.cxUniform)
    toolbox.register("mutate", tools.mutShuffleIndexes)
    toolbox.register("evaluate", evaluate)
    #Register helper
    toolbox.register("clone", copy.copy)
    
    return toolbox

'''
Recives configurations for the genetic algorithm: period, seed
Executes algorithm to find a result
Returns found solution
'''
def find_solution(population=5, max_gen=2, period=10, seed=1992):
    #Get simulator data
    simulator = TCAService()
    intersections = simulator.get_traffic_lights()
    normal_lights = get_normalized_lights(intersections)
    
    #Register global creator classes
    
    #Fitrness function should maximize average speed and minimize total stopped time
    creator.create("FitnessMin", base.Fitness, weights=(1.0, -1.0,))
    #Individual basic definition
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    #Set random seed and fill toolbox
    random.seed = seed
    toolbox = fill_toolbox(normal_lights, period)
    
    #Init population
    population = toolbox.population(n=population)
    
    #Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
        print(fit)

    #Operator probability
    CXPB, MUTPB = 0.5, 0.2
    
    #Iterate generations
    for g in range(max_gen):
        # Select the next generation individuals
        offspring = toolbox.select(population, int(len(population) / 2))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)
        offspring = [toolbox.clone(child) for child in offspring]
        print(offspring)
        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2, 0.2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, 0.1)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        population[:]= offspring
    

if __name__ == '__main__':
    find_solution(period=1, seed=1992)
