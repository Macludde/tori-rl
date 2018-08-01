import controller
from keras.layers import Dense, Dropout

def sigmoid(x):
	return 1

def setupModels():
	models = []
	for i in range(20):
		models.append(createModel(4))
	models.append(createModel(2))
	models.append(createModel(2))

def createModel(output):
	model = Sequential()
	model.add(Dense(512, input_shape=(132,), activation="relu"))
	model.add(Dropout(0.3))

	model.add(Dense(1024, activation="relu"))
	model.add(Dropout(0.3))

	model.add(Dense(1024, activation="relu"))
	model.add(Dropout(0.3))

	model.add(Dense(512, activation="relu"))
	model.add(Dropout(0.3))

	model.add(Dense(128, activation="relu"))
	model.add(Dropout(0.3))
	model.add(Dense(output, activation="softmax"))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['mae'])

def train():
	controller.setRandomMuscles()
	data = controller.getData()
	data = data[5:]
	print(data)
	dataPoints = data.split(",")
	print(dataPoints)
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