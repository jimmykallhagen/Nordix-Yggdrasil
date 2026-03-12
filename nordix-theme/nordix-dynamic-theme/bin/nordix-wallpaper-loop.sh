#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##
# Randomly cycles wallpapers using waypaper at a set interval.

show_help() {
    echo "Usage: nordix-wallpaper-loop.sh [TIME]"
    echo ""
    echo "Automatically change wallpaper at a set interval using waypaper."
    echo ""
    echo "  TIME    Seconds between wallpaper changes (default: 180)"
    echo ""
    echo "Examples:"
    echo "  nordix-wallpaper-loop.sh 60      Change every 60 seconds"
    echo "  nordix-wallpaper-loop.sh 300     Change every 5 minutes"
    echo "  nordix-wallpaper-loop.sh         Change every 3 minutes (default)"
}

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

TIME_SEC="${1:-180}"

if ! [[ "$TIME_SEC" =~ ^[0-9]+$ ]]; then
    echo "Error: TIME must be a number (seconds)"
    echo ""
    show_help
    exit 1
fi

echo "Nordix Wallpaper Loop — changing every ${TIME_SEC}s"

while true; do
    waypaper --random
    sleep "$TIME_SEC"
done


