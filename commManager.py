def readComms():
	commsPy = open("commsPy.txt","r+")
	line = commsPy.readline()
	if (line != ""):
		commsPy.truncate(0);
	commsPy.close()
	return line


def writeComms(data):
	commsLua = open("commsLua.txt", "w")
	commsLua.write(data) 
	commsLua.close()


def waitForInput():
	while True:
		data = readComms()
		if data != "":
			return data