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
		self.gamma = 0.98
		self.exploration_rate = 0.1
		self.exploration_decay = 0.995#0.999955
		self.memories = [[]]
		self.sample_batch_size = 32
		self.totalRewards = []
		self.epochs = 0
		self.twoPlayers = True
		self.wins = [];
		self.disabled = [False, False];
		self.randomOpponent = True;

	def createModel(self, output):
		# Neural Net for Deep-Q learning Model
		model = Sequential()
		model.add(Dense(128, input_dim=132, activation="tanh"))
		model.add(Dropout(0.2))

		model.add(Dense(64, activation="tanh"))
		model.add(Dropout(0.2))

		model.add(Dense(16, activation="tanh"))
		model.add(Dropout(0.1))

		model.add(Dense(output, activation="linear"))

		model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
		return model

	def setup(self): 
		self.models = [self.createModel(88)]
		#self.model = load_model("model_weights.h5")
		self.models[0].load_weights("model_weights_only_0.h5")
		self.wins.append(0);
		if self.twoPlayers:
			self.wins.append(0);
			self.models.append(self.createModel(88))
			self.models[1].load_weights("model_weights_only_1.h5")
			self.memories.append([])

	def save_model(self):
		self.models[0].save_weights("model_weights_only_0.h5")
		if (self.twoPlayers and not self.disabled[1]):
			self.models[1].save_weights("model_weights_only_1.h5")

	def act(self, state, id):
		moves = []
		if (self.disabled[id] or np.random.rand() <= self.exploration_rate*0.1 + 0.05*id*0.1):
			if (not self.randomOpponent):
				moves = [2 for i in range(20)]
				moves.append(0)
				moves.append(0)
				return moves
			else:
				return [random.randint(0, 3) for i in range(22)]
		"""
		if np.random.rand() <= self.exploration_rate:
			for i in range(22):
				moves.append(random.randint(0, 3))
			return moves
		"""
		act_values = self.models[id].predict(state)[0]
		for i in range(22):
			if np.random.rand() <= self.exploration_rate + 0.05*id:
				moves.append(random.randint(0,3))
			else:
				moves.append(np.argmax(act_values[i:i+4])%4)

		return moves


	def remember(self, state, action, reward, next_state, done, player):
		if (not self.disabled[player]):
			self.memories[player].append((state, action, reward, next_state, done))


	def replay(self, sample_batch_size, id):
		if (self.disabled[id]):
			return;
		if len(self.memories[id]) < sample_batch_size:
			return
		big_differences = []
		sample_batch = random.sample(self.memories[id], sample_batch_size)
		for state, action, reward, next_state, done in sample_batch:
			target = reward + self.gamma * np.amax(self.models[id].predict(next_state)[0])
			target_f = self.models[id].predict(state)
			differences = []
			for i in range(len(action)-2):
				index = action[i]+i*4
				differences.append(abs(target_f[0][index] - target))
				target_f[0][index] = target
			big_differences.append(sum(differences) / float(len(differences)))
			self.models[id].fit(state, target_f, epochs=1, verbose=0)
		if self.exploration_rate > 0.1:
			self.exploration_rate *= self.exploration_decay
			#print(np.std(self.totalRewards))
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
		done = -1
		if data[:5] == "done:":
			oneWon = reward > 1000000
			reward = reward - 100000000*(oneWon*2-1) - 3000*(oneWon*2-1)
			done = 1 - oneWon
			self.totalRewards.insert(0, reward)
			if (len(self.totalRewards) > 20):
				self.totalRewards.pop()
			if (self.twoPlayers):
				self.wins[1-oneWon] += 1;
			else:
				self.wins[0] += oneWon;
		return (dataPoints, reward, done, player)

	def run(self):
		players = [
		{
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
				players[player]["action"] = self.act(players[player]["state"], player)
				controller.setMuscles(players[player]["action"])
				
				temp_state, temp_points, done, player = self.getData()
				players[player]["state"] = temp_state
				players[player]["points"] = temp_points

				turns = 0
				while done < 0:
					turns += 1
					players[player]["action"] = self.act(players[player]["state"], player)
					controller.setMuscles(players[player]["action"])

					temp_state, temp_points, done, player = self.getData()
					players[player]["next_state"] = temp_state
					players[player]["next_points"] = temp_points

					reward = (players[player]["next_points"] - players[player]["points"]) if done==-1 else 0

					self.remember(players[player]["state"], players[player]["action"], 
						reward + (done >= 0)*((done==player*2-1)*60000/turns), 
						players[player]["next_state"], done, player)

					if (done >= 0 and self.twoPlayers):
						players[1-player]["next_state"] = self.flipData(players[player]["state"])
						reward = -reward

						self.remember(players[1-player]["state"], players[1-player]["action"], 
							reward + (done==player*2-1)*60000/turns + turns*500, 
							players[1-player]["next_state"], done, 1-player)

						players[1-player]["state"] = players[1-player]["next_state"]
						players[1-player]["points"] = players[1-player]["next_points"]

					players[player]["state"] = players[player]["next_state"]
					players[player]["points"] = players[player]["next_points"]

				self.replay(self.sample_batch_size, 0)
				if (self.twoPlayers):
					self.replay(self.sample_batch_size, 1)
				self.save_model()
				self.epochs += 1

				if (self.epochs % 5 == 0):
					print("Wins: " + str(self.wins))
					print("Wins per epoch: {}".format(str(self.wins[0]/self.epochs)))
		finally:
			self.save_model()

	def flipData(self, input_data):
		data = input_data[0]
		data[:3] = data[3:6]
		data[3:6] = data[:3]
		data[6:9] = data[9:12]
		data[9:12] = data[6:9]
		data[12:72] = data[72:]
		data[72:] = data[12:72]
		return np.array([data])


agent = Agent()
agent.setup()
agent.run()

