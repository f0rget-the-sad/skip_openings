--[[
	Simple script to display the end-time for the current file.
	Example input.conf bind:
	E script-message display-eta
]]--
local utils = require("mp.utils")

local BINDING_NAME = 'skip-intro'

start_ts = nil
end_ts   = nil

function skip_intro()
	res = mp.set_property("playback-time", end_ts)
	if res ~= true then
		print(res)
	end
	mp.remove_key_binding(BINDING_NAME)
end

function init(event)
	local filename  = mp.get_property_native("filename")
	print("F IS " .. filename)
	for line in io.lines("intro_time.csv") do
		if line:find(filename) then
			-- consume filename
			line = string.sub(line, string.len(filename) + 2, string.len(line))
			print(line)
			-- consume start and end time
			comma, _  = string.find(line, ",")
			start_ts  = tonumber(string.sub(line, 1, comma - 1))
			end_ts    = tonumber(string.sub(line, comma + 1, string.len(line)))
		end
	end
end

function launch_timer()
	if start_ts == nil or end_ts == nil then
		return
	end
	local once = true
	print("Starting skip intro timer...")
	timer = mp.add_periodic_timer(1, function()
		local playback_time = mp.get_property_native("playback-time")
		if playback_time > start_ts and once then
			once = false
			mp.osd_message("(S)kip intro")
			mp.add_key_binding("S", BINDING_NAME, skip_intro)
		end
		if playback_time >= end_ts then
			print("Stoping skip intro timer...")
			timer:kill()
		end
	end)
end

function main()
	init()
	launch_timer()
end

-- script is loaded before the video, register event to get all properties
-- correctly initialized
mp.register_event("file-loaded", main)
