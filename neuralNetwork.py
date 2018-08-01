import controller
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np

learning_rate = 0.95
y = 0.95
exploration_rate = 0.5
explorations_decay = 0.999
episodes = 10000
memory = []

def createModel(output):

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

def remember(state, action, reward, next_state, done):
	memory.append((state, action, reward, next_state, done))

def setup(): 
	model = createModel()
	global model

def turn():

	data = controller.getData()
	data = data[5:]
	dataPoints = [float(dataPoint) for dataPoint in data.split(",")]
	if (last_state != []):
		target = dataPoints[-1] + y * np.amax(model.predict(dataPoints[:-1]))




	"""
	y = 0.95
	eps = 0.5
	decay_factor = 0.999
	r_avg_list = []
	for i in range(num_episodes):
	    s = env.reset()
	    eps *= decay_factor
	    if i % 100 == 0:
	        print("Episode {} of {}".format(i + 1, num_episodes))
	    done = False
	    r_sum = 0
	    while not done:
	"""

train()