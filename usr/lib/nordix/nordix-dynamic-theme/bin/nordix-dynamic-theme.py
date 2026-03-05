#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Nordix
#
# This file is part of Nordix Desktop

import subprocess
import os
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

def create_gtk_symlinks():
    home = Path.home()

    # --- GTK3 ---
    # Pywal generates ~/.cache/wal/gtk.css from the GTK3 template.
    # We symlink it into the theme directory so gsettings can pick it up.
    gtk3_source = home / ".cache/wal/gtk.css"
    gtk3_dir = home / ".themes" / THEME_NAME / "gtk-3.0"
    gtk3_dir.mkdir(parents=True, exist_ok=True)
    link_gtk3 = gtk3_dir / "gtk.css"

    # --- GTK4 / libadwaita ---
    # Pywal generates ~/.cache/wal/libadwaita-tweaks.css from the GTK4 template.
 
    gtk4_source = home / ".cache/wal/nordix-dynamic-libadwaita-theme.css"
    gtk4_dir = home / ".config/gtk-4.0/libadwaita-tweaks.css"
    gtk4_dir.mkdir(parents=True, exist_ok=True)
    link_gtk4 = gtk4_dir / "libadwaita-tweaks.css"

    for link in [link_gtk3, link_gtk4]:
        if link.is_symlink() or link.exists():
            link.unlink()

    link_gtk3.symlink_to(gtk3_source)
    link_gtk4.symlink_to(gtk4_source)
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
    
    # Build wal command
    wal_cmd = [
        'wal',
        '-a', str(args.alpha),
        '--saturate', str(args.saturate),
        '--contrast', str(args.contrast),
        '--cols16', str(args.cols16),
        '-i', wallpaper,
        '-n'
    ]
    
    # Add backend (only if not the default 'wal' backend)
    if args.backend != 'wal':
        wal_cmd.extend(['--backend', args.backend])
    
    try:
        subprocess.run(wal_cmd, check=True)
        print("Pywal ran successfully")
    except subprocess.CalledProcessError as e:
        print(f"Pywal failed: {e}")
        return
    
    time.sleep(0.1)
    
    create_gtk_symlinks()
    
    subprocess.Popen(['pywalfox', 'update'])
    
    apply_gtk_theme()
    subprocess.run(['hyprctl', 'reload'], capture_output=True)
    print("Hyprland config reloaded (Qt theme refresh)")
    print("Nordix Dynamic Themes is applied!")
    
if __name__ == "__main__":
    main()
