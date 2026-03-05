/*===================================================================*
 * SPDX-License-Identifier: GPL-3.0-or-later                         *
 * Copyright (c) 2025 Jimmy Källhagen                                *
 * Part of Yggdrasil - Nordix desktop environment                    *
 * Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen *
 *===================================================================*/
/*
 Nordx Ghostty background toggler and config reload

******************************************************************************************
you might think it's inappropriate to license this under gpl when ghostty is MIT?
yes, it might be!
But since ghostty's maintainers didn't respond when I tried to reach them,
where I offered to share this tool/plugin/feature with them, I made two attempts.
I recorded a youtube video for demonstration, I sent mail with descriptions and the link,
no one looked at it. I waited, tried to get in touch in another way where
I told them about the pluggin and how i have manage to solved
the problem to auto reload ghostty, that i have send them an mail with descriptions of the plugin.
You only make two attempts, after that you're whiny
****************************************************************

***
So I use GPL like i do on everything else. (MIT is not good) 
I include the "pluggin" in Nordix to every user that wants to use ghostty
yes, of course it is free to use it outside of Nordix as well
*/
#define _GNU_SOURCE
#include <linux/uinput.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <ctype.h>
#include <dirent.h>

// Function to send Ctrl Shift ,
void send_reload_keys() {
    int fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
    if (fd < 0) {
        fd = open("/dev/input/uinput", O_WRONLY | O_NONBLOCK);
        if (fd < 0) {
            perror("Failed to open uinput device");
            return;
        }
    }
    
    ioctl(fd, UI_SET_EVBIT, EV_KEY);
    ioctl(fd, UI_SET_KEYBIT, KEY_LEFTCTRL);
    ioctl(fd, UI_SET_KEYBIT, KEY_LEFTSHIFT);
    ioctl(fd, UI_SET_KEYBIT, KEY_COMMA);
    
    struct uinput_setup usetup;
    memset(&usetup, 0, sizeof(usetup));
    strncpy(usetup.name, "ghostty-reload-keys", UINPUT_MAX_NAME_SIZE);
    usetup.id.bustype = BUS_USB;
    usetup.id.vendor = 0x1234;
    usetup.id.product = 0x5678;
    usetup.id.version = 1;
    
    if (ioctl(fd, UI_DEV_SETUP, &usetup) < 0) {
        perror("UI_DEV_SETUP failed");
        close(fd);
        return;
    }
    
    if (ioctl(fd, UI_DEV_CREATE) < 0) {
        perror("UI_DEV_CREATE failed");
        close(fd);
        return;
    }
    
    usleep(100000);
    
    struct input_event ev;
    
    // Press Ctrl
    memset(&ev, 0, sizeof(ev));
    ev.type = EV_KEY;
    ev.code = KEY_LEFTCTRL;
    ev.value = 1;
    write(fd, &ev, sizeof(ev));
    
    // Press Shift  
    ev.code = KEY_LEFTSHIFT;
    write(fd, &ev, sizeof(ev));
    
    // Press Comma
    ev.code = KEY_COMMA;
    write(fd, &ev, sizeof(ev));
    
    // Sync
    memset(&ev, 0, sizeof(ev));
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    
    usleep(50000);
    
    // Release Comma
    ev.type = EV_KEY;
    ev.code = KEY_COMMA;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    
    // Release Shift
    ev.code = KEY_LEFTSHIFT;
    write(fd, &ev, sizeof(ev));
    
    // Release Ctrl
    ev.code = KEY_LEFTCTRL;
    write(fd, &ev, sizeof(ev));
    
    // Final sync
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    
    usleep(10000);
    
    ioctl(fd, UI_DEV_DESTROY);
    close(fd);
}

// Function to change ONLY background-image =
void change_background_image_only() {
    char *home = getenv("HOME");
    if (!home) {
        fprintf(stderr, "HOME environment variable not set\n");
        return;
    }
    
    char config_path[512];
    char bg_dir[512];
    snprintf(config_path, sizeof(config_path), "%s/.config/ghostty/config", home);
    snprintf(bg_dir, sizeof(bg_dir), "%s/Pictures/ghostty-backgrounds", home);
    
    mkdir(bg_dir, 0755);
    
// Read config
    FILE *config = fopen(config_path, "r");
    if (!config) {
        perror("Could not open config file");
        return;
    }
    
    char line[512];
    char current_bg[512] = "";
    int current_num = 0;
    int has_background_image = 0;
    
    while (fgets(line, sizeof(line), config)) {
        char *setting = line;
        while (*setting && isspace(*setting)) setting++;
        
        if (strncmp(setting, "background-image", 16) == 0) {
            char *after_name = setting + 16;
            while (*after_name && isspace(*after_name)) after_name++;
            
            if (*after_name == '=') {
                char *value = after_name + 1;
                while (*value && isspace(*value)) value++;
                
                char *dest = current_bg;
                while (*value && !isspace(*value) && *value != '#' && 
                       dest < current_bg + sizeof(current_bg) - 1) {
                    *dest++ = *value++;
                }
                *dest = '\0';
                has_background_image = 1;
            }
        }
    }
    fclose(config);
    
// Get current number
    if (current_bg[0]) {
        char *filename = strrchr(current_bg, '/');
        if (filename) filename++;
        else filename = current_bg;
        
        char *dot = strrchr(filename, '.');
        if (dot) *dot = '\0';
        
        int is_number = 1;
        for (char *p = filename; *p; p++) {
            if (!isdigit(*p)) {
                is_number = 0;
                break;
            }
        }
        
        if (is_number) {
            current_num = atoi(filename);
        }
    }
    
// Find the next image
    int next_num = current_num + 1;
    char next_bg[512];
    
    while (1) {
        snprintf(next_bg, sizeof(next_bg), "%s/%d.png", bg_dir, next_num);
        
        struct stat st;
        if (stat(next_bg, &st) == 0) {
            break;
        }
        
        next_num++;
        
        if (next_num > 100) {
            next_num = 1;
            snprintf(next_bg, sizeof(next_bg), "%s/%d.png", bg_dir, next_num);
            if (stat(next_bg, &st) == 0) {
                break;
            }
            
            fprintf(stderr, "No background images found in %s\n", bg_dir);
            return;
        }
    }
    
// Update config
    char temp_path[512];
    snprintf(temp_path, sizeof(temp_path), "%s.tmp", config_path);
    
    config = fopen(config_path, "r");
    FILE *temp = fopen(temp_path, "w");
    
    if (!config || !temp) {
        fprintf(stderr, "Could not open files for writing\n");
        if (config) fclose(config);
        if (temp) fclose(temp);
        return;
    }
    
    while (fgets(line, sizeof(line), config)) {
        char *setting = line;
        while (*setting && isspace(*setting)) setting++;
        
        if (strncmp(setting, "background-image", 16) == 0) {
            char *after_name = setting + 16;
            while (*after_name && isspace(*after_name)) after_name++;
            
            if (*after_name == '=') {
                fprintf(temp, "background-image = %s\n", next_bg);
            } else {
                fputs(line, temp);
            }
        } else {
            fputs(line, temp);
        }
    }
    
    if (!has_background_image) {
        fprintf(temp, "\nbackground-image = %s\n", next_bg);
    }
    
    fclose(config);
    fclose(temp);
    
    rename(temp_path, config_path);
    
    printf("Changed background-image to: %s\n", next_bg);
}

int main() {
    change_background_image_only();
    send_reload_keys();
    return 0;
}