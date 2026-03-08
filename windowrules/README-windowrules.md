# Nordix Yggdrasil - Window Rules

Window rules configuration for the Yggdrasil desktop environment.

## Overview

Yggdrasil uses a two-tier window rules system that allows users to customize behavior while preserving system defaults.

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Yggdrasil Configuration                       │
├─────────────────────────────────────────────────────────────────────┤
│  source = /usr/lib/nordix/yggdrasil/config/system-windowrules.conf  │  ← System defaults (read first)
│  source = ~/.config/nordix/user/windowrules/user-windowrules.conf   │  ← User overrides (read last)
└─────────────────────────────────────────────────────────────────────┘
```

**Last rule wins** - User rules override system defaults automatically.

## File Locations

| File | Path | Purpose |
|------|------|---------|
| System | `/usr/lib/nordix/yggdrasil/config/system-windowrules.conf` | Default Yggdrasil rules (read-only) |
| User | `~/.config/nordix/user/windowrules/user-windowrules.conf` | User customizations |

## How It Works

1. **System rules load first** - Provides sane defaults for common applications
2. **User rules load last** - Any matching rule here overrides the system default

### Example: Override Opacity

System default sets Firefox to fully opaque:
```bash
# In system-windowrules.conf
windowrule = opacity 1.0 override, match:class ^(firefox)$
```

User wants transparency:
```bash
# In user-windowrules.conf
windowrule = opacity 0.85 override, match:class ^(firefox)$
```

Result: Firefox runs at 85% opacity.

## Features

### Built-in Reference Documentation

Both config files include complete Hyprland window rules documentation:
- Syntax reference for Hyprland 0.53+
- All available match properties
- All available effects (static and dynamic)
- Layer rules reference
- Regex tips
- Troubleshooting guide

No need to leave your editor to check the wiki.


### Opacity Sections

Opacity rules are marked with `#::: Opacity :::` for easy customization. Users who want to enable transparency can quickly find and modify these rules.

### Gaming Support

Global game rules using multiple detection methods:
- `match:content 3` - Content type detection
- `match:class ^(steam.*)$` - Steam client and games
- `match:class ^(steam_app_.*)$` - Steam games specifically

Games automatically get:
- `immediate on` - Tearing for lower latency
- `no_blur on` - Performance
- `no_dim on` - No dimming
- `workspace special:Game` - Dedicated game workspace

Toggle game overlay with keybind:
```bash
bind = $mainMod, G, togglespecialworkspace, Game
```

## System Rules Include

**Web Browser**
 * Firefox
 * Brave
 * Chromium
 * LibreWolf

**Image Viewers/Editor**
 - Gwenview

**GNU image manipulation program**
 - GIMP
    * Welcome to GIMP
    * Change Foreground Color

**File Managers**
 - Thunar
    * Rename Dialog
    * Properties Dialog
    * New Empty File
    * File Operation Progress
    * Confirm Replace
    * Open Shell Script
    * Create New Folder
    * Properties
 - Ark (Archive)
    *  Compress to Archive

**Dialog Systems**
 - Zenity
 - xdg-desktop-portal
     * xdg-desktop-portal-gtk
     * Save File
     * Open File
     * Add New Virtual Hardware

**Desktop Apps**
 - Upscayl (Select Image)
 - Smile (Emoji Picker)
 - Gucharmap (Character Map)
 - Crow Translate
 - Calculator (qalculate-gtk, GNOME Calculator)
 - Bluetooth (blueberry, blueman-manager)
 - Audio Controls (pavucontrol)
 - Network (nm-applet, nm-connection-editor)
 - Timeshift
 - GNOME System Monitor
 - File-Roller

**Terminals**
 - Wezterm
 - Ghostty
 - Cool Retro Term

**Visual Editors**
 - Sublime Text
 - Lapce
 - Zed

**Authentication**
 - Polkit
    * GCR-Prompter
    * Unlock Keyring

**Virtualization**
 - virt-manager

**Android**
 - Waydroid
    * Aurora Store
    * Package Installer
    * Android Vending

**COSMIC Apps**
 - com.system76.*

**Aplication Lancher**
 - cosmic-app-library

**Wallpaper-Store**
 - Swengine

**Local AI**
 - Jan AI
 - LM Studio
 - ClaraVerse

**Media**
 - Picture-in-Picture
 - mpv
 - imv
 - danmufloat
 - termfloat
 - nemo
 - ncmpcpp
 - Spotify

**Recording**
 - GPU Screen Recorder
 - OBS Studio

**Communication**
 - Discord
 - Armcord
 - Webcord

**Gaming**
 - Lutris
 - Global Game (match:content 3)
 - Steam
    * Self Updater
    * Steam Games (steam_app_*)
    * Steam Client

**Wine/Proton**
  - Wine (.exe)
  - Wine Config (winecfg.exe)
  - Wine Control Panel (control.exe)
  - Setup Files

**Download Manager**
  - Free Download Manager (fdm)

**Emulators**
  - Yuzu

**Global Rules**
  - Fullscreen
  - Modal Dialogs

**Special Workspaces**
  - Nordix (Sublime, Lapce, Zed, Crow Translate)
  - Game (steam_app_*, match:content 3)
  - System Settings (Nordix Settings)

**Additional Rules**
  - Flameshot
  - Pinentry (GPG Password)

**Layer Rules**
   - Cosmic App Library
   - Ashell
   - Mpvpaper (Wallpaper)
   - Notifications
   - Screenshot Selection


## Quick Start

### Add a New Application Rule

1. Open `~/.config/nordix/user/windowrules/user-windowrules.conf`
2. Find the window class: `hyprctl clients`
3. Add your rule:

```bash
# Example: Make Discord float
windowrule = float on, match:class ^(discord)$
```

### Override a System Rule

Just write the same rule with different values in your user config:

```bash
# System has: windowrule = no_blur on, match:class ^(steam)$
# Override with:
windowrule = no_blur off, match:class ^(steam)$
```

### Find Window Information

```bash
# List all windows with their properties
hyprctl clients

# List all layers
hyprctl layers
```

## Useful Commands

| Command | Description |
|---------|-------------|
| `hyprctl clients` | List windows with class/title |
| `hyprctl layers` | List layer namespaces |
| `hyprctl reload` | Reload configuration |
| `hyprctl keyword 'windowrule[name]:enable false'` | Disable named rule |

## License

GPL-3.0-or-later

Copyright (c) 2025 Jimmy Källhagen

Part of Nordix - Yggdrasil Desktop Environment
