# nordix-filestat

#### **A file size analysis tool for understanding the storage characteristics of directories. Included with Nordix Desktop to help users make informed decisions when configuring ZFS dataset options like recordsize.**

---

## Usage

```
nordix-filestat /path/to/directory
nordix-filestat -a /path/to/directory
nordix-filestat -q /path/to/directory
```

---

## Options

| **Flag**   | **Description**                      |
|--------|------------------------------------------|
| (none) | Filtered analysis with size distribution |
| -a     | Include all files (no filtering)         |
| -q     | Compact output (no size distribution)    |
| -aq    | All files, compact output                |
| -h     | Show help                                |

---

## What it does

- Scans a directory recursively and reports file count, total size, average, median, min, max, and a size distribution breakdown from 4 KB to 1 MB+.

---

## Filtered vs All

#### **By default, nordix-filestat excludes file types that are irrelevant when measuring actual data content: text files, scripts, source code, configs, images, icons, fonts, desktop entries, empty files and symlinks.**

- **USE:** -a to include everything.

---

## Why this exists

- Nordix Yggdrasil runs on ZFS.
- Properties like recordsize have a significant impact on performance and space efficiency.
- The optimal value depends on what kind of files a dataset actually contains.
- This tool gives you the data to make that decision yourself rather than guessing.

---

## License
* SPDX-License-Identifier: GPL-3.0-or-later                         
* Copyright (c) 2025 Jimmy Källhagen                                
* Part of **Yggdrasil - Nordix Desktop Environment**                    
* Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen

---