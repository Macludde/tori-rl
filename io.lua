CommsWrite = "commsPy.txt"
CommsRead = "commsLua.txt"

local function open_file(filename)
        local oldinput = io.input()
	io.input(filename)
	local file = io.input()
	io.input(oldinput)
	return file
     end

local function write_file(filename)
	local oldoutput = io.output()
	io.output(filename)
	local file = io.output()
	io.output(oldoutput)
	return file
     end

local function append_to_file(filename,string)
   local tmpInput = open_file(filename)
   local lines = {}
 end
 
 local function read_from_Py()
 	file = open_file(CommsRead)
	data = file:read("*l")
	file:close()
	file = write_file()
	file:write("")
	return data
end
 
 local function send_to_Py(vars)
 tmpFile = write_file(CommsWrite)
	 tmpFile:write(vars)
	 tmpFile:close()
	 echo("done")
end
int = 0
while true do
	int = int + 1
	send_to_Py(int)
	while true do
		temp = read_from_Py()
		if (temp ~= nil) then
			break
		end
	end
	if (int > 1000000) then 
		break
	end
end
	
	
	



