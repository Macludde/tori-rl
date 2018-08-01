

inputen = ({4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3})
playerID = 0
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
local function next_turn()
	step_game()
end
local function next_game()
	start_new_game()
end	

local function make_move(playID,valArr)
   jointVals = valArr
   for i = 1,21 do
      set_joint_state(0, i-1, jointVals[i])
   end
   set_grip_info(playID, 11,jointVals[20])
   set_grip_info(playID, 12,jointVals[21])
end
local function get_players_moves()
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
	return ("data:" ..array)
end
	

local function execute_turn()
	make_move(playerID,inputen)
	values = Get_State()
	writeComms(values)
	
	next_turn()
end




add_hook("enter_freeze"," j",execute_turn)
	
	
	


