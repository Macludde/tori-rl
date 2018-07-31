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
 	tmpFileRead = open_file(CommsRead)
	vars = tmpFileRead:read("*l")

	return vars
end
 
 local function send_to_Py(vars)
 tmpFile = write_file(CommsWrite)
	 tmpFile:write(vars)
	 tmpFile:close()
	 echo("done")
end



