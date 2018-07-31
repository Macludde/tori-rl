def readComms():
	commsPy = open("commsPy.txt","r+")
	line = commsPy.readline()
	print(line)
	# Process Line
	commsPy.truncate(0);
	commsPy.close()
	return line


def writeComms(data):
	commsLua = open("commsLua.txt", "a")
	commsLua.write(data) 
	commsLua.close()


