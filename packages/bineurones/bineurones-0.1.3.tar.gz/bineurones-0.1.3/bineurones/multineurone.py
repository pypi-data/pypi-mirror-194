from math import exp

class Multineurone:
    def __init__(self, numinputs, rate=0.1):
        self.weights = [-1] * numinputs
        self.rate = rate
        self.ninputs = numinputs
        self.b = 1
        self.wb = -1
        self.error = 0
        self.sumw = 0
        self.out = 0

    def sigmoid(self):
        self.out = 1 / (1 + exp(-self.sumw))
        self.sumw = 0

    def wsum(self, inputs):
        self.sumw += self.b * self.wb
        for i in range(self.ninputs):
            self.sumw += self.weights[i] * inputs[i]

    def lineal_error(self, pred):
        self.error = self.out - pred

    def grlearn(self, inputs):
        self.wb -= self.rate * self.error * self.b
        for i in range(self.ninputs):
            self.weights[i] -= self.rate * self.error * inputs[i]

    def train(self, inputs, pred, epochs=300):
        errors = []
        for i in range(epochs):
            self.wsum(inputs)
            self.sigmoid()
            self.lineal_error(pred)
            errors.append(self.error)
            if self.error == 0:
                break
            else:
                self.grlearn(inputs)
        return errors

    def use(self, inputs):
        self.wsum(inputs)
        self.sigmoid()
        return self.out

