function trim(s)
	return (string.gsub(s, "^%s*(.-)%s*$", "%1"))
end

local socket = require("socket")
local client = assert(socket.tcp())
local host, port = "172.16.0.127", 7051
print("Client created")

client:connect(host, port);
client:send("hello world\n");

while true do
	local s, status, partial = client:receive()
	s = trim(s)
	local moves = {}
	for i = 1, #s do
		local c = s:sub(i, i)
		moves[i] = tonumber(c)
	end
	if status == "closed" then
		break
	end
end
client:close()
