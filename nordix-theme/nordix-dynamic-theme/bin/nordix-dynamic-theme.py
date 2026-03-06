#!/usr/bin/env python3
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

import subprocess
import os
import json
import time
import argparse
from pathlib import Path

THEME_NAME = "nordix-dynamic-theme"

def get_current_wallpaper():
    try:
        result = subprocess.run(['swww', 'query'], capture_output=True, text=True, check=True)
        for line in result.stdout.split('\n'):
            if 'image:' in line:
                wallpaper = line.split('image: ')[1].strip()
                return wallpaper
    except subprocess.CalledProcessError as e:
        print(f"Error running swww: {e}")
        return None
    return None


# ==========================================================================
# Qt color generation — BreezeDark-style fixed offsets
# ==========================================================================
# BreezeDark uses three distinct brightness levels with FIXED offsets:
#
#   View    = 20,22,24   (Window - 12)  — darkest: content, lists, inputs
#   Window  = 32,35,38   (base)         — general window bg, sidebar
#   Header  = 41,44,48   (Window + 9)   — toolbar, buttons, tooltips
#
# The previous mix(bg, fg, N%) approach was wrong because it produced
# wildly different offsets depending on foreground brightness (e.g. +54
# instead of +9). Fixed offsets give consistent results like Breeze.
# ==========================================================================

def hex_to_rgb(hex_color):
    """Convert '#RRGGBB' to (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_str(rgb):
    """Convert (R, G, B) tuple to 'R,G,B' string for KDE .colors format."""
    return f"{rgb[0]},{rgb[1]},{rgb[2]}"

def clamp_rgb(rgb):
    """Clamp RGB values to 0-255 range."""
    return tuple(max(0, min(255, v)) for v in rgb)

def offset_rgb(base, delta):
    """Offset all RGB channels by a fixed amount."""
    return clamp_rgb(tuple(base[i] + delta for i in range(3)))

def load_pywal_colors():
    """Load pywal's generated colors from ~/.cache/wal/colors.json."""
    colors_file = Path.home() / ".cache/wal/colors.json"
    if not colors_file.exists():
        print(f"Error: {colors_file} not found")
        return None
    with open(colors_file) as f:
        data = json.load(f)
    
    colors = {}
    colors['background'] = hex_to_rgb(data['special']['background'])
    colors['foreground'] = hex_to_rgb(data['special']['foreground'])
    for i in range(16):
        colors[f'color{i}'] = hex_to_rgb(data['colors'][f'color{i}'])
    
    return colors

def generate_qt_colors(colors):
    """Generate derived colors using fixed offsets like Breeze Dark.
    
    BreezeDark hierarchy (3 levels, ~10 steps apart):
      View     = bg - 12   (darkest)
      Window   = bg        (base)
      Raised   = bg + 9    (header, button, tooltip, window-alt)
    """
    bg = colors['background']
    
    # Scale offsets based on bg brightness so very dark/bright bgs still work
    avg_bg = sum(bg) / 3
    down = max(8, min(15, int(avg_bg * 0.35)))   # ~10-12 for typical dark bg
    up   = max(6, min(12, int(avg_bg * 0.28)))    # ~7-9 for typical dark bg
    
    return {
        'view_bg':      offset_rgb(bg, -down),            # darkest: content areas
        'view_alt':     offset_rgb(bg, -down + (up // 2)),# alternating rows in view
        'raised':       offset_rgb(bg, up),               # header, button, tooltip, window-alt
        'hover':        offset_rgb(bg, up + 5),           # button hover
        'wm_active':    offset_rgb(bg, up + 2),           # WM active titlebar
        'wm_inactive':  bg,                               # WM inactive titlebar
    }


def build_color_sections(colors, derived):
    """Build the KDE color sections as a string.
    Used by both .colors and kdeglobals to avoid duplication."""
    bg = colors['background']
    fg = colors['foreground']
    raised = derived['raised']
    
    # Shorthand for foreground colors (same across all sections)
    c1  = rgb_str(colors['color1'])   # accent / red
    c2  = rgb_str(colors['color2'])   # success / green
    c3  = rgb_str(colors['color3'])   # warning / yellow
    c4  = rgb_str(colors['color4'])   # link / blue
    c5  = rgb_str(colors['color5'])   # visited / purple
    c8  = rgb_str(colors['color8'])   # inactive / muted
    c9  = rgb_str(colors['color9'])   # bright red
    fgs = rgb_str(fg)                 # foreground normal
    
    # BreezeDark pattern:
    # Button:       raised / raised        (Alternate=raised for hover-ish)
    # Complementary: raised / bg           
    # Header:       bg / raised            (Alt=bg, Norm=raised)
    # Header[Inact]: raised / bg           (swapped from active)
    # Selection:    accent-alt / accent
    # Tooltip:      bg / raised
    # View:         view-alt / view        (darkest level)
    # Window:       raised / bg            (Alt=raised, Norm=bg)

    return f"""\
[ColorEffects:Disabled]
Color=56,56,56
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={c8}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={rgb_str(derived['hover'])}
BackgroundNormal={rgb_str(raised)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Complementary]
BackgroundAlternate={rgb_str(raised)}
BackgroundNormal={rgb_str(bg)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Header]
BackgroundAlternate={rgb_str(bg)}
BackgroundNormal={rgb_str(raised)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Header][Inactive]
BackgroundAlternate={rgb_str(raised)}
BackgroundNormal={rgb_str(bg)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Selection]
BackgroundAlternate={c4}
BackgroundNormal={c1}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={fgs}
ForegroundInactive={c8}
ForegroundLink={c3}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Tooltip]
BackgroundAlternate={rgb_str(bg)}
BackgroundNormal={rgb_str(raised)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:View]
BackgroundAlternate={rgb_str(derived['view_alt'])}
BackgroundNormal={rgb_str(derived['view_bg'])}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[Colors:Window]
BackgroundAlternate={rgb_str(raised)}
BackgroundNormal={rgb_str(bg)}
DecorationFocus={c1}
DecorationHover={c1}
ForegroundActive={c1}
ForegroundInactive={c8}
ForegroundLink={c4}
ForegroundNegative={c9}
ForegroundNeutral={c3}
ForegroundNormal={fgs}
ForegroundPositive={c2}
ForegroundVisited={c5}

[General]
ColorScheme=NordixDynamic
Name=Nordix Dynamic
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={rgb_str(derived['wm_active'])}
activeBlend={fgs}
activeForeground={fgs}
inactiveBackground={rgb_str(derived['wm_inactive'])}
inactiveBlend={c8}
inactiveForeground={c8}
"""


def write_qt_colors_file(colors, derived):
    """Write the .colors file for hyprqt6engine."""
    header = """\
##===================================================================##
 # SPDX-License-Identifier: GPL-3.0-or-later                         #
 # Copyright (c) 2025 Jimmy Källhagen                                #
 # Part of Yggdrasil - Nordix desktop environment                    #
 # Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen # 
##===================================================================##

# Nordix Dynamic Theme — KDE/Qt Color Scheme
# Auto-generated by nordix-dynamic-theme.py from pywal colors.
# Uses BreezeDark-style fixed offsets for proper visual hierarchy.

"""
    return header + build_color_sections(colors, derived)


def write_kdeglobals_file(colors, derived):
    """Write kdeglobals — same colors plus KDE-specific settings."""
    content = build_color_sections(colors, derived)
    
    # Append KDE-specific sections that only belong in kdeglobals
    content += """
[Icons]
Theme=breeze-dark

[KFileDialog Settings]
Allow Expansion=false
Automatically select filename extension=true
Breadcrumb Navigation=true
Decoration position=2
Show Full Path=false
Show Inline Previews=true
Show Preview=false
Show Speedbar=true
Show hidden files=false
Sort by=Name
Sort directories first=true
Sort hidden files last=false
Sort reversed=false
Speedbar Width=173
View Style=DetailTree
"""
    return content


def generate_qt_theme_files():
    """Load pywal colors, compute blended values, write .colors and kdeglobals
    directly to their final locations."""
    colors = load_pywal_colors()
    if not colors:
        print("Could not load pywal colors — skipping Qt theme generation")
        return False
    
    derived = generate_qt_colors(colors)
    home = Path.home()
    
    # Write .colors file directly where hyprqt6engine.conf reads it
    qt_dir = home / ".themes" / THEME_NAME / "qt"
    qt_dir.mkdir(parents=True, exist_ok=True)
    colors_file = qt_dir / "nordix-dynamic.colors"
    colors_file.write_text(write_qt_colors_file(colors, derived))
    print(f"Qt color scheme written: {colors_file}")
    
    # Write kdeglobals directly to ~/.config/kdeglobals
    config_dir = home / ".config"
    config_dir.mkdir(parents=True, exist_ok=True)
    kdeglobals_file = config_dir / "kdeglobals"
    if kdeglobals_file.is_symlink():
        kdeglobals_file.unlink()
    kdeglobals_file.write_text(write_kdeglobals_file(colors, derived))
    print(f"kdeglobals written: {kdeglobals_file}")
    
    return True


def create_theme_symlinks():
    home = Path.home()

    # --- GTK3 ---
    gtk3_source = home / ".cache/wal/nordix-dynamic-gtk-theme.css"
    gtk3_dir = home / ".themes" / THEME_NAME / "gtk-3.0"
    gtk3_dir.mkdir(parents=True, exist_ok=True)
    link_gtk3 = gtk3_dir / "gtk.css"
    if link_gtk3.exists() or link_gtk3.is_symlink():
        link_gtk3.unlink()
    link_gtk3.symlink_to(gtk3_source)

    # --- GTK4 / libadwaita ---
    gtk4_source = home / ".cache/wal/nordix-dynamic-libadwaita-theme.css"
    gtk4_dir = home / ".config/gtk-4.0"
    gtk4_dir.mkdir(parents=True, exist_ok=True)
    link_gtk4 = gtk4_dir / "libadwaita-tweaks.css"
    if link_gtk4.exists() or link_gtk4.is_symlink():
        link_gtk4.unlink()
    link_gtk4.symlink_to(gtk4_source)

    # Qt .colors and kdeglobals are written directly by generate_qt_theme_files()

    print("Symbolic links created (GTK3 + GTK4/libadwaita)")


def apply_gtk_theme():
    try:
        subprocess.run([
            'gsettings', 'set', 
            'org.gnome.desktop.interface', 
            'gtk-theme', 
            THEME_NAME
        ], check=True)
        print("GTK theme applied with gsettings")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply theme: {e}")


def main():
    parser = argparse.ArgumentParser(description='Apply pywal colors from current wallpaper')
    parser.add_argument('-b', '--backend', 
                       default='fast-colorthief',
                       choices=['haishoku', 'colorthief', 'fast-colorthief', 'colorz', 'wal'],
                       help='Color backend to use (default: haishoku)')
    parser.add_argument('--cols16', 
                       default='foxify-lighten',
                       choices=['darken', 'lighten', 'dual', 'foxify-darken', 'foxify-lighten'],
                       help='16-color generation mode (default: foxify-lighten)')
    parser.add_argument('-a', '--alpha', type=float, default=0.5,
                       help='Terminal background transparency (default: 0.9)')
    parser.add_argument('-s', '--saturate', type=float, default=0.9,
                       help='Color saturation (default: 0.9)')
    parser.add_argument('-c', '--contrast', type=float, default=0.3,
                       help='Color contrast (default: 0.9)')
    parser.add_argument('-w', '--wait', type=int, default=4,
                       help='Seconds to wait for wallpaper to apply (default: 4)')
    
    args = parser.parse_args()
    
    time.sleep(args.wait)
    
    wallpaper = get_current_wallpaper()
    if not wallpaper:
        print("Failed to get wallpaper from swww")
        return
    
    print(f"Applying pywal to: {wallpaper}")
    print(f"Using backend: {args.backend}")
    
    wal_cmd = [
        'wal',
        '-a', str(args.alpha),
        '--saturate', str(args.saturate),
        '--contrast', str(args.contrast),
        '--cols16', str(args.cols16),
        '-i', wallpaper,
        '-n'
    ]
    
    if args.backend != 'wal':
        wal_cmd.extend(['--backend', args.backend])
    
    try:
        subprocess.run(wal_cmd, check=True)
        print("Pywal ran successfully")
    except subprocess.CalledProcessError as e:
        print(f"Pywal failed: {e}")
        return
    
    time.sleep(0.1)
    
    generate_qt_theme_files()
    
    create_theme_symlinks()
    
    subprocess.Popen(['pywalfox', 'update'])
    
    apply_gtk_theme()
    subprocess.run(['hyprctl', 'reload'], capture_output=True)
    print("Hyprland config reloaded (Qt theme refresh)")
    print("Nordix Dynamic Themes is applied!")
    
if __name__ == "__main__":
    main()
