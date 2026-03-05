#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

# Path
FILE="Screenshot-$(date).png"

# Screenshot to clippboard
grimblast save window "$FILE"
pw-play --latency 10   --volume 3.0  /home/core/nordix/desktop-ljud/clean_camera.wav
sleep 2
# Notification
notify-send -t 5000 -h string:x-canonical-private-synchronous:grimblast \
"Screenshot Saved clipboard" "File: $(basename "$FILE")"
