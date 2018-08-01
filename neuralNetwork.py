import controller
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np
import random

class Agent():
	def __init__(self):
		self.learning_rate = 0.95
		self.y = 0.95
		self.exploration_rate = 0.5
		self.explorations_decay = 0.999
		self.episodes = 10000
		self.memory = []

	def createModel(self, output):
	    # Neural Net for Deep-Q learning Model
		model = Sequential()
		model.add(Dense(512, input_dim=132, activation="relu"))
		model.add(Dropout(0.3))

		model.add(Dense(1024, activation="relu"))
		model.add(Dropout(0.3))

		model.add(Dense(2048, activation="relu"))
		model.add(Dropout(0.3))

		model.add(Dense(1024, activation="relu"))
		model.add(Dropout(0.3))

		model.add(Dense(512, activation="relu"))
		model.add(Dropout(0.3))
		model.add(Dense(output, activation="sigmoid"))

		model.compile(loss='mse', optimizer='adam', metrics=['mae'])
		return model

	def remember(self, state, action, reward, next_state, done):
		memory.append((state, action, reward, next_state, done))

	def setup(self): 
		self.model = self.createModel(88)

	def act(self, state):
		moves = []
		if np.random.rand() <= self.exploration_rate:
			for i in range(22):
				moves.append(random.randint(0, 3))
			return moves
		act_values = self.model.predict(state)[0]
		for i in range(22):
			moves.append(np.argmax(act_values[i:i+4])%4)

		return moves



	def turn(self):

		data = controller.getData()
		data = data[5:]
		dataPoints = [float(dataPoint) for dataPoint in data.split(",")]
		if (self.last_state != []):
			target = dataPoints[-1] + y * np.amax(model.predict(dataPoints[:-1]))
	def predict(self):
		controller.setRandomMuscles()
		data = controller.getData()
		data = data[5:]
		dataPoints = np.array([[float(dataPoint) for dataPoint in data.split(",")]])
		print(self.act(dataPoints))



class NeuralNet():
	def __init__(self):
		pass

agent = Agent()
agent.setup()
agent.predict()

