# -*- coding: utf-8 -*-
"""genetic2b.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gwx-6LSg7axeunUVrUQ27CjS6IW6O8iQ
"""

!pip install pyeasyga
import random 
from pyeasyga import pyeasyga



seed_data = [{'name':'machine0', 'RUL':3,'cost':100, 'timeconsumption' : 100, 'productionLine':1}, 
             {'name': 'machine1', 'RUL':5,'cost':70,'timeconsumption': 100, 'productionLine':2}, 
             {'name':'machine2', 'RUL': 20,'cost':80,'timeconsumption' :100,'productionLine':1}, 
             {'name': 'machine3', 'RUL':5,'cost':45,'timeconsumption': 100, 'productionLine':3}, 
             {'name':'machine4', 'RUL': 20,'cost':150,'timeconsumption' :100,'productionLine':3}, 
             {'name': 'machine5', 'RUL':5,'cost':350,'timeconsumption': 100, 'productionLine':2}, 
             {'name':'machine6', 'RUL': 20,'cost':98,'timeconsumption' :100,'productionLine':2}, 
             {'name': 'machine7', 'RUL':5,'cost':654,'timeconsumption': 100, 'productionLine':1}, 
             {'name':'machine8', 'RUL': 20,'cost':789,'timeconsumption' :100,'productionLine':4}]


# initialise the GA
ga = pyeasyga.GeneticAlgorithm(seed_data,
                            population_size=100,
                            generations=200,
                            crossover_probability=0.8,
                            mutation_probability=0.5,
                            elitism=True,
                            maximise_fitness=False)

def create_individual(data):

    a3 = list(range(len(data)))
    random.shuffle(a3)
    return a3

ga.create_individual = create_individual

def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, len(parent_1))
    # crossover_index2 = random.randrange(crossover_index, len(parent_1))
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b
    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
    child_2 = child_2a + child_2b
    return child_1, child_2

# and set the Genetic Algorithm's ``crossover_function`` attribute to
# your defined function
ga.crossover_function = crossover

# define and set the GA's mutation operation
def mutate(individual):
    mutate_index1 = random.randrange(len(individual))
    mutate_index2 = random.randrange(len(individual))
    individual[mutate_index1], individual[mutate_index2] = individual[mutate_index2], individual[mutate_index1]

ga.mutate_function = mutate

def fitness (individual, data):
    print(individual)
    cost = 0
    line = 0
    days =0
    for (selected, ind) in zip(individual, data):
        #
        cost += seed_data[selected].get('cost')
        line2 = seed_data[selected].get('productionLine')
        days +=seed_data[selected]
        if (line == line2):
            cost -= 10
        line = line2


      
                
    return cost

ga.fitness_function = fitness       # set the GA's fitness function
# define and set the GA's selection operation
def selection(population):
 
    return random.choice(population)

ga.selection_function = selection
ga.run()                            # run the GA


def printResult(result,data):
  s="["
  i=0
  for machine in result:
  
    if i==len(result)-1:
      s += data[machine].get('name')
      
    else:
      s += data[machine].get('name') + ", "
    i+=1
  s+="]"
  print(s)
  
print("Cost - " , ga.best_individual()[0])
printResult(ga.best_individual()[1],seed_data)
