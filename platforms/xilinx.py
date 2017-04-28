
import math

class XilinxGatewareSize(object):

    data = """\
# This data comes from "Table 1-1: Bitstream Length" in the "7 Series FPGAs
# Configuration User Guide UG470 (v1.11) September 27, 2016"
# https://www.xilinx.com/support/documentation/user_guides/ug380.pdf
# ------------------------------------------------------------------------
# Device, Gateware Size (bits), Minimum Flash Size (Megabits), JTAG IDCODE[31:0]
# Spartan-7 Family
7S6 4310752 8 0x3622093
7S15 4310752 8 0x3620093
7S25 9934432 16 0x37C4093
7S50 17536096 32 0x362F093
7S75 29494496 32 0x37C8093
7S100 29494496 32 0x37C7093
# Artix-7 Family
7A12T 9934432 16 0x37C3093
7A15T 17536096 32 0x362E093
7A25T 9934432 16 0x37C2093
7A35T 17536096 32 0x362D093
7A50T 17536096 32 0x362C093
7A75T 30606304 32 0x3632093
7A100T 30606304 32 0x3631093
7A200T 77845216 128 0x3636093
# Kintex-7 Family
7K70T 24090592 32 0x3647093
7K160T 53540576 64 0x364C093
7K325T 91548896 128 0x3651093
7K355T 112414688 128 0x3747093
7K410T 127023328 128 0x3656093
7K420T 149880032 256 0x3752093
7K480T 149880032 256 0x3751093
# Virtex-7 Family
7V585T 161398880 256 0x3671093
7V2000T 447337216 512 0x36B3093
7VX330T 111238240 128 0x3667093
7VX415T 137934560 256 0x3682093
7VX485T 162187488 256 0x3687093
7VX550T 229878496 256 0x3692093
# ------------------------------------------------------------------------

# The gateware size data comes from "Table 5-5: Spartan-6 FPGA Bitstream
# Length" in the "Spartan-6 FPGA Configuration User Guide UG380 (v2.10) March
# 31, 2017"
# https://www.xilinx.com/support/documentation/user_guides/ug380.pdf
6SLX4 2731488
6SLX9 2742528
6SLX16 3731264
6SLX25 6440432
6SLX25T 6440432
6SLX45 11939296
6SLX45T 11939296
6SLX75 19719712
6SLX75T 19719712
6SLX100 26691232
6SLX100T 26691232
6SLX150 33909664
6SLX150T 33909664
"""

#  2742528/8   0x53b20 -> 0x080000  mimasv2
#  6440432/8   0xc48be -> 0x100000  minispartan6 with lx25
# 11939296/8  0x16c5bc -> 0x200000  opsis/atlys
# 17536096/8  0x21728c -> 0x220000  arty

    @staticmethod
    def minimum_size(s):
        return 2**math.ceil(math.log2(s/(1024*1024)))
        i = 1
        while (2**i) * (1024 * 1024) < s:
            i += 1
        return 2**i

    def __init__(self):
        def split(l, n):
            o = l.split(' ')
            while len(o) < n:
                o.append(None)
            return o

        for line in self.data.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue

            part, gateware_bits, flash_size, idcode = split(line, 4)
            gateware_bits = int(gateware_bits)

            calc_flash_size = self.minimum_size(gateware_bits)
            if flash_size:
                flash_size = int(flash_size)
                assert calc_flash_size == flash_size

            flash_size_bits = calc_flash_size*1024*1024
            spare_bits = flash_size_bits - gateware_bits
            #bios_offset = 

            print("%r %r %r (spare %.02fMbits)" %(part, gateware_bits, hex(calc_flash_size*1024*1024), (spare_bits/1024/1024)))


if __name__ == "__main__":
    XilinxGatewareSize()
