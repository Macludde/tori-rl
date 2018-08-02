input = ({4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3})
playerID = 0

local function split(source, delimiters)
        local elements = {}
        local pattern = '([^'..delimiters..']+)'
        string.gsub(source, pattern, function(value) elements[#elements + 1] =     value;  end);
        return elements
end

local function readComms()
 	file = io.open("commsLua.txt", "r")
 	data = file:read()
	file:close()
	if (data ~= nil) then
	 	file = io.open("commsLua.txt", "w")
	 	file:write("")
	 	file:close()
	 end

 	return data
end
 
local function writeComms(data)
	file = io.open("commsPy.txt", "w")	
	file:write(data)
	file:close()
end

local function next_turn()
	step_game()
end

local function next_game()

	win = get_world_state().winner
	extraPoints = 0
	if win~=-1 then
		extraPoints = 1000000 * ((playerID == win) and 1 or -1)
	end
	values = Get_State()
	writeComms("done:"..values..","..(get_player_info(1-playerID).injury-get_player_info(playerID).injury + extraPoints))
	start_new_game()
end
	

local function make_move(playerID,jointVals)
   for i = 1,21 do
      set_joint_state(playerID, i-1, jointVals[i])
   end
   --set_grip_info(playerID, 11,jointVals[21])
   --set_grip_info(playerID, 12,jointVals[22])
end
local function get_players_moves()
	echo("look")
	jointsArr1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
	jointsArr2 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
	array = {}
	for i = 0,1 do
		for k = 0,19 do
			l = get_joint_info(i,k)
			
			table.insert(array,l)
			
		end
	end
	
	return array
end
local function Get_State()
	array  = {}
	for i = 0,1 do
		local varx,vary,varz = get_body_angular_vel(i,0)
	
		table.insert(array,varx)
		table.insert(array,vary)
		table.insert(array,varz)
	end
		for i = 0,1 do
		local varx,vary,varz = get_body_linear_vel(i,0)
	
		table.insert(array,varx)
		table.insert(array,vary)
		table.insert(array,varz)
	end
	for i = 0,1 do
		for o = 0,19 do
			local varx,vary,varz = get_joint_pos(i,o)
	
			table.insert(array,varx)
			table.insert(array,vary)
			table.insert(array,varz)
		end
	end
	
	array = table.concat(array,",")
	return (array)
end



local function processInput(input)
	substring = string.sub(input, 1, 4)
	data = string.sub(input, 6)
	if (substring == "move") then
		moves = {}
		for match in string.gmatch(data, "[^,]+") do
			table.insert(moves, tonumber(match)+1)
		end
		make_move(playerID, moves)
	else
		echo(data)
	end
end

local function waitForInput()
	while true do
		data = readComms()
		if (data ~= nil) then
			processInput(data)
			break
		end
	end
end
	

local function execute_turn()
	values = Get_State()
	table.insert(values, get_player_info(1-playerID).injury)
	writeComms("data:"..values)

	waitForInput()
	
	next_turn()
end




add_hook("enter_freeze"," j",execute_turn)
add_hook("end_game", "start_new_game", next_game)
add_hook("new_game", "start", execute_turn)