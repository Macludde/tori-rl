import commManager
import random

def setMuscles(muscleArray):
	data = "move:"
	if (len(muscleArray) < 22):
		for i in range(22-len(muscleArray)):
			muscleArray.append(0)
	for i in muscleArray:
		data += (str(i) + ",")
	data = data[:-1]
	commManager.writeComms(data)

def getData():
	return commManager.waitForInput()

def setRandomMuscles():
	moves = []
	for i in range(22):
		moves.append(random.randint(0, 3))
	setMuscles(moves)