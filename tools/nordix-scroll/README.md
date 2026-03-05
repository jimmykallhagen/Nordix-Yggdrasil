# nordix scroll

- This is a tool that i developt for nordix-pacman and nordix-paru
- I think i will use this behind a keybind in hyprland for shortcut to top or bottom

## how it works
- Emulates a virtual keybord/mouse and send scroll events to the kernel
- The user need to be in the group "input"

### Build

```bash
# nordix-pacman
clang -march=native -mtune=native -O3 -flto=full -o nordix-scroll-top nordix-scroll-top.c
# nordix-paru
clang -march=native -mtune=native -O3 -flto=full -o nordix-scroll-bottom nordix-scroll-bottom.c
```

### Install

```bash
sudo cp  nordix-scroll-bottom  nordix-scroll-top /usr/bin/
```

### Permissions (for auto-scroll)

The auto-scroll feature uses `/dev/uinput`. Add your user to the `input` group:

```bash
sudo usermod -aG input $USER
```

---

## License

* SPDX-License-Identifier: GPL-3.0-or-later                         
* Copyright (c) 2025 Jimmy Källhagen                                
* Part of **Yggdrasil - Nordix Desktop Environment**                   
* Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen

---