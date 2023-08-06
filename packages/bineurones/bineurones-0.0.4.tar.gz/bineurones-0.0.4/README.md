# Bineurone

![Bineurone](Bineurone.png)

|--------------------------------------------------------|
| A library to create artificial neurons with two inputs |
|--------------------------------------------------------|

# Requirements

  - Python3 or new

# Example of use
   from bineurone import Neurone
   
   predict = [0, 1, 0, 0]
   data = [[0, 1], [1, 1], [1, 0], [0, 0]]
   leraningrate = 0.01
   neu = Neurone(rate = learningrate)
   for d in len(data):
       error.append(neu.train(inputs = data[d], preds = pred[d], epochs = 1000))
   for t in error:
       print(t)
   output = neu.use()
   print(output)
