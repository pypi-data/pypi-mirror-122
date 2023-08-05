from math import exp


class Neuron:
    """A neuron should act as the neurons in a human brain, to calculate the synapse and input weights and feed_forward"""

    def __init__(self, bias, weights = []):
        """Neurons calculate output and besed on weight and bias. The output of each neuron will dictate the prediction.

        Args:
            _bias (float): Bias allows you to shift the activation function by adding a constant.
            _weight (float): The connecting weight of the synapse.
        """
        self.bias = bias
        self.weights = weights
        self.output = None

    def calculate_output(self, input):
        """Calculates the output of the node, given the input.

        Args:
            input (numeric): The input value or the output of the previous node layer.

        Returns:
            float: The output of the node, given the input.
        """
        self.input = input

        if len(self.weights) == 0:
            return self.input

        self.simoid()
        return self.output

    def simoid(self):
        """[summary]

        Args:
            _input ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.output = 1.0 / (1.0 + exp(-self.dot_product()))

    def sigmoid_derivative(self):
        """The derivative function of sigmoid

        Returns:
            [type]: [description]
        """
        return 1
    
    def dot_product(self):
        """
        Multiply the inputs by the synaptic weights + bias.
        """
        total = 0.0
        for i in range(len(self.input)):
            total += self.input[i] * self.weights[i]
        return total + self.bias
    
    def calculate_pd_error_wrt_total_net_input(self, target_output):
        return self.calculate_pd_error_wrt_output(target_output) * self.calculate_pd_total_net_input_wrt_input()

    def calculate_pd_error_wrt_output(self, target_output):
        return -(target_output - self.output)

    def calculate_pd_total_net_input_wrt_input(self):
        return self.output * (1 - self.output)

    def calculate_pd_total_net_input_wrt_weight(self, index):
        return self.input[index]

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights

    def inspect(self):
        print("\t\tbias: ", self.bias)
        print("\t\tweights: ", self.weights)