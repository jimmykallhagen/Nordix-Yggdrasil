#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

# Shader Off Script

STATE_FILE="/tmp/hypr_shader_index"

# Reset index 
echo "-1" > "$STATE_FILE"

# Turn off shader
hyprctl keyword decoration:screen_shader ""

# Show notify
if command -v notify-send &> /dev/null; then
    notify-send -t 5000 -h string:x-canonical-private-synchronous:shader "Nordix shader's" "OFF"
fi
