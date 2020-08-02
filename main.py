import random
from texttable import Texttable
from operator import attrgetter


class Individual:
  def __init__(self, number):
    self.decimal_number = number
    self.function_result = self.run_function(number)
    self.individual_in_bits = self.convert_to_bits(number)
    self.probability = 0
  
  def convert_to_bits(self,number):
    if (number >= 0):
      return "0"+'{0:04b}'.format(number)
    return "1"+'{0:04b}'.format(number*-1)

  def run_function(self,x):
    return (x*x - 3*x + 4)
  
  def set_probability(self,probability):
    self.probability = probability
  
  def set_individual_in_bits(self,bits):
    self.individual_in_bits = bits
  
  def set_decimal_number(self,number):
    self.decimal_number = number
  
  def set_function_result(self,number):
    self.function_result = number
  
  def get_function_result(self):
    return self.function_result
  
  def get_probability(self):
    return self.probability
  
  def get_individual_in_bits(self):
    return self.individual_in_bits
  
  def get_decimal_number(self):
    return self.decimal_number
  
  #Operator overloading to make crossover
  def makeCross(self, individual2):
    if (random.random() < 0.7):
      random_cut = random.randint(1,4)
      
      first_part_individual = self.individual_in_bits[0:random_cut]
      second_part_individual1 = self.individual_in_bits[random_cut:5]
      
      individual2_bits = individual2.get_individual_in_bits()
      
      first_part_individual2 = individual2_bits[0:random_cut]
      second_part_individual2 = individual2_bits[random_cut:5]

      first_son = first_part_individual + second_part_individual2
      second_son = first_part_individual2 + second_part_individual1

      return [first_son, second_son] 
    return None
  



NUMBER_OF_GENERATIONS = 5
POPULATION_LENGTH = 4
MINIMUM_VALUE = -10
MAXIMUM_VALUE = 10


def iniciar():
  individuals = generate_initial_population()
  current_generation = 0
  while current_generation < NUMBER_OF_GENERATIONS:
    set_probabilities(individuals)
    first_sample = run_tournament(individuals)
    second_sample = run_tournament(individuals)
    while first_sample == second_sample:
      second_sample = run_tournament(individuals)
    if run_crossover(first_sample,second_sample,individuals):
      run_mutation(2,individuals)
    normalize(individuals)
    print_table(individuals,current_generation)
    current_generation += 1

#Generate initial population with POPULATION_LENGTH individuals between -10 and 10
def generate_initial_population():
  #List of individuals objects
  individuals_list = []
  while (len(individuals_list) < POPULATION_LENGTH):
    randomNumber = random.randrange(MINIMUM_VALUE,MAXIMUM_VALUE)
    individuals_list.append(Individual(randomNumber))
  return individuals_list

#Set the probabilities of each individual 
def set_probabilities(individuals):
  sum_individuals = 0
  for individual in individuals:
    sum_individuals += individual.get_function_result()
  
  for individual in individuals:
    probability = individual.get_function_result()/sum_individuals
    individual.set_probability(probability)

#Get two random individuals and see which one has the greater probability
def run_tournament(individuals):
  samples = random.sample(individuals, 2)      
  max_value = 0
  max_sample = None
  for sample in samples:
    if sample.get_probability() > max_value:
      max_value = sample.get_probability()
      max_sample = sample
  return max_sample


#Make the crossover between two individulas
def run_crossover(individual1, individual2, individuals):
  #return response in bits
  response = individual1.makeCross(individual2)
  if response == None:
    return False
  else:
    first_son, second_son = response
    delete_worsts(2,individuals)
    first_son_integer = int(first_son[1:5],2)
    second_son_integer = int(second_son[1:5],2)
    if first_son[0] == "1":
      first_son_integer *= -1
    if second_son[0] == "1":
      second_son_integer *= -1
    individuals.append(Individual(first_son_integer))
    individuals.append(Individual(second_son_integer))
    return True


def run_mutation(number,individuals):
  for individual_index in range(1,number+1):
    individual_bits = individuals[individual_index*-1].get_individual_in_bits()
    bits_after_mutation = ""
    for bit in individual_bits:
      if random.random() < 0.01:
        bits_after_mutation += "0" if bit == "1" else "1"
      else:
        bits_after_mutation += bit
    individuals[individual_index].set_individual_in_bits(bits_after_mutation)

def delete_worsts(number,individuals):
  for i in range(number):
    min_individual = min(individuals,key=attrgetter('function_result'))
    individuals.remove(min_individual)
  
def normalize(individuals):
  for individual in individuals:
    individual_bits = individual.get_individual_in_bits()
    first_bit = individual_bits[0]
    integer = int(individual_bits[1:5], 2)
    if integer > 10:
      integer = 10
      individual_bits = first_bit + "1010"
    if first_bit == "1":
      integer *= -1
    individual.set_decimal_number(integer)
    individual.set_function_result(individual.run_function(integer))
    individual.set_individual_in_bits(individual_bits)
    individual.set_probability(0)

def print_table(individuals, generation):
  print("Geracao Atual: "+str(generation)+"\n" )
  table_rows = []
  table = Texttable()
  table_rows.append(['Individuo', 'valor de X', 'X Binario', 'f(x)'])
  for index, individual in enumerate(individuals):
    table_rows.append([index, individual.get_decimal_number(), individual.get_individual_in_bits(), individual.get_function_result()])
  table.add_rows(table_rows)
  print(table.draw())
  max_individual = max(individuals,key=attrgetter('function_result'))
  print("\nMaximo = "+str(max_individual.get_function_result())+"\n")
  print("\n\n")

if __name__ == "__main__":
    iniciar()
