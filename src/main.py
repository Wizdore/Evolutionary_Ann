import gym
import numpy as np
import matplotlib.pyplot as plt

ENV = gym.make('CartPole-v0')

class ResultGraph:
    """
    Shows a graph at the end of execution depicting how the generations have evolved.
    """

    def __init__(self):
        self.x = []
        self.y = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)

    def plot(self):
        self.ax.clear()
        self.ax.plot(self.x, self.y)
        plt.show()

GRAPH = ResultGraph()

class ANN:
    def __init__(self, state):
        self.state = state                      # 29 size vector that holds weights and biases of whole network
        self.activation = lambda x: (2/(1+ np.exp(-0.5*x)))-1   # Slightly modified tanh Activation Function that should work better in our case
        self.fitness = 0
    
    def set_hl_activation(self, activation):        # Optional function change the activation function
        self.activation = activation

    def get_output(self, inputs):
        hl_weight = self.state[0:16].reshape(4,4)       # First 20 elements are weights for input to hidden layer edges
        hl_bias = self.state[16:20]                     # Next 4 elements are for 4 nodes of hidden layer
        ol_weight = self.state[20:24].reshape(4,1)      # Next 4 elements are for 4 weights for hidden to output edges 
        #ol_bias = self.state[-1]                     # Next 1 element is the bias of the output layer

        inputs = self.activation(inputs)                # Normalizing the input values

        hl_result = (np.matmul(inputs, hl_weight) + hl_bias)        # calc from input to hidden layer (is linear activation good enough?!)
        ol_result = (np.matmul(hl_result, ol_weight))     # calc from Hidden to output layer

        return ol_result        # returning raw result of the network

def crossover(parent1, parent2, crossSize=4):
    """
    Parent1 and Parent2 are 2 states from 2 networks.
    The two parents are chosen from the top performers in the generation.
    Returns a tuple containing child 1 and child 2 which has mixed values from parent 1 and 2.
    """
    pivotMin = np.random.randint(0, len(parent1) - crossSize)
    pivotMax = pivotMin + crossSize

    # Create children.
    child1 = parent1
    child2 = parent2
    # Crossover data.
    child1[pivotMin:pivotMax] = parent2[pivotMin:pivotMax]
    child2[pivotMin:pivotMax] = parent1[pivotMin:pivotMax]
    
    return child1, child2

def mutate_all(state, rate=0.0025):
    """
    Go through each element in the state and check if that element should be mutated with
    probability 'rate'.
    """
    m = np.random.uniform(0.0,1.0,size=len(state))
    for idx, _ in enumerate(state):
        if rate >= m[idx]:
            state[idx] = np.random.uniform(-1,1)

def mutation_single(state, rate=0.0025):
    """
    Mutate single index (element) in state if mutation probability = TRUE.
    """
    if rate >= np.random.uniform(0,1):
        state[np.random.randint(0,len(state))] = np.random.uniform(-1,1)

def retainAndKeepBest(population, percent=0.5):
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
        
        population.extend([child1, child2])
    return population

def population_score(population):
    total_score = 0
    highest_score = max(population, key=lambda x: x.fitness).fitness
    for child in population:
        total_score += child.fitness

    return highest_score, (total_score/len(population))

def test_population(population):
    """
    Run a network for some element in the population.
    """
    prevActions = np.arange(5) # Store last 5 actions for sanity check suggestion.
    iteration = 0 # Keep track of the number of iterations.
    for child in population:        
        ENV.reset()
        observation = ENV.observation_space.sample() # random inputs
        done = False
        while(not done):
            ENV.render()
            action = (1 if child.get_output(observation) >= 0 else 0)
            if len(set(prevActions)) == 1: # All actions are the same, use opposite action.
                action = (1 if prevActions[0] <= 0 else 0)
            observation, reward, done, _ = ENV.step(action)        
            child.fitness += reward
            prevActions[iteration % len(prevActions)] = action
            iteration += 1
            
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
    population = [ANN(np.random.uniform(-1,1,24)) for _ in range(60)] # Initial population
    for gennum in range(15):
        test_population(population)
        highest, avg = population_score(population)
        population = retainAndKeepBest(population)

        GRAPH.x.append(gennum+1)
        GRAPH.y.append(avg)

        print("Gen {}:\t\tAverage {:.3f},\t\tHighest {}".format(gennum+1, avg, highest))

    ENV.close()
    GRAPH.plot()