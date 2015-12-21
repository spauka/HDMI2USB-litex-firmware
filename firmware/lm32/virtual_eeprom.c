

#define I2C_STATUS_SHIFT_REG_FULL  1
#define I2C_STATUS_SHIFT_REG_EMPTY 2
#define I2C_STATUS_SHIFT_REG_READY 0

#define I2C_SLAVE_ADDRESS 0x51

int main(void)
{
    unsigned int addr = 0;
    unsigned char loading_low = 0;
    irq_setmask(0);
    irq_setie(1);
    uart_init();

    i2c_slave_addr_write(I2C_SLAVE_ADDRESS);
    i2c_shift_reg_write(fx2fw[addr]);
    i2c_status_write(I2C_STATUS_SHIFT_REG_READY);
    while(1) {
        unsigned char status = i2c_status_read();
        if(status == I2C_STATUS_SHIFT_REG_EMPTY) // there's been a master READ
        {
            addr++;
            //printf("READ 0x%04X\n", addr);
            i2c_shift_reg_write(fx2fw[addr]);
            i2c_status_write(I2C_STATUS_SHIFT_REG_READY);
        } 
        else if(status == I2C_STATUS_SHIFT_REG_FULL) // there's been a master WRITE
        {
            if(loading_low)
                addr |= i2c_shift_reg_read() & 0xFF;
            else
                addr = i2c_shift_reg_read() << 8;
            //printf("WRITE %04X\n", addr);
            if(loading_low)
                i2c_shift_reg_write(fx2fw[addr]);
            loading_low = 1 - loading_low;
            i2c_status_write(I2C_STATUS_SHIFT_REG_READY);

        } else if (status != 0) {
            printf("wuut? %02X\n", status);
        }
    }
    return 0;
}
