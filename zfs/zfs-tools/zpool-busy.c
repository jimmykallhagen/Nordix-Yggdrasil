/*
SPDX-License-Identifier: GPL-3.0-or-later
Copyright (c) 2025 Nordix
This is a part of Yggdrasil - Nordix desktop envirorment
*/

/*
* zpool_check – reports whether ZFS is doing scrub, resilver, trim or nothing. 
* Run: ./zpool_check [poolname] (without arguments all pools are checked) 
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_MAX_LEN 512

typedef enum {
    STATE_NONE,
    STATE_SCRUB,
    STATE_RESILVER,
    STATE_TRIM
} ZpoolState;

static ZpoolState check_pool(const char *pool)
{
    char cmd[256];
    if (pool)
        snprintf(cmd, sizeof(cmd), "zpool status %s 2>/dev/null", pool);
    else
        snprintf(cmd, sizeof(cmd), "zpool status 2>/dev/null");

    FILE *fp = popen(cmd, "r");
    if (!fp) {
        fprintf(stderr, "error: kunde inte köra zpool status\n");
        exit(1);
    }

    char line[LINE_MAX_LEN];
    ZpoolState state = STATE_NONE;

    while (fgets(line, sizeof(line), fp)) {
/* 
* The "scan:" line contains info about ongoing or last completed operation. 
* Examples of ongoing: 
* scan: scrub in progress since ... 
* scan: resilver in progress since ... 
* scan: (none) 
* 
* TRIM is visible under "trim:" (one line per vdev) or in scan: 
* trim: action: TRIM in progress since ...
         */
        char *p = line;
        while (*p == ' ' || *p == '\t') p++;   /* strip leading whitespace */

        if (strncmp(p, "scan:", 5) == 0) {
            if (strstr(p, "scrub in progress"))
                state = STATE_SCRUB;
            else if (strstr(p, "resilver in progress"))
                state = STATE_RESILVER;
        } else if (strncmp(p, "trim:", 5) == 0) {
            if (strstr(p, "in progress"))
                state = STATE_TRIM;
        } else if (strncmp(p, "action:", 7) == 0) {
            /* Vissa ZFS-versioner skriver TRIM-status under action: */
            if (strstr(p, "TRIM in progress"))
                state = STATE_TRIM;
        }
    }

    pclose(fp);
    return state;
}

int main(int argc, char *argv[])
{
    const char *pool = (argc > 1) ? argv[1] : NULL;
    ZpoolState s = check_pool(pool);

    switch (s) {
    case STATE_SCRUB:    puts("scrub");    break;
    case STATE_RESILVER: puts("resilver"); break;
    case STATE_TRIM:     puts("trim");     break;
    default:             puts("none");     break;
    }

    return 0;
}
