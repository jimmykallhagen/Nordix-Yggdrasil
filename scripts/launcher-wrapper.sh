#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

# Nordix - Wrapper for cosmic-app-library
# ensure that no remaining live processes are interfering, which
# apparently can happen after starting a few specific apps.
# an app so far but this ensured function regardless

# wrapper function:
# when you launch cosmic-app-library it
# look after running cosmic-app-librarys process.
# kill them if active process are dedected.
# otherwise it just launch cosmic-app-library.
# It kill every cosmic-app-library's process after you closed the meny.

# no processes should remain alive after you close the menu,
# and if it does, they will be killed by this wrapper,
# to always maintain good function for cosmci-app-library

# Uses Hyprland IPC to detect when the app is actually closed

APP="cosmic-app-library"
SCRIPT_PID=$$


if pgrep -f "$APP" | grep -v "$SCRIPT_PID" >/dev/null 2>&1; then
    pkill -f "$APP" --exclude $$ 2>/dev/null
    sleep 0.01
    # KILL!!
    if pgrep -f "$APP" | grep -v "$SCRIPT_PID" >/dev/null 2>&1; then
        pkill -9 -f "$APP" --exclude $$ 2>/dev/null
    fi
fi

"$APP" &
APP_PID=$!

sleep 0.5
while hyprctl layers | grep -q "app-library.*$APP_PID"; do
    sleep 0.5
done

sleep 0.2
pkill -f "$APP" --exclude $$ 2>/dev/null
sleep 0.2
pkill -9 -f "$APP" --exclude $$ 2>/dev/null
