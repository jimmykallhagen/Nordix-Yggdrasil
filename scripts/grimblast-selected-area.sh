#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##
FILE="~/Pictures/Screenshots/Screenshot-$(date).png"
mkdir -p ~/Pictures/Screenshots

# Screenshot
grimblast save area  ~/Pictures/Screenshots/"Screenshot-$(date)".png¨
pw-play --latency 10   --volume 3.0  /home/core/nordix/desktop-ljud/clean_camera.wav
sleep 2
# Notification
notify-send -t 5000 -h string:x-canonical-private-synchronous:grimblast \
"Screenshot Saved in ~/Pictures/screenshots" "File: $(basename "$FILE")"


