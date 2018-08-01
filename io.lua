CommsWrite = "commsPy.txt"
CommsRead = "commsLua.txt"

local function append_to_file(filename,string)
   local tmpInput = open_file(filename)
   local lines = {}
 end
 
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