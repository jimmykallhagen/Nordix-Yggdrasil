#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

# * Toggle XWayland scaling on/off
# * Workaround for scaling xwayland apps like Steam
# * Toggle before starting a game to enable native resolution
# * Default keybind: SUPER + CTRL + S

# Get current status
current_status=$(hyprctl getoption xwayland:force_zero_scaling | grep "int:" | awk '{print $2}')

if [ "$current_status" = "1" ]; then
    # Currently unscaled, switch to scaled (for regular apps)
    hyprctl keyword xwayland:force_zero_scaling false
   notify-send -t 5000 -h string:x-canonical-private-synchronous:force_zero_scaling "XWayland Scale" "Scaling ON (for regular apps)"
else
    # Currently scaled, switch to unscaled (for games in native 4K)
    hyprctl keyword xwayland:force_zero_scaling true
    notify-send -t 5000 -h string:x-canonical-private-synchronous:force_zero_scaling "XWayland Scale" "Scaling OFF (native resolution for games)"
fi
