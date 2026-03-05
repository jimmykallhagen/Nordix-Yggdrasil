 <h1 align="center">Nordix Theme For Yggdrasil</h1>
<p align="center">
  <img src="../../icons/hicolor/128x128/apps/nordix.png" alt="Nordix Logo" width="128"/>
</p

Dynamic wallpaper-based theming for Nordix Desktop — automatically generates a matching color scheme for GTK-3, GTK-4, Qt, and Firefox from your wallpaper.  (nordix-dynamic-theme.py)

---


## Nordix principles - Honor the developers

### Nordix desktop theme for Yggdrasil is built upon the hard work of several outstanding open-source projects.<br> All credit for the foundational work belongs to the original developers. Here are the projects that make this possible:


- **[pywal](https://github.com/dylanaraps/pywal)** – The original pywal project, run by Dylan "dylanaraps" and contributors.
- **[pywal16](https://github.com/eylles/pywal16)** – 16-bit color fork of pywal, by Eylles and contributors.
- **[pywalfox](https://github.com/Frewacom/pywalfox)** – Themes Firefox dynamically, by Fredrik Engstrand "Frewacom" and contributors.
- **[colorz](https://github.com/metakirby5/colorz)** – A backend for pywal, by Ethan Chan "metakirby5" and Michael Polidori "mpolidori".
- **[haishoku](https://github.com/LanceGin/haishoku)** – Another pywal backend, by Gin "LanceGin" and Four "HungryFour".
- **[colorthief](https://github.com/fengsp/color-thief-py)** – Python color extractor, by Shipeng Feng "fengsp" and contributors.
- **[fast-colorthief](https://github.com/bedapisl/fast-colorthief)** – High-performance color extractor, by "bedapisl" and contributors.
- **[swww / Gswww](https://github.com/Ph1lll/Gswww)** – Resource-saving wallpaper system, by Phillip Davies "Ph1lll".
- **[waypaper](https://github.com/anufrievroman/waypaper)** – GUI wallpaper setter for Wayland and Xorg, by Roman "anufrievroman" and contributors.
- **[adw-gtk3](https://github.com/lassekongo83/adw-gtk3)** – Unofficial GTK3 port of libadwaita, by Mattias "lassekongo83". The base of Nordix Dynamic GTK Theme.

---

> "**_Even though the project is free of charge,_**  
> **_we are all responsible for paying by showing respect._**"  

> *Jimmy Källhagen – Nordix*

---

## How It Works

Nordix Dynamic Theme uses **pywal** to extract colors from your current wallpaper and applies them across the entire desktop:

- **GTK-3** — based on adw-gtk3-dark with pywal color variables, includes improved Thunar support with rounded rubberband selection
- **GTK-4** — custom `libadwaita-tweaks.css` for native libadwaita apps
- **Qt** — KDE color scheme generated from pywal, loaded via hyprqt6engine
- **Firefox** — themed via python-pywalfox (requires the Pywalfox extension in Firefox)

nordix-dynamic-theme.py runs: `gsettings set org.gnome.desktop.interface gtk-theme nordix-dynamic-theme` to set the GTK theme. It runs `hyprctl reload` to reload the Qt theme (Hyprland uses hyprqt6engine). Your hyprqt6engine.conf needs to point the color scheme to `~/.cache/wal/nordix-dynamic.colors` for the Qt theme to work.

nordix-wallpaper-loop.sh uses waypaper's own config to trigger a reload of Nordix Dynamic Theme. It is simple — nordix-wallpaper-loop.sh is like a timer where you tell it how many seconds you want between wallpaper changes. When the timer has run the specific seconds you have given it, it will run the command: `waypaper --random`. This takes a random picture from `~/Pictures/wallpapers`.

Every time the wallpaper changes, waypaper reloads `~/.config/waypaper/config.ini`. The waypaper config has the option `post_command`, and that is the key to triggering nordix-dynamic-theme.py. So every time the wallpaper changes, the post command runs: `post_command = /usr/bin/nordix-dynamic-theme.py` — and your desktop changes theme on GTK-3, GTK-4, Qt, Firefox and any terminals that are already open.

---

## Wallpaper Management

- Uses **swww** as wallpaper daemon — supports animated GIFs and static wallpapers
- Uses **waypaper** for wallpaper management and selection
- Includes `nordix-wallpaper-loop.sh` to auto-rotate random wallpapers from `~/Pictures/wallpapers`
- Uses **swengine** to browse and download wallpapers and GIFs
- Waypaper's config triggers Nordix Dynamic Theme on wallpaper change

---

## Templates

The pywal templates for Nordix Dynamic Theme need to be placed in `~/.config/wal/templates/`:

- `gtk.css` — GTK-3 theme template
- `libadwaita-tweaks.css` — GTK-4/libadwaita template
- `nordix-dynamic.colors` — Qt/KDE color scheme template

When `nordix-dynamic-theme.py` runs pywal, these templates are used to generate theme files in `~/.cache/wal/`. The script then creates symlinks to the correct locations so all toolkits pick up the same theme.

---

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

---

## Usage nordix-wallpaper-loop.sh

- Usage: nordix-wallpaper-loop.sh [TIME]
- Automatically change wallpaper at a set interval using waypaper.
- TIME — Seconds between wallpaper changes (default: 180)

---

## Pywalfox Theme Modes

nordix-dynamic-theme.py does not have support to take pywalfox flags like it has for regular pywal. But you can change the theme for pywalfox directly in the terminal and nordix-dynamic-theme.py will follow it, example: `pywalfox light`

This info is taken from: https://github.com/Frewacom/pywalfox

> There are three different theme modes: "Dark" (🌙), "Light" (☀) and "Auto" (👁)️. Selecting "Auto" will automatically switch between the other two modes based on a time interval found in the "General" section of the add-on settings GUI.

---

## Examples

- nordix-wallpaper-loop.sh 60 — Change every 60 seconds
- nordix-wallpaper-loop.sh 300 — Change every 5 minutes
- nordix-wallpaper-loop.sh — Change every 3 minutes (default)

---

## Install
```
sudo chmod +x /usr/lib/python3.14/site-packages/pywalfox/bin/main.sh
```
```
pywalfox install
```
```
sudo cp ./nordix-dynamic-theme.py /usr/bin
```
```
sudo chmod +x /usr/bin/nordix-dynamic-theme.py
```
```
sudo cp ./nordix-wallpaper-loop.sh /usr/bin
```
```
sudo chmod +x /usr/bin/nordix-wallpaper-loop.sh
```
## Waypaper Config

You can still run nordix-dynamic-theme.py
manually from your terminal, it will then take a color sample <br>
of your current wallpaper and apply it as a theme for your desktop.<br>
If you want your desktop to automatically change theme when you change the background,<br>
you need to add this as you see below to ~/.config/waypaper/config.ini
```
post_command = /path/to/nordix-dynamic-theme.py
```

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

---

## Work in Progress


- [ ] Discord theme integration
- [ ] Steam theme integration
- [ ] Wezterm theme integration
- [ ] Qt needs some work
- [ ] Some libadwaita programs are not good, like Lact
- [ ] Finish the Qt theme
- [ ] Create templates for gwenview
- [ ] Create template for Dolphin

---

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

---

> *The GTK-3 Thunar rubberband has some visual artifacts — every time you see them, think to yourself: "Jimmy can't do it better than this"* 😌

---

## Licens

#### **Nordix Dynamic Theme - Python wrapper (nordix-dynamic-theme.py)**
  * SPDX-License-Identifier: GPL-3.0-or-later
  * Copyright (c) 2025 Nordix
  * This file is part of Nordix - Yggdrasil desktop envirorment

#### **Nordix Wallpaper Loop - Randomly cycles wallpapers (nordix-wallpaper-loop.sh)**
  * SPDX-License-Identifier: GPL-3.0-or-later
  * Copyright (c) 2025 Nordix
  * This script is a part of Nordix - Yggdrasil desktop envirorment

#### **Nordix Dynamic Theme — libadwaita (libadwaita-tweaks.css)**
   * SPDX-License-Identifier: GPL-3.0-or-later
   * Copyright (c) 2025 Nordix
   * This theme is a part of Nordix - Yggdrasil desktop envirorment

#### Nordix Dynamic Theme — KDE/Qt Color Scheme (nordix-dynamic-qt.colors)**
   * SPDX-License-Identifier: GPL-3.0-or-later
   * Copyright (c) 2025 Nordix
   * This theme is a part ofNordix - Yggdrasil desktop envirorment

#### Nordix Dynamic GTK Theme - GTK3-template (nordix-dynamic-gtk-theme.css)**
   * SPDX-License-Identifier: LGPL-2.1 license
   * Copyright (c) 2025 Nordix
   * This theme is a part of Nordix - Yggdrasil desktop envirorment

  - **Based on adw-gtk3-dark (LGPL-2.1)**
  - Nordix modifications:
    * Dynamic color scheme for pywal integration
    * Added support for Thunar theming
    * [Original project](https://github.com/lassekongo83/adw-gtk3)


