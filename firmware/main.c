#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#include <irq.h>
#include <uart.h>
#include <time.h>
#include <generated/csr.h>
#include <generated/mem.h>
#include <hw/flags.h>
#include <console.h>
#include <system.h>

#include "ci.h"
#include "config.h"
#include "encoder.h"
#include "etherbone.h"
#include "ethernet.h"
#include "fx2.h"
#include "hdmi_out0.h"
#include "hdmi_out1.h"
#include "mdio.h"
#include "oled.h"
#include "opsis_eeprom.h"
#include "pattern.h"
#include "processor.h"
#include "stdio_wrap.h"
#include "telnet.h"
#include "tofe_eeprom.h"
#include "uptime.h"
#include "version.h"

void sleep(void);
void brightness(void);
void write_rgb(uint8_t, uint8_t, uint8_t);
void rgb(void);
int s = 0;

void sleep(void) {
    while (1) {
        if(elapsed(&s, SYSTEM_CLOCK_FREQUENCY/8)) {
            break;
        }
    }
}

void brightness(void) {
    static int i = 1;
    static int dir = 0;

    pwm_on_val_write(1 << i);
    i += dir ? -1 : 1;
    if (i == 11)
        dir = 1;
    else if (i == 0)
        dir = 0;
}

void write_rgb(uint8_t r, uint8_t g, uint8_t b) {
    uint32_t rgb = r | (g << 8) | (b << 16);
    rgb_rgb_write(rgb);
    printf("0x%x\n", rgb_rgb_read());

    /*rgb_r_on_val_write(r);*/
    /*rgb_g_on_val_write(g);*/
    /*rgb_b_on_val_write(b);*/
}

void rgb(void) {
    static int i = 0;
    static int c = 0;

    write_rgb((1 << 2) * ((i&1) == 1), (1 << 2) * ((i&2) == 2), (1 << 2) * ((i&4) == 4));

    c += 1;
    if (c == 8) {
        i += 1;
        if (i == 8)
            i = 0;
        c = 0;
    }
}

int main(void) {
    irq_setmask(0);
    irq_setie(1);
    uart_init();
    time_init();

    elapsed(&s, -1);

    puts("HDMI2USB blinker firmware booting...\r\n");

    while(true) {
        brightness();
        rgb();
        sleep();
    }
}
