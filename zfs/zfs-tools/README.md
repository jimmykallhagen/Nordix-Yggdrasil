## this tool is meant to be used precisely to identify if zpool has a work in progress with trim, scrub, or resilver. 
 
## this tool is intended to act as a helper for other tools, it is naturally possible to use it manually if you want that too. and it is a part of the development of nnordix-graceful-shutdown

when you run zpool-busy, there are 4 responses you can get 

  * scrub 
  * resilver 
  * trim 
  * none

## license
- SPDX-License-Identifier: GPL-3.0-or-later
- Copyright (c) 2025 Nordix
- This is a part of Yggdrasil - Nordix desktop envirorment