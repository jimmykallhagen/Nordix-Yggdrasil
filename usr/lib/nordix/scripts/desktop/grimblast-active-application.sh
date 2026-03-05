#!/usr/bin/env bash
# Nordix - screenshoot 
# Version: 1.0
#
#
#

FILE="~/Pictures/Screenshots/Screenshot-$(date).png"


mkdir -p ~/Pictures/Screenshots



# Take screenshot of the active application that has focus

grimblast save active ~/Pictures/Screenshots/"Screenshot-$(date)".png
pw-play --latency 10   --volume 3.0  /home/core/nordix/desktop-ljud/clean_camera.wav
sleep 2
# Notification

notify-send -t 5000 -h string:x-canonical-private-synchronous:grimblast \
"Screenshot Saved in $HOME/Pictures/Screenshots" "File: $(basename "$FILE")"
