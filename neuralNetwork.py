import controller
from keras.layers import Dense, Dropout
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class Agent():
	def __init__(self):
		self.learning_rate = 0.001
		self.gamma = 0.95
		self.exploration_rate = 0.5
		self.exploration_decay = 0.999
		self.memory = []
		self.sample_batch_size = 32
		self.totalRewards = []
		self.epochs = 1
		self.twoPlayers = True

	def createModel(self, output):
		# Neural Net for Deep-Q learning Model
		model = Sequential()
		model.add(Dense(128, input_dim=132, activation="relu"))
		model.add(Dropout(0.2))

		model.add(Dense(128, activation="relu"))
		model.add(Dropout(0.2))

		model.add(Dense(32, activation="relu"))
		model.add(Dropout(0.2))

		model.add(Dense(output, activation="linear"))

		model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
		return model

	def setup(self): 
		self.model = self.createModel(88)
		#self.model = load_model("model_weights.h5")
		self.model.load_weights("model_weights_only.h5")

	def save_model(self):
		self.model.save_weights("model_weights_only.h5")

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


	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))


	def replay(self, sample_batch_size):
		if len(self.memory) < sample_batch_size:
			return
		big_differences = []
		sample_batch = random.sample(self.memory, sample_batch_size)
		for state, action, reward, next_state, done in sample_batch:
			target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
			target_f = self.model.predict(state)
			differences = []
			for i in range(len(action)-2):
				index = action[i]+i*4
				differences.append(abs(target_f[0][index] - target))
				target_f[0][index] = target
			big_differences.append(sum(differences) / float(len(differences)))
			self.model.fit(state, target_f, epochs=1, verbose=0)
		if self.exploration_rate > 0.03:
			self.exploration_rate *= self.exploration_decay

		if (self.epochs % 5 == 0):
			print(np.std(self.totalRewards))
		"""
			plt.plot(self.totalRewards)
			plt.ylabel('Total Reward')
			plt.show()
		"""


	def getData(self):
		data = controller.getData()
		dataPoints = np.array([[float(dataPoint) for dataPoint in data[5:].split(",")][1:-1]])
		reward = math.floor(float(data[5:].split(",")[-1]))
		player = int(data[5])

		if data[:5] == "done:":
			turns = math.floor(reward/10000000)
			reward = reward % 10000000 + turns*1000
			self.totalRewards.insert(0, reward)
			if (len(self.totalRewards) > 20):
				self.totalRewards.pop()

		return (dataPoints, reward, (data[1:5] == "done:"), player)

	def run(self):
		players = [{
			"state": 0,
			"points": 0,
			"next_state": 0,
			"next_points": 0,
			"action": []
		}, 
		{
			"state": 0,
			"points": 0,
			"next_state": 0,
			"next_points": 0,
			"action": []
		}]

		try:
			while True:
				temp_state, temp_points, done, player = self.getData()
				players[player]["state"] = temp_state
				players[player]["points"] = temp_points

				players[player]["action"] = self.act(players[player]["state"])
				controller.setMuscles(players[player]["action"])
				temp_state, temp_points, done, player = self.getData()
				players[player]["state"] = temp_state
				players[player]["points"] = temp_points

				index = 0
				while not done:
					players[player]["action"] = self.act(players[player]["state"])
					controller.setMuscles(players[player]["action"])
					temp_state, temp_points, done, player = self.getData()
					players[player]["next_state"] = temp_state
					players[player]["next_points"] = temp_points
					reward = players[player]["next_points"] - players[player]["points"]

					self.remember(players[player]["state"], players[player]["action"], reward, players[player]["next_state"], done)

					if (done and self.twoPlayers):
						players[1-player]["next_state"] = self.flipData(players[players]["state"])
						reward = -reward
						self.remember(players[1-player]["state"], players[1-player]["action"], reward, players[1-player]["next_state"], done)
						players[1-player]["state"] = players[1-player]["next_state"]
						players[1-player]["points"] = players[1-player]["next_points"]

					players[player]["state"] = players[player]["next_state"]
					players[player]["points"] = players[player]["next_points"]
					index += 1

				self.replay(self.sample_batch_size)
				self.save_model()
				self.epochs += 1
		finally:
			self.save_model()

	def flipData(self, data):
		print(data)
		data[:3] = data[3:6]
		data[3:6] = data[:3]
		data[6:9] = data[9:12]
		data[9:12] = data[6:9]
		data[12:72] = data[72:]
		data[72:] = data[12:72]
		print(data)
		return data


agent = Agent()
agent.setup()
agent.run()

