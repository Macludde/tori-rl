local function append_to_file(filename,string)
   local tmpInput = open_file(filename)
   local lines = {}
 end

 
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
