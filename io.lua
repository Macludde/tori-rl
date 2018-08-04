input = ({4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3})
mainPlayerID = 0
oppponentID = 1
twoPlayers = true
turns = 0

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


local function Get_State(playerID)
	array  = {}
	table.insert(array, playerID)
	for i = 0,1 do
		local varx,vary,varz = get_body_angular_vel((i+playerID)%2,0	)
	
		table.insert(array,varx*50)
		table.insert(array,vary*50)
		table.insert(array,varz*50)
	end
		for i = 0,1 do
		local varx,vary,varz = get_body_linear_vel((i+playerID)%2, 0)
	
		table.insert(array,varx*50)
		table.insert(array,vary*50)
		table.insert(array,varz*50)
	end
	for i = 0,1 do
		for o = 0,19 do
			local varx,vary,varz = get_joint_pos((i+playerID)%2,o)
	
			table.insert(array,varx*50)
			table.insert(array,vary*50)
			table.insert(array,varz*50)
		end
	end
	table.insert(array, get_player_info(1-playerID).injury)
	
	return (array)
end

local function next_turn()
	turns = turns + 1
	step_game()
end

local function next_game()
	win = get_world_state().winner

	winPoints = 0
	if win~=-1 then
		winPoints = 100000000 * ((mainPlayerID == win) and 1 or -1)
		if (mainPlayerID == win and not twoPlayers) then
			echo("Player Won")
		end
	end
	values = Get_State(mainPlayerID)
	values[table.getn(values)] = get_player_info(1-mainPlayerID).injury - get_player_info(mainPlayerID).injury + winPoints
	array = table.concat(values,",")
	writeComms("done:"..array)

	turns = 0
	start_new_game()
end
	

local function make_move(playerID,jointVals)
	for i = 1,21 do
		if (jointVals[i] ~= 0) then
      		set_joint_state(playerID, i-1, jointVals[i])
  		end
	end
	if (jointVals[21] ~= 0) then
		if (jointVals[21] > 2) then
			set_grip_info(playerID, 11,1)
		else 
			set_grip_info(playerID, 11,0.5)
		end
	end
	if (jointVals[22] ~= 0) then
		if (jointVals[22] > 2) then
			set_grip_info(playerID, 12,1)
		else 
			set_grip_info(playerID, 12,0.5)
		end
	end
end



local function processInput(playerID, input)
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

local function waitForInput(playerID)
	while true do
		data = readComms()
		if (data ~= nil) then
			processInput(playerID, data)
			break
		end
	end
end
	

local function execute_turn()
	values = Get_State(mainPlayerID)
	opponentValues = Get_State(oppponentID)
	array = table.concat(values,",")
	opponentArray = table.concat(opponentValues,",")
	writeComms("data:"..array)
	waitForInput(mainPlayerID)
	if (twoPlayers) then
		writeComms("data:"..opponentArray)
		waitForInput(oppponentID)
	end

	
	next_turn()
end




add_hook("enter_freeze"," j",execute_turn)
add_hook("end_game", "start_new_game", next_game)
add_hook("new_game", "start", execute_turn)