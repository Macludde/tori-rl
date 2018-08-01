<<<<<<< HEAD
CommsWrite = "commsPy.txt"
CommsRead = "commsLua.txt"

=======
>>>>>>> 4af3802a25a63f79270b1dae6ca4dbbaa8ff7984
local function append_to_file(filename,string)
   local tmpInput = open_file(filename)
   local lines = {}
 end
<<<<<<< HEAD
 
 local function read_from_Py()
 	file = io.open(CommsRead, "r+")	
 	io.input(file)
 	data = io.read("*l")

	io.output(file)
	io.write("")
	io.close(file)

	return data
end
 
 local function send_to_Py(data)
 	file = io.open(CommsWrite, "w")	
	io.output(file)
	io.write(data)
	io.close(file)
end


send_to_Py("Test")
echo(read_from_Py())
echo(read_from_Py())
echo(read_from_Py())
=======

 
local function readComms()
 	file = io.open("commsLua.txt", "r")
 	data = file:read()
	file:close()
 	file = io.open("commsLua.txt", "w")
 	file:write("")
 	file:close()

 	return data
end
 
local function writeComms(data)
	file = io.open("commsPy.txt", "w")	
	file:write(data)
	file:close()
end


writeComms("Data27")
echo(readComms())
echo(readComms())
>>>>>>> 4af3802a25a63f79270b1dae6ca4dbbaa8ff7984
