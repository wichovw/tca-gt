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
    real_intersections = {}
    for intersection in traffic_lights:
        intersections[intersection['id']] = [l % max_lights for l in intersection['lights']]
        real_intersections[intersection['id']] = [l for l in intersection['lights']]
    return intersections, real_intersections

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

def decode_chromosome(period, normal_inters, real_inters, individual):
    '''
    Receives a period, the normalized intersections, the real intersections, and an individual
    Returns a list of intersection descriptions according to the API
    '''
    api_inters = []
    for inter_id, inter_lights in normal_inters.items():
        api_inter = {"id": inter_id, "lights": real_inters[inter_id]}
        light_past = -1
        schedule = {}
        for t in range(period):
            light_t = individual[t]
            if light_t != light_past:
                schedule[t] = real_inters[inter_id][inter_lights.index(light_t)]
                light_past = light_t
        api_inter['schedule'] = schedule
        api_inters.append(api_inter)
    return api_inters

def evaluate(simulator, period, normal_inters, real_inters, individual):
    '''
    Receives a simulator instance, an intersection map and an individual
    Executes simulation and returns fitness values
    '''
    #Map normalized ids to real ids and calculate times
    api_inters = decode_chromosome(period, normal_inters, real_inters, individual)
    simulator.reset_statistics()
    #Change traffic lights and configuration and run simulation
    simulator.set_traffic_lights(api_inters)
    simulator.fixed_time_start(period * 5)
    
    return simulator.get_average_speed(), simulator.get_stopped_time()

def fill_toolbox(intersections, period, simulator):
    '''
    Returns a DEAP toolbox with required components
    '''
    normal_inters, real_inters = get_normalized_lights(intersections)
    #Register toolbox components
    toolbox = base.Toolbox()
    #Population building components
    toolbox.register("attr_light", random.choice)
    toolbox.register("individual", build_rand_chromosome, creator.Individual, normal_inters, period, toolbox.attr_light)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #Register operator
    toolbox.register("selectBest", tools.selBest)
    toolbox.register("selectRest", tools.selTournament)
    toolbox.register("mate", tools.cxUniform)
    toolbox.register("mutate", tools.mutShuffleIndexes)
    toolbox.register("decode", decode_chromosome, period, normal_inters, real_inters)
    toolbox.register("evaluate", evaluate, simulator, period, normal_inters, real_inters)
    #Register helper
    toolbox.register("clone", copy.copy)
    
    return toolbox

def find_solution(population=100, max_gen=10, period=10, seed=64):
    '''
    Recives configurations for the genetic algorithm: period, seed
    Executes algorithm to find a result
    Returns found solution
    '''
    #Get simulator data
    simulator = TCAService()
    intersections = simulator.get_traffic_lights()
    
    #Register global creator classes
    
    #Fitrness function should maximize average speed and minimize total stopped time
    creator.create("FitnessMin", base.Fitness, weights=(1.0, -1.0,))
    #Individual basic definition
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    #Set random seed and fill toolbox
    random.seed = seed
    toolbox = fill_toolbox(intersections, period, simulator)
    
    #Init population
    population = toolbox.population(n=population)
    
    #Evaluate the entire population fitness
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    #Operator probability
    CXPB, MUTPB = 0.5, 0.01
    
    #Iterate generations
    g = 0
    
    while g < max_gen:
        print("g:"+str(g))
        # Select the next generation individuals
        best_num = int(len(population) * 0.20)
        offspring = toolbox.selectBest(population, best_num)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        offspring = [toolbox.clone(child) for child in offspring]
        # Select the next generation individuals
        offspring2 = toolbox.selectRest(population, (len(population)), 2)
        # Clone the selected individuals
        offspring2 = list(map(toolbox.clone, offspring2))
        
        # Apply crossover on the offspring
        for child1, child2 in zip(offspring2[::2], offspring2[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2, 0.2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring2:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, 0.1)
                del mutant.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring2 if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        offspring.extend(offspring2)
        # The population is entirely replaced by the offspring
        population[:]= offspring
        g += 1
    #Select the best one
    best = toolbox.selectBest(population, 1)[0]
    print(toolbox.decode(best))
    print(best.fitness.values)

if __name__ == '__main__':
    import cProfile
    cProfile.run('find_solution(population=100, max_gen=10, period=30)')
    
