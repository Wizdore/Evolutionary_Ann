import gym
import numpy as np

env = gym.make('CartPole-v0')


class ANN:
    def __init__(self, state):
        self.state = state                      # 29 size vector that holds weights and biases of whole network
        self.activation = lambda x: (2/(1+ np.exp(-0.5*x)))-1   # Slightly modified tanh Activation Function that should work better in our case
        self.fitness = 0
    
    def set_hl_activation(self, activation):        # Optional function change the activation function
        self.activation = activation

    def get_output(self, inputs):
        hl_weight = self.state[0:20].reshape(5,4)       # First 20 elements are weights for input to hidden layer edges
        hl_bias = self.state[20:24]                     # Next 4 elements are for 4 nodes of hidden layer
        ol_weight = self.state[24:28].reshape(4,1)      # Next 4 elements are for 4 weights for hidden to output edges 
        ol_bias = self.state[28:29]                     # Next 1 element is the bias of the output layer

        inputs = self.activation(inputs)                # Normalizing the input values

        hl_result = (np.matmul(inputs, hl_weight) + hl_bias)        # calc from input to hidden layer (is linear activation good enough?!)
        ol_result = (np.matmul(hl_result, ol_weight) + ol_bias)     # calc from Hidden to output layer

        return ol_result        # returning raw result of the network


def crossover(parent1, parent2):
    """
    Parent1 and Parent2 are 2 states from 2 networks.
    The two parents are chosen from the top performers in the generation.
    Returns a tuple containing child 1 and child 2 which has mixed values from parent 1 and 2.
    """
    pivot = np.random.randint(0, len(parent1)) # Pick a random number.
    # Create children.
    child1 = parent1
    child2 = parent2
    # Crossover data.
    child1[:pivot] = parent2[:pivot]
    child2[:pivot] = parent1[:pivot]
    
    return child1, child2

def mutate_all(child, rate=0.001):
    """
    Go through each element in the state and check if that element should be mutated with
    probability 'rate'.
    """
    m = np.random.uniform(0.0,1.0,size=len(child))
    for idx, _ in enumerate(child):
        if rate >= m[idx]:
            child[idx] = np.random.uniform(-1,1)

def mutation_single(child, rate=0.5):
    """
    Mutate single index (element) in state if mutation probability = TRUE.
    """
    if rate >= np.random.uniform(0,1):
        child[np.random.randint(0,len(child))] = np.random.uniform(-1,1)


def mutation_singular(children, rate=0.001):
    """
    Mutate single index (element) in state if mutation probability = TRUE.
    """
    for child in children:
        if rate >= np.random.uniform(0,1):
            child[np.random.randint(0,len(child))] = np.random.uniform(-1,1)

def retainAndKeepBest(population, percent = 0.5):
    """
    Removes bad performers, crossovers and mutates best performers.
    Returns new population for the next gen.
    """
    population = sorted(population, key=lambda x: x.fitness, reverse=True) # Sort population based on best fitness.
    population = population[:(int(len(population)*percent))] # keep top 50%
    size = len(population)
    
    for i in range(0, size, 2):
        population[i].fitness = 0
        population[i+1].fitness = 0
        parent1_dna = population[i].state
        parent2_dna = population[i+1].state
        child1_dna, child2_dna = crossover(parent1_dna,parent2_dna)
        mutation_single(child1_dna)
        mutation_single(child2_dna)

        child1 = ANN(child1_dna)
        child2 = ANN(child2_dna)
        
        population.append(child1)
        population.append(child2)
    return population


def population_score(population):
    total_score = 0
    highest_score = population[0].fitness
    for child in population:
        total_score += child.fitness

    return highest_score, total_score/len(population)

def test_population(population):
    """
    Run a network for some element in the population.
    """
    for child in population:
        env.reset()
        observation, reward, done, _ = env.step(env.action_space.sample())
        done = False
        
        observation = np.concatenate([observation, [0]])

        while(not done):
            env.render()
            res = child.get_output(observation)
            observation, reward, done, _ = env.step(1 if res > 0 else 0)  
            observation = np.concatenate([observation, res])      
            child.fitness += reward




if __name__ == "__main__":
    """
    Start execution of ANN Evolution here:
    - Create environment
    - Create an initial population
    - Run through X generations
    - For each generation run through Y population
    - For each population calculate fitness and rank the population for generation Z based on high-low fitness
    - Also keep track of the average score for each generation
    - Use the data to generate some data frame for use in excel (save as .csv)
    - WHAT ELSE ?
    """

    population = [ANN(np.random.uniform(-1,1,29)) for _ in range(40)] # Initial population
    for gennum in range(1000):
        test_population(population)
        highest, avg = population_score(population)
        population = retainAndKeepBest(population)

        if gennum > 0:
            print("Gen {}: Average {}, Highest {}".format(gennum, avg, highest))




    env.close()