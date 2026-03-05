# nordix move

- **Nordic Move is a tool to optimize your file transfer.**

---

## What is does
'''
The move command is a single core process only.
This tool assigns the move process to two cores instead of one.
This has a positive impact on the process's performance, meaning it will go faster to move large files.
'''

---

## how it works

---

'''
If you force the move process to use two cores, it will not magically become a multi-threaded process.
However, you can give it some breathing room by running the process until one core gets hot and where you normally see a decrease in boost or tickrate, the move process can now shift cores to a cooler one and not lose speed. 
Giving it access to more cores than two does not seem to be of any use.
'''

---
'''
This tool automatically retrieves the last two cores on your CPU and then assigns them to the move command process. To be clear, not the last two threads, but two physical cores. I chose the last ones deliberately to also move the process away from the cores that you normally see the system favoring, this for smarter process management."
'''
---

### **Install**

```bash
sudo cp nx-mv /usr/bin/
sudo chmod +x /usr/bin/nx-mv
```

#### **Optional** - put Nordix Move behind your regular move command 'mv'
- **For fish shell**
'''
sed -i "\$a alias mv='nx-mv'" ~/.config/fish/config.fish
'''
- **For bash shell**
'''
sed -i "\$a alias mv='nx-mv'" ~/.bashrc
'''
- **For zsh shell**
'''
sed -i "\$a alias mv='nx-mv'" ~/.zshrc
'''

---

## License

* SPDX-License-Identifier: GPL-3.0-or-later                         
* Copyright (c) 2025 Jimmy Källhagen                                
* Part of **Yggdrasil - Nordix Desktop Environment**                    
* Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen

---