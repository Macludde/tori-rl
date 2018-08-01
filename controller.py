import commManager


def setMuscles(muscleArray):
	data = "move:"
	if (len(muscleArray) < 22):
		for i in range(22-len(muscleArray)):
			muscleArray.append(0)
	for i in muscleArray:
		data += (str(i) + ",")
	data = data[:-1]
	commManager.writeComms(data)

setMuscles([0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2])