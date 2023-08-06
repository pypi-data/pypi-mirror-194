from math import exp

class Neurone:
    def __init__(self, rate = 0.01):
        self.w11 = 0.0
        self.w22 = 0.0
        self.x11 = 0
        self.x22 = 0
        self.b = 0
        self.bw = 0
        self.rate = rate
        self.out = 0
        self.sumw = 0
    def sigmoid(self):
        self.out = (1 / (1 + exp(-self.sumw)))
    def wsum(self):
        self.sumw = b * wb + (x11 * w11 + x22 * w22)
    def grlearn(self):
        self.w11 += self.rate
        self.w22 += self.rate
    def lineal_error(self, pred):
        self.error = self.out - pred
    def train(self, inputs, preds, epochs = 300):
        self.x11 = inputs[0]
        self.x22 = inputs[1]
        for i in epochs:
            self.wsum()
            self.sigmoid()
            self.lineal_error()
            errors.append(self.error)
            if self.error == 0:
                break
            else:
                self.grlearn()
        return errors
    def use(self, inputs):
        self.x11 = inputs[0]
        self.x22 = inputs[1]
        self.wsum()
        self.sigmoid()
        return self.out
