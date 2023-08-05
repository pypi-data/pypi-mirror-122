from .Neuron import Neuron
from numpy import random as nprand

class Layer:
    def __init__(self, _amtNeurons, amt_input_synapses, _bias, _nextLayer=None, isInputLayer=False):
        """Defines the Neuron layer, which could be a hidden, input or output layer of many neurons.

        Args:
            _amtNeurons (integer): Amount of neurons in the neuron layer.
            _bias (float): Bias allows you to shift the activation function by adding a constant
            _nextLayer (Layer): The next layer in the network.
        """
        self.isInputLayer = isInputLayer
        self.bias = _bias
        self.amt_input_synapses = amt_input_synapses
        self.nextLayer = _nextLayer
        for count in range(_amtNeurons):
            self.neurons = [Neuron(_bias, []) for k in range(_amtNeurons)]
        self.initialise_neuron_weights()

    def initialise_neuron_weights(self):
        """Initializes the synapse weights for each neurons entry,
        """
        for neuron in self.neurons:
            neuron.set_weights(nprand.rand(self.amt_input_synapses))


    def feed_forward(self, _inputs):
        """
        calculate inputs of all neurons in the layer and pass to next layer
        """
        output = []
        if self.isInputLayer:
            self.nextLayer.feed_forward(_inputs)
        else:
            for neuron in self.neurons:
                output.append(neuron.calculate_output(_inputs))
            if self.nextLayer:
                self.nextLayer.feed_forward(output)
            else:
                print("output: ", output)


    def inspect(self):
        print("\tBIAS: ", self.bias)
        for neuron in self.neurons:
            neuron.inspect()