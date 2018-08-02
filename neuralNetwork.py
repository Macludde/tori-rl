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
		#self.model.load_weights("model_weights_only.h5")

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
		print("Average difference: " + str(sum(differences) / float(len(differences))))
		print(np.std(self.totalRewards))
		"""
		if (self.epochs % 20 == 0):
			plt.plot(self.totalRewards)
			plt.ylabel('Total Reward')
			plt.show()
		"""


	def getData(self):
		data = controller.getData()
		if data[:5] == "done:":
			doneState = np.array([[-1]])
			finalReward =math.floor(float(data[5:]))
			print("Final reward: " + str(finalReward))
			self.totalRewards.insert(0, finalReward)
			if (len(self.totalRewards) > 20):
				self.totalRewards.pop()
			return (doneState,finalReward)
		data = data[5:]
		dataPoints = np.array([[float(dataPoint) for dataPoint in data.split(",")][:-1]])
		reward = float(data.split(",")[-1])
		return (dataPoints, reward)

	def run(self):
		try:
			while True:
				state, points = self.getData()

				done = False
				index = 0
				while not done:
					action = self.act(state)
					controller.setMuscles(action)
					next_state, next_points = self.getData()
					reward = next_points - points
					done = next_state.shape[1] == 1
					if (done):
						break
					reward = -reward
					self.remember(state, action, reward, next_state, done)
					state = next_state
					points = next_points
					index += 1
				self.replay(self.sample_batch_size)
				self.save_model()
				self.epochs += 1
		finally:
			self.save_model()


agent = Agent()
agent.setup()
agent.run()

