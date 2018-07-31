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


readComms();
sleep(10000);
writeComms("move:3,2,1,0,2,0,3,1,0,1,1,2")
while True:
	line = readComms()
	if line != "":
		break;
writeComms("move:3,2,1,0,2,0,3,1,0,1,1,2")
while True:
	line = readComms()
	if line != "":
		break;
