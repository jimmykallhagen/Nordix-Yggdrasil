<p align="center">
  <img src="icons/hicolor/128x128/apps/nordix.png" alt="Nordix Logo" width="128"/>
</p>


# ❄️ Nordix System Settings

A graphical settings system for the Nordix Desktop Environment built on Hyprland. Provides a unified interface to configure the desktop without editing config files manually.

## Overview

Nordix System Settings is a collection of GTK4/Libadwaita settings modules accessed through a central launcher. Each module reads and writes directly to the corresponding Hyprland configuration file, with changes applied immediately via hyprctl reload.

The launcher hides while a settings module is open and reappears when it is closed.

## Modules

---
| Module               | Description | Config |
|----------------------|-------------------------------------------------------------------|-------------------------------------|
| General              | Borders, gaps, colors, resize behavior, tearing, snapping         | general.conf                        |
| Monitors             | Resolution, refresh rate, scale, HDR, 10-bit, VRR, dual monitor   | monitors.conf                       |
| Decorations          | Window borders, shadows, blur, opacity, rounding, dim             | decorations.conf                    |
| Layout               | Master, Dwindle, Scroll, Monolucer layout options                 | nordix-layout.conf                  |
| Groups               | Window groups, groupbar appearance, colors                        | nordix-groups.conf                  |
| Environment          | Language, GPU selection, Wayland/X11 compatibility, WebKit fixes  | environment.conf                    |
| Input                | Keyboard layout, repeat rate, mouse sensitivity, touchpad, scroll | nordix-input.conf                   |
| Keybindings          | Keyboard shortcuts and bind configuration                         | binds.conf                          |
| Default Applications | Default apps for MIME types and system environment variables      | mimeapps.list, system_defaults.conf |
| Advanced             | Performance tuning, rendering, and advanced Hyprland options      | advanced.conf                       |
---

## Architecture

nordix-system-settings.py is the central launcher that starts each module as an independent process. Each module is a standalone GTK4/Libadwaita application with its own application ID, allowing them to run in isolation without interfering with each other.

## How it works

1. Each settings module parses its corresponding Hyprland config file on startup
2. The user adjusts settings through the GUI
3. On Apply, the module writes the updated config and runs hyprctl reload
4. A backup of the previous config is created automatically before each save

## Config locations

All Nordix Desktop configuration files are stored in:

    ~/.config/nordix/desktop/config/

This keeps Nordix settings separate from any manual Hyprland configuration. The main Hyprland config sources these files.

## Requirements

- Hyprland
- Python 3
- GTK4
- Libadwaita

## Part of Nordix desktop envirorment **Yggdrasil**

- All of the Nordix settings GUI is components of the Nordix Desktop Environment Yggdrasil, an Arch Linux based desktop built on Hyprland with ZFS as the root filesystem. The system is designed to provide a complete desktop experience with graphical configuration tools while maintaining the power and flexibility of a tiling Wayland compositor.

## License

---

* SPDX-License-Identifier: GPL-3.0-or-later                         
* Copyright (c) 2025 Jimmy Källhagen                                
* Part of **Yggdrasil - Nordix Desktop Environment**                    
* Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen

---

