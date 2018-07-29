local function trim(s)
	return (string.gsub(s, "^%s*(.-)%s*$", "%1"))
end

local socket = require("socket")
local client = assert(socket.tcp())
local host, port = "172.16.0.127", 7051
--print("Client created")

client:connect(host, port);
--client:send("hello world\n");

local function getAction()
	inputen = {}
	local s, status, partial = client:receive()
	s = trim(s)
	for i = 1, #s do
		local c = s:sub(i, i)
		inputen[i] = tonumber(c)
	end
	--if status == "closed" then
		--break
	--end
end
client:close()

inputen = ({1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2})
playerID = 0
local function make_move(playID,valArr)
   jointVals = valArr
   echo("move")
   for i = 1,19 do
      set_joint_state(0, i, jointVals[i])
   end
   set_grip_info(playID, 11,jointVals[20])
   set_grip_info(playID, 12,jointVals[21])
   echo("endi")
end
local function get_players_moves()
	echo("look")
	jointsArr1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
	jointsArr2 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
	for i = 0,1 do
		for k = 1,19 do
			l = get_joint_info(i,k)
			echo (l)
		end
	end
end


local function make()
	echo("make")
	getAction()
	make_move(playerID,inputen)
	get_players_moves()
end


add_hook("enter_freeze"," j",make)
