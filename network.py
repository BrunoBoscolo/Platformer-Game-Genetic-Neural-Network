import numpy as np

# Define sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Parameters:
    def __init__(self, input_weights, input_biases, hidden_weights, hidden_biases, output_weights, output_biases):
        self.input_weights = input_weights
        self.input_biases = input_biases
        self.hidden_weights = hidden_weights
        self.hidden_biases = hidden_biases
        self.output_weights = output_weights
        self.output_biases = output_biases

    @staticmethod
    def glorot_uniform(shape):
        # Glorot initialization for weights
        limit = np.sqrt(6.0 / (shape[0] + shape[1]))
        return np.random.uniform(-limit, limit, shape)

    @staticmethod
    def glorot_normal(shape):
        # Glorot initialization for biases
        stddev = np.sqrt(2.0 / (shape[0] + shape[1]))
        return np.random.normal(0, stddev, shape)

    @staticmethod
    def create_parameters():
        # Generate weights and biases using Glorot initialization
        input_weights = Parameters.glorot_uniform((4, 4))
        input_biases = Parameters.glorot_normal((4,))
        hidden_weights = Parameters.glorot_uniform((4, 4))
        hidden_biases = Parameters.glorot_normal((4,))
        output_weights = Parameters.glorot_uniform((4, 2))
        output_biases = Parameters.glorot_normal((2,))

        return Parameters(input_weights, input_biases, hidden_weights, hidden_biases, output_weights, output_biases)

    def mutate(self, mutation_rate, mutation_chance):
        def apply_mutation(array):
            for i in np.ndindex(array.shape):
                if np.random.rand() < mutation_chance:
                    array[i] += np.random.randn() * mutation_rate

        apply_mutation(self.input_weights)
        apply_mutation(self.input_biases)
        apply_mutation(self.hidden_weights)
        apply_mutation(self.hidden_biases)
        apply_mutation(self.output_weights)
        apply_mutation(self.output_biases)

    @staticmethod
    def extract_parameters(neural_network):
        return Parameters(neural_network.input_weights, neural_network.input_biases,
                          neural_network.hidden_weights, neural_network.hidden_biases,
                          neural_network.output_weights, neural_network.output_biases)


    def mutate_parameters(network, mutation_rate, mutation_chance):
        extracted_parameters = Parameters.extract_parameters(network)
        Parameters.mutate(extracted_parameters, mutation_rate, mutation_chance)
        return extracted_parameters
    
# Define neural network class
class RandomNeuralNetwork:
    def __init__(self):
        # Initialize random weights and biases for input layer, hidden layer, and output layer
        self.input_weights = np.random.randn(4, 4)  # Random weights for 4 inputs to 4 neurons in hidden layer
        self.input_biases = np.random.randn(4)  # Random biases for 4 neurons in hidden layer
        self.hidden_weights = np.random.randn(4, 4)  # Random weights for 4 neurons in hidden layer to 4 neurons in another hidden layer
        self.hidden_biases = np.random.randn(4)  # Random biases for 4 neurons in another hidden layer
        self.output_weights = np.random.randn(4, 2)  # Random weights for 4 neurons in hidden layer to 2 neurons in output layer
        self.output_biases = np.random.randn(2)  # Random biases for 2 neurons in output layer

    def forward(self, inputs):
        # Forward pass through the network
        hidden_layer_output = np.maximum(0, np.dot(inputs, self.input_weights) + self.input_biases)
        another_hidden_layer_output = np.maximum(0, np.dot(hidden_layer_output, self.hidden_weights) + self.hidden_biases)
        output = np.dot(another_hidden_layer_output, self.output_weights) + self.output_biases
        return list(output)

    
    def createInitialGeneration():
        # Generate 50 neural networks
        neural_networks = [RandomNeuralNetwork() for _ in range(50)]
        return neural_networks

    def computeInputFirstGeneration(neural_networks, input_list):
        # Define input list
        #input_list = [1, 2, 3, 4]  # Example input list [x1, y1, x2, y2]

        # Forward pass through each neural network for the same input list
        output_values = []
        for neural_network in neural_networks:
            values = neural_network.forward(input_list)
            output_values.append(values)
            #print(values)

class CustomNeuralNetwork:
    def __init__(self, parameters):
        # Set weights and biases provided as input
        self.input_weights = parameters.input_weights
        self.input_biases = parameters.input_biases
        self.hidden_weights = parameters.hidden_weights
        self.hidden_biases = parameters.hidden_biases
        self.output_weights = parameters.output_weights
        self.output_biases = parameters.output_biases

    def forward(self, inputs):
        # Forward pass through the network
        hidden_layer_output = sigmoid(np.dot(inputs, self.input_weights) + self.input_biases)
        another_hidden_layer_output = sigmoid(np.dot(hidden_layer_output, self.hidden_weights) + self.hidden_biases)
        output = np.dot(another_hidden_layer_output, self.output_weights) + self.output_biases
        return output
    

class Evolution:

    @staticmethod
    def select_top_half(networks_fitness):
        # Sort networks based on fitness (higher fitness values are better)
        sorted_networks = sorted(networks_fitness, key=lambda x: x[1], reverse=True)
        # Select the top half of networks
        top_half = sorted_networks[:len(sorted_networks)//2]
        return top_half

class genetics:
    def create_network_array(custom_network, fitness, generation_array:list):
        customNetworkArray = [custom_network, fitness]
        generation_array.append(customNetworkArray)

    def mutate_network_parameters(generation_array):
        mutate_custom_network_array = []
        for network, fitness in generation_array:
            mutated_parameters = Parameters.mutate_parameters(network, 0.1, 0.5)
            custom_network_mutated = CustomNeuralNetwork(mutated_parameters)
            mutate_custom_network_array.append(custom_network_mutated)
        return mutate_custom_network_array

class debugging:
    def print_network_parameters(network):
        print("Input Weights:\n", network.input_weights)
        print("Input Biases:\n", network.input_biases)
        print("Hidden Weights:\n", network.hidden_weights)
        print("Hidden Biases:\n", network.hidden_biases)
        print("Output Weights:\n", network.output_weights)
        print("Output Biases:\n", network.output_biases)

