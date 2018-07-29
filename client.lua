-- load namespace
local socket = require("socket")
-- create a TCP client socket
local client = assert(socket.tcp())
-- find out which port the OS chose for us
local host, port = "localhost", 7051
print("Client created")


client:connect(host, port);
client:send("hello world\naaa\n");


while true do
    local s, status, partial = client:receive()
    print(s or partial)
    if status == "closed" then break end
end
client:close()