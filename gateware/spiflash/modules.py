
import re

# Taken from http://repo.or.cz/openocd.git/blob/HEAD:/src/flash/nor/spi.c
# 6501fbc18d674932496278bb8cfe55f02c38836c
#        /* name, erase_cmd, chip_erase_cmd, device_id, pagesize, sectorsize, size_in_bytes */
data = """\
        FLASH_ID("st m25p05",      0xd8, 0xc7, 0x00102020, 0x80,  0x8000,  0x10000),
        FLASH_ID("st m25p10",      0xd8, 0xc7, 0x00112020, 0x80,  0x8000,  0x20000),
        FLASH_ID("st m25p20",      0xd8, 0xc7, 0x00122020, 0x100, 0x10000, 0x40000),
        FLASH_ID("st m25p40",      0xd8, 0xc7, 0x00132020, 0x100, 0x10000, 0x80000),
        FLASH_ID("st m25p80",      0xd8, 0xc7, 0x00142020, 0x100, 0x10000, 0x100000),
        FLASH_ID("st m25p16",      0xd8, 0xc7, 0x00152020, 0x100, 0x10000, 0x200000),
        FLASH_ID("st m25p32",      0xd8, 0xc7, 0x00162020, 0x100, 0x10000, 0x400000),
        FLASH_ID("st m25p64",      0xd8, 0xc7, 0x00172020, 0x100, 0x10000, 0x800000),
        FLASH_ID("st m25p128",     0xd8, 0xc7, 0x00182020, 0x100, 0x40000, 0x1000000),
        FLASH_ID("st m45pe10",     0xd8, 0xd8, 0x00114020, 0x100, 0x10000, 0x20000),
        FLASH_ID("st m45pe20",     0xd8, 0xd8, 0x00124020, 0x100, 0x10000, 0x40000),
        FLASH_ID("st m45pe40",     0xd8, 0xd8, 0x00134020, 0x100, 0x10000, 0x80000),
        FLASH_ID("st m45pe80",     0xd8, 0xd8, 0x00144020, 0x100, 0x10000, 0x100000),
        FLASH_ID("sp s25fl004",    0xd8, 0xc7, 0x00120201, 0x100, 0x10000, 0x80000),
        FLASH_ID("sp s25fl008",    0xd8, 0xc7, 0x00130201, 0x100, 0x10000, 0x100000),
        FLASH_ID("sp s25fl016",    0xd8, 0xc7, 0x00140201, 0x100, 0x10000, 0x200000),
        FLASH_ID("sp s25fl116k",   0xd8, 0xc7, 0x00154001, 0x100, 0x10000, 0x200000),
        FLASH_ID("sp s25fl032",    0xd8, 0xc7, 0x00150201, 0x100, 0x10000, 0x400000),
        FLASH_ID("sp s25fl132k",   0xd8, 0xc7, 0x00164001, 0x100, 0x10000, 0x400000),
        FLASH_ID("sp s25fl064",    0xd8, 0xc7, 0x00160201, 0x100, 0x10000, 0x800000),
        FLASH_ID("sp s25fl164k",   0xd8, 0xc7, 0x00174001, 0x100, 0x10000, 0x800000),
        FLASH_ID("sp s25fl128",    0xd8, 0xc7, 0x00182001, 0x100, 0x10000, 0x1000000),
        FLASH_ID("sp s25fl256",    0xd8, 0xc7, 0x00190201, 0x100, 0x10000, 0x2000000),
        FLASH_ID("atmel 25f512",   0x52, 0xc7, 0x0065001f, 0x80,  0x8000,  0x10000),
        FLASH_ID("atmel 25f1024",  0x52, 0x62, 0x0060001f, 0x100, 0x8000,  0x20000),
        FLASH_ID("atmel 25f2048",  0x52, 0x62, 0x0063001f, 0x100, 0x10000, 0x40000),
        FLASH_ID("atmel 25f4096",  0x52, 0x62, 0x0064001f, 0x100, 0x10000, 0x80000),
        FLASH_ID("atmel 25fs040",  0xd7, 0xc7, 0x0004661f, 0x100, 0x10000, 0x80000),
        FLASH_ID("mac 25l512",     0xd8, 0xc7, 0x001020c2, 0x010, 0x10000, 0x10000),
        FLASH_ID("mac 25l1005",    0xd8, 0xc7, 0x001120c2, 0x010, 0x10000, 0x20000),
        FLASH_ID("mac 25l2005",    0xd8, 0xc7, 0x001220c2, 0x010, 0x10000, 0x40000),
        FLASH_ID("mac 25l4005",    0xd8, 0xc7, 0x001320c2, 0x010, 0x10000, 0x80000),
        FLASH_ID("mac 25l8005",    0xd8, 0xc7, 0x001420c2, 0x010, 0x10000, 0x100000),
        FLASH_ID("mac 25l1605",    0xd8, 0xc7, 0x001520c2, 0x100, 0x10000, 0x200000),
        FLASH_ID("mac 25l3205",    0xd8, 0xc7, 0x001620c2, 0x100, 0x10000, 0x400000),
        FLASH_ID("mac 25l6405",    0xd8, 0xc7, 0x001720c2, 0x100, 0x10000, 0x800000),
        FLASH_ID("micron n25q064", 0xd8, 0xc7, 0x0017ba20, 0x100, 0x10000, 0x800000),
        FLASH_ID("micron n25q128", 0xd8, 0xc7, 0x0018ba20, 0x100, 0x10000, 0x1000000),
        FLASH_ID("win w25q80bv",   0xd8, 0xc7, 0x001440ef, 0x100, 0x10000, 0x100000),
        FLASH_ID("win w25q32fv",   0xd8, 0xc7, 0x001640ef, 0x100, 0x10000, 0x400000),
        FLASH_ID("win w25q32dw",   0xd8, 0xc7, 0x001660ef, 0x100, 0x10000, 0x400000),
        FLASH_ID("win w25q64cv",   0xd8, 0xc7, 0x001740ef, 0x100, 0x10000, 0x800000),
        FLASH_ID("win w25q128fv",  0xd8, 0xc7, 0x001840ef, 0x100, 0x10000, 0x1000000),
        FLASH_ID("gd gd25q20",     0x20, 0xc7, 0x00c84012, 0x100, 0x1000,  0x80000),
        FLASH_ID("gd gd25q16c",    0xd8, 0xc7, 0x001540c8, 0x100, 0x10000, 0x200000),
        FLASH_ID("gd gd25q32c",    0xd8, 0xc7, 0x001640c8, 0x100, 0x10000, 0x400000),
        FLASH_ID("gd gd25q128c",   0xd8, 0xc7, 0x001840c8, 0x100, 0x10000, 0x1000000),
"""
#       FLASH_ID("MX25R3235FM1I",  0xd8, 0xc7, 0x001628c2, 0x100, 0x1000,  0x400000), # x1/x2/x4 -- 32MBIT -- (1x 8 dummy, 2x 4 dummy, 4x, 2+4 dummy?)

regex=re.compile(
    'FLASH_ID\("([^"]*)",[^0]*0x(..), *0x([^,]*), *0x([^,]*), *0x([^,]*), *0x([^,]*), *0x([^)]*)\),')


# MX25R3235FM1I
# | Mode      | Cmd | Address ->  | Dummy -> | Data        |
# | READ      | 03  | SI          |   0      | SO          |
# | FAST_READ | 0B  | SI          |   8      | SO          |
# | DREAD     | 3B  | S0          |   8      | S0+S1       |
# | 2READ     | BB  | S0+S1       |   2+2    | S0+S1       |
# | QREAD     | 6B  | S0          |   8      | S0+S1+S2+S3 |
# | 4READ     | EB  | S0+S1+S2+S3 |   2+4    | S0+S1+S2+S3 |

# N25Q128

# Extended SPI? -- Depends on command, instruction always on one line
#
# DIO-SPI? -- Always use 2 data lines
# 0xBB, 0x3B, 0x0B
# QIO-SPI? -- Always use 4 data lines
# 0xEB, 0x6B, 0x0B
#
# Dummy bytes dependent on config in NVCR<15:12>
# MHz
# Dummy Clock FASTREAD DOFR DIOFR QOFR QIOFR
# 1 50 50 39 43 20
# 2 95 85 59 56 39
# 3 105 95 75 70 49
# 4 108 105 88 83 59
# 5 108 108 94 94 69
# 6 108 108 105 105 78
# 7 108 108 108 108 86
# 8 108 108 108 108 95
# 9 108 108 108 108 105
# 10 108 108 108 108 108



# | Board         | Flash Part              | Flash ID   | Component | Dummy  | Width | Notes
# |---------------+-------------------------+------------+-----------+--------+-------+-----------
# | arty          | Micron N25Q128A13ESF40  | 0x0018ba20 |           |   10   |       |
# | atlys         | Micron N25Q128          | 0x0018ba20 |           |   10   |       |
# | mimasv2       | M25P16                  | 0x00152020 | U1        |    8   |       |
# | minispartan6+ | Mac 25L6405             | 0x001720c2 |           |    4   |       |
# | netv2         | MX25R3235FM1IH0         | 0x001628c2 | U11C      |   ??   |       | Maybe n25q128 compatible? -- Connected through level shifter?
# | nexys_video   | Spansion S25FL256S      | 0x00190201 |           |   10?  |       |
# | opsis         | W25Q128FVEIG            | 0x0018ba20 | U3        |   10   |       |
# | pipistrello   | Micron N25Q128          | 0x0018ba20 |           |   10   |       |


for line in data.splitlines():
    line = line.strip()
    if not line:
        continue
    bits = regex.match(line)
    assert bits
    assert bits.groups()

    flash_name, erase_cmd, chip_erase_cmd, device_id, pagesize, sectorsize, size_in_bytes = bits.groups()
    erase_cmd = int(erase_cmd, 16)
    chip_erase_cmd = int(chip_erase_cmd, 16)
    device_id = int(device_id, 16)
    pagesize = int(pagesize, 16)
    sectorsize = int(sectorsize, 16)
    size_in_bytes = int(size_in_bytes, 16)

    flash_shortname = flash_name.split(flash_name, 1)[-1]

    print({'flash_name': flash_name, 'erase_cmd': erase_cmd, 'chip_erase_cmd': chip_erase_cmd, 'device_id': device_id, 'pagesize': pagesize, 'sectorsize':sectorsize, 'size_in_bytes': size_in_bytes})
