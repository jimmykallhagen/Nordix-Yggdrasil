#!/bin/bash
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

#*****************************************************
# This is purely because i think it looks fun 
#
#  * The top bar is delayed by a couple of seconds.
#  * Gives the impression that the top bar,
#  * "overslept" and it's late for work,
#  * rushes in, way too fast, 
#  * collides with the top edge of the moniteor so it bounces
#
#***************************************************************

#****                                    ****************# 
# If you have now read this,                             #
# well then you will probably think,                     #
# that "Jimmy is so childish" every time you logging in. #
# and I think that's even more fun                       #
#****************                                    ****#  

killall -SIGUSR2 ashell

sleep 2

exec ashell --config-path ~/.config/nordix/desktop/config/nordix-ashell-theme.toml &