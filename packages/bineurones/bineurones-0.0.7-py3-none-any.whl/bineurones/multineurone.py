class MultiNeurone:
    def __init__(self, rate=0.01, numinputs):
        self.weights = [-1] * numinputs
        self.rate = rate
        self.ninputs = numinputs
        self.b = 1
        self.wb = -1
        self.error = 0
        self.sumw = 0
        self.out = 0
    def sigmoid(self):
        self.out = 1 / (1 + exp(-self.sumw)))
        self.sumw = 0
    def wsum(self):
        self.sumw += self.b * self.wb
        for i in range(self.ninputs):
            self.sumw += self.weight[i] * inputs[i]
    def lineal_error(self, pred):
        self.error = self.out - pred
    def grlearn(self):
        self.wb += self.rate
        for i in range(self.ninputs):
            self.weights[i] += self.rate
    def train(self, inputs, pred, epochs = 300):
        errors = []
        for i in range(epochs):
            self.wsum()
            self.sigmoid()
            self.lineal_error(pred)
            errors += self.error
            if self.error == 0:
                break
            else:
                self.grlearn()
        return errors
    def use(self):
        self.wsum()
        self.sigmoid()
        return self.out
