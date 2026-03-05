/*===================================================================*
 * SPDX-License-Identifier: GPL-3.0-or-later                         *
 * Copyright (c) 2025 Jimmy Källhagen                                *
 * Part of Yggdrasil - Nordix desktop environment                    *
 * Nordix and Yggdrasil are registered trademarks of Jimmy Källhagen *
 *===================================================================*/
// Nordix scoll events: scroll to bottom - or top, depends on your own scroll directions //

#define _GNU_SOURCE
#include <linux/uinput.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <errno.h>

int main() {
    int fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
    if (fd < 0) {
        fd = open("/dev/input/uinput", O_WRONLY | O_NONBLOCK);
        if (fd < 0) {
            perror("Failed to open uinput device");
            return 1;
        }
    }
    
    // Enable relative events (for mouse wheel)
    if (ioctl(fd, UI_SET_EVBIT, EV_REL) < 0) {
        perror("Failed to set EV_REL");
        close(fd);
        return 1;
    }
    
    // Enable wheel events
    if (ioctl(fd, UI_SET_RELBIT, REL_WHEEL) < 0) {
        perror("Failed to set REL_WHEEL");
        close(fd);
        return 1;
    }
    
    // Enable high-resolution wheel (modern systems)
    ioctl(fd, UI_SET_RELBIT, REL_WHEEL_HI_RES);  // Ignorera om det inte finns
    
    // Setup uinput device
    struct uinput_setup usetup = {0};
    strncpy(usetup.name, "nordix-scroll", UINPUT_MAX_NAME_SIZE);
    usetup.id.bustype = BUS_USB;
    usetup.id.vendor = 0x1234;
    usetup.id.product = 0x5678;
    usetup.id.version = 1;
    
    if (ioctl(fd, UI_DEV_SETUP, &usetup) < 0) {
        perror("UI_DEV_SETUP failed");
        close(fd);
        return 1;
    }
    
    if (ioctl(fd, UI_DEV_CREATE) < 0) {
        perror("UI_DEV_CREATE failed");
        close(fd);
        return 1;
    }
    
    // Give kernel time to set up the device
    usleep(250000);  // 200ms
    
    struct input_event ev;
    
    // ===== SCROLL DIRECTLY TO THE TOP =====
    // First method: traditional mouse wheel
    memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL;
    ev.value = -18000;  // - scroll upp
    write(fd, &ev, sizeof(ev));
    
    // Second method: high resolution scroll (more modern terminals)
    memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL_HI_RES;
    ev.value = -200000;  // Large value = scroll a lot
    write(fd, &ev, sizeof(ev));
    // Sync - important! Signals that the events are complete
    memset(&ev, 0, sizeof(ev));
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    
        memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL;
    ev.value = -18000;  // -100 = scroll down
    write(fd, &ev, sizeof(ev));
    
    // Second method: high resolution scroll (more modern terminals)
    memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL_HI_RES;
    ev.value = -200000;  // Large value = scroll a lot
    write(fd, &ev, sizeof(ev));
    // Sync - important! Signals that the events are complete
    memset(&ev, 0, sizeof(ev));
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    // Wait for the events to be processed
            memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL;
    ev.value = -18000;  // -100 = scroll down
    write(fd, &ev, sizeof(ev));
    
    // Second method: high resolution scroll (more modern terminals)
    memset(&ev, 1, sizeof(ev));
    ev.type = EV_REL;
    ev.code = REL_WHEEL_HI_RES;
    ev.value = -200000;  // Large value = scroll a lot
    write(fd, &ev, sizeof(ev));
    // Sync - important! Signals that the events are complete
    memset(&ev, 0, sizeof(ev));
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;
    write(fd, &ev, sizeof(ev));
    // Wait for the events to be processed
    usleep(300000);
    
    // Clean up
    ioctl(fd, UI_DEV_DESTROY);
    close(fd);

    return 0;
}