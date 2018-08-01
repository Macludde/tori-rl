import controller
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np

class AI():
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
	    model.add(Dense(24, input_dim=self.state_size, activation='relu'))
	    model.add(Dense(24, activation='relu'))
	    model.add(Dense(self.action_size, activation='linear'))
	    model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
		model = Sequential()
		model.add(Dense(512, input_shape=(132,), activation="relu"))
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
		self.model = createModel()

	def turn(self):

		data = controller.getData()
		data = data[5:]
		dataPoints = [float(dataPoint) for dataPoint in data.split(",")]
		if (self.last_state != []):
			target = dataPoints[-1] + y * np.amax(model.predict(dataPoints[:-1]))

