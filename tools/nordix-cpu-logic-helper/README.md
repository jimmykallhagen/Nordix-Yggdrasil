# Nordix CPU-Logic helper

## Overview
- Linux counts cpu cores and threads, very messy.
- If, like me, you have 16 cores and 32 threads,  
 you get a headache when you have to run a simple taskset.
- Nordix CPU-Logic helper automatically shows which threads are siblings. 

---

## **Why?** - Has anyone informed Torvald? Should it be like this?
#### Yes The questions are many, but I would think this is the explanation:

- I think that it is a leftover part of Linux, from a time when a CPU was single core only.
- When they later came up with the technology to be able to run two logical threads on one physical core,  they probably needed to rewrite the entire Linux logic for processor management.
- It probably became as simple as just picking up where the single core thread ended.
- they probably took the easy way out and pretended nothing happened, just kept adding the extra threads after the first few.

> *I wrote this with irony, so don't take it personally*
> *in case anyone takes offense. Linux kernel developers are probably the*  
> *last people you would accuse of taking the easy way out of solving problems.*

---

## Function
❯ nordix-cpu-logic-helper

        Core  0:   0 - 16
        Core  1:   1 - 17
        Core  2:   2 - 18
        Core  3:   3 - 19
        Core  4:   4 - 20
        Core  5:   5 - 21
        Core  6:   6 - 22
        Core  7:   7 - 23
        Core  8:   8 - 24
        Core  9:   9 - 25
        Core 10:  10 - 26
        Core 11:  11 - 27
        Core 12:  12 - 28
        Core 13:  13 - 29
        Core 14:  14 - 30
        Core 15:  15 - 31

- You can now clearly se that core 0 and 1 is 0,16 and 1,17
- So this is usefull for peaple like me.
- I was thinking i left core 0 and 1 alone to the system when i set nohz_full=3-31

---

## Licens
* SPDX-License-Identifier: GPL-3.0-or-later                         
* Copyright (c) 2025 Jimmy Källhagen                                
* Part of **Yggdrasil - Nordix Desktop Environment**
* Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen

---