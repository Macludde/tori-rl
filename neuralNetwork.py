class NeuralNetwork:
    def __init__(self):
        pass

    def generateAction(self, data):
        return [x % 4 for x in range(20)]
