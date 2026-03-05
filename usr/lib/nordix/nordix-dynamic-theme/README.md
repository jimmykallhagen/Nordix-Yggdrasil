# Nordix Dynamic Theme (nordix-dynamic-theme.py)

Dynamic wallpaper-based theming for Nordix Desktop — automatically generates a matching color scheme for GTK-3, GTK-4, Qt, and Firefox from your wallpaper.


## First a try to honor the developers
- Nordix Dynamic Theme consists of a number of other people's projects.
- I am therefore grateful to be able to use these excellent programs
- To show respect for their projects I publish links to all projects here so you can go in and see for yourself all the hard work they put into their projects

**pywal** The original pywal project, a project run by Dylan Araps and a number of Contributors
- https://github.com/dylanaraps/pywal?tab=MIT-1-ov-file

**pywal16** The 16-bit color fork of pywal, a project run by eylles and a number of Contributors
- https://github.com/eylles/pywal16?tab=readme-ov-file

**pywalfox** The program that dynamic themes firefox, a project run by Fredrik Engstrand "Frewacom" and a number of Contributors
- https://github.com/Frewacom/pywalfox

**colorz** A backend that pywal can use, a project run by Ethan Chan "metakirby5" and the Contributor: Michael Polidori "mpolidori" (at the time of writing)
- https://github.com/metakirby5/colorz

**haishoku** A backend that pywal can use, a project run by Gin "LanceGin" and the Contributor: Four "HungryFour" a developer who I guess works like four - (at the time of writing)
- https://github.com/LanceGin/haishoku

**colorthief** A backend that pywal can use, a project run by Shipeng Feng "fengsp" and the Contributors: Josh Leeb-du Toit "joshleeb" and "crazyzubr"- (at the time of writing)
- https://github.com/fengsp/color-thief-py

**fast-colorthief**  A backend that pywal can use, a project run by "bedapisl" and the Contributor: "baseplate-admin · Baseplatisphere" - (at the time of writing)
- https://github.com/bedapisl/fast-colorthief

**swww/Gswww** A resource-saving system for displaying images or animations as wallpaper, a project run by Phillip Davies "Ph1lll"
- https://github.com/Ph1lll/Gswww

**waypaper** GUI wallpaper setter for Wayland and Xorg, a project run by Roman "anufrievroman" and a number of Contributors
- https://github.com/anufrievroman/waypaper

**adw-gtk3** An unofficial GTK3 port of libadwaita, a project run by Mattias "lassekongo83" and a number of Contributors.
- https://github.com/lassekongo83/adw-gtk3?tab=readme-ov-file
- It is the theme that i based Nordix Dynamic GTK Theme on






## How It Works

Nordix Dynamic Theme uses **pywal** to extract colors from your current wallpaper and applies them across the entire desktop:

- **GTK-3** — based on adw-gtk3-dark with pywal color variables, includes improved Thunar support with rounded rubberband selection
- **GTK-4** — custom `libadwaita-tweaks.css` for native libadwaita apps
- **Qt** — KDE color scheme generated from pywal, loaded via hyprqt6engine
- **Firefox** — themed via python-pywalfox (requires the Pywalfox extension in Firefox)

nordix-dynamic-theme.py runs: `gsettings set org.gnome.desktop.interface gtk-theme nordix-dynamic-theme` to set the GTK theme. It runs `hyprctl reload` to reload the Qt theme (Hyprland uses hyprqt6engine). Your hyprqt6engine.conf needs to point the color scheme to `~/.cache/wal/nordix-dynamic.colors` for the Qt theme to work.

nordix-wallpaper-loop.sh uses waypaper's own config to trigger a reload of Nordix Dynamic Theme. It is simple — nordix-wallpaper-loop.sh is like a timer where you tell it how many seconds you want between wallpaper changes. When the timer has run the specific seconds you have given it, it will run the command: `waypaper --random`. This takes a random picture from `~/Pictures/wallpapers`.

Every time the wallpaper changes, waypaper reloads `~/.config/waypaper/config.ini`. The waypaper config has the option `post_command`, and that is the key to triggering nordix-dynamic-theme.py. So every time the wallpaper changes, the post command runs: `post_command = /usr/bin/nordix-dynamic-theme.py` — and your desktop changes theme on GTK-3, GTK-4, Qt, Firefox and any terminals that are already open.

## Wallpaper Management

- Uses **swww** as wallpaper daemon — supports animated GIFs and static wallpapers
- Uses **waypaper** for wallpaper management and selection
- Includes `nordix-wallpaper-loop.sh` to auto-rotate random wallpapers from `~/Pictures/wallpapers`
- Uses **swengine** to browse and download wallpapers and GIFs
- Waypaper's config triggers Nordix Dynamic Theme on wallpaper change

## Templates

The pywal templates for Nordix Dynamic Theme need to be placed in `~/.config/wal/templates/`:

- `gtk.css` — GTK-3 theme template
- `libadwaita-tweaks.css` — GTK-4/libadwaita template
- `nordix-dynamic.colors` — Qt/KDE color scheme template

When `nordix-dynamic-theme.py` runs pywal, these templates are used to generate theme files in `~/.cache/wal/`. The script then creates symlinks to the correct locations so all toolkits pick up the same theme.

## Usage

`nordix-dynamic-theme.py` accepts the standard pywal flags:

| Flag               | Description                                                    |
|--------------------|----------------------------------------------------------------|
| `--backend`        | `haishoku`, `colorthief`, `fast-colorthief`, `colorz`, `wal`   |
| `--cols16`         | `darken`, `lighten`, `dual`, `foxify-darken`, `foxify-lighten` |
| `-a`, `--alpha`    | Terminal transparency (0-100)                                  |
| `-s`, `--saturate` | Adjust color saturation                                        |
| `-c`, `--contrast` | Adjust color contrast                                          |
| `-w`, `--wait`     | Delay before applying                                          |

## Usage nordix-wallpaper-loop.sh

- Usage: nordix-wallpaper-loop.sh [TIME]
- Automatically change wallpaper at a set interval using waypaper.
- TIME — Seconds between wallpaper changes (default: 180)

## Pywalfox Theme Modes

nordix-dynamic-theme.py does not have support to take pywalfox flags like it has for regular pywal. But you can change the theme for pywalfox directly in the terminal and nordix-dynamic-theme.py will follow it, example: `pywalfox light`

This info is taken from: https://github.com/Frewacom/pywalfox

> There are three different theme modes: "Dark" (🌙), "Light" (☀) and "Auto" (👁)️. Selecting "Auto" will automatically switch between the other two modes based on a time interval found in the "General" section of the add-on settings GUI.

## Examples

- nordix-wallpaper-loop.sh 60 — Change every 60 seconds
- nordix-wallpaper-loop.sh 300 — Change every 5 minutes
- nordix-wallpaper-loop.sh — Change every 3 minutes (default)

## Install

- sudo chmod +x /usr/lib/python3.14/site-packages/pywalfox/bin/main.sh
- pywalfox install
- sudo cp ./nordix-dynamic-theme.py /usr/bin
- sudo chmod +x /usr/bin/nordix-dynamic-theme.py
- sudo cp ./nordix-wallpaper-loop.sh /usr/bin
- sudo chmod +x /usr/bin/nordix-wallpaper-loop.sh

## Waypaper Config

- Waypaper needs to have this in ~/.config/waypaper/config.ini
- post_command = /path/to/nordix-dynamic-theme.py

## Nordix Wallpaper Loop

- Designed to be autostarted
- First you need to start the swww-daemon
- In Hyprland: exec-once = swww-daemon &
- In Hyprland: exec-once = nordix-wallpaper-loop.sh 150 &
- You can run it from the terminal with:
  * swww-daemon &
  * nordix-wallpaper-loop.sh 150 &

## Nordix Dynamic Theme Default Wal Settings

- --backend fast-colorthief
- --cols16 foxify-lighten
- --alpha 0.5
- -a 0.9 — Terminal background transparency
- --saturate 0.9
- --contrast 0.9
- --wait 4

## Work in Progress

- Discord theme integration
- Steam theme integration
- Wezterm theme integration

## Package List

### Pacman
- waypaper
- swww

### AUR
- python-pywal16-git
- pywal-discord-git
- python-pywalfox
- colorz
- python-fast-colorthief
- python-colorthief
- python-haishoku
- python-wal-steam-git

### Nordix
- nordix-dynamic-theme.py
- nordix-wallpaper-loop.sh
- libadwaita-tweaks.css
- nordix-dynamic-qt.colors
- nordix-dynamic-gtk-theme.css

> *The GTK-3 Thunar rubberband has some visual artifacts — every time you see them, think to yourself: "Jimmy can't do it better than this"* 😌

## Licens

- Nordix Dynamic Theme - Python wrapper (nordix-dynamic-theme.py)

  SPDX-License-Identifier: GPL-3.0-or-later
  Copyright (c) 2025 Nordix
  This file is part of Nordix Desktop

- Nordix Wallpaper Loop - Randomly cycles wallpapers (nordix-wallpaper-loop.sh)
 
  SPDX-License-Identifier: GPL-3.0-or-later
  Copyright (c) 2025 Nordix
  This script is a part of Nordix Desktop

- Nordix Dynamic Theme — libadwaita (libadwaita-tweaks.css)

   SPDX-License-Identifier: GPL-3.0-or-later
   Copyright (c) 2025 Nordix
   This theme is a part of Nordix Desktop

- Nordix Dynamic Theme — KDE/Qt Color Scheme (nordix-dynamic-qt.colors)
 
  SPDX-License-Identifier: GPL-3.0-or-later
  Copyright (c) 2025 Nordix
  This theme is a part of Nordix Desktop

- Nordix Dynamic GTK Theme - GTK3-template (nordix-dynamic-gtk-theme.css)

  SPDX-License-Identifier: LGPL-2.1 license
  Copyright (c) 2025 Nordix
  This theme is a part of Nordix Desktop
 
  Based on adw-gtk3-dark (LGPL-2.1)
  Nordix modifications:
    * Dynamic color scheme for pywal integration
    * Added support for Thunar theming
  Original project: https://github.com/lassekongo83/adw-gtk3


