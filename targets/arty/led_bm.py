from litex.soc.cores.gpio import GPIOOut
from litex.soc.interconnect.csr import AutoCSR,CSRStorage
from litex.gen import *
from targets.arty.base import BaseSoC
from targets.utils import csr_map_update

class PWM(Module, AutoCSR):
    def __init__(self, pin, count_bits=12):
        counter = Signal(count_bits)

        self.on_val = CSRStorage(count_bits, write_from_dev=True)
        on_val_signal = self.on_val.storage

        self.sync += counter.eq(counter - 1)
        self.sync += If(counter == on_val_signal,
                        pin.eq(1))
        self.sync += If(counter == 0,
                        pin.eq(0))

class RGB(Module, AutoCSR):
    def __init__(self, r, g, b):
        self.rgb = CSRStorage(24)

        self.submodules.r = PWM(r, 8) #signal=self.rgb.on_val.storage[0:8])
        self.submodules.g = PWM(g, 8) #signal=self.rgb.on_val.storage[8:16])
        self.submodules.b = PWM(b, 8) #signal=self.rgb.on_val.storage[16:24])

        self.comb += self.r.on_val.we.eq(1)
        self.comb += self.g.on_val.we.eq(1)
        self.comb += self.b.on_val.we.eq(1)
        self.comb += self.r.on_val.dat_w.eq(self.rgb.storage[0:8])
        self.comb += self.g.on_val.dat_w.eq(self.rgb.storage[8:16])
        self.comb += self.b.on_val.dat_w.eq(self.rgb.storage[16:24])

#class BlinkerCPU(AutoCSR, Module):
    #def __init__(self, led):
        #self.submodules.leds = GPIOOut(led)

class BlinkSoC(BaseSoC):
    csr_peripherals = (
        "pwm", "rgb",
    )

    csr_map_update(BaseSoC.csr_map, csr_peripherals)

    def __init__(self, platform, *args, **kwargs):
        BaseSoC.__init__(self, platform, *args, **kwargs)
        led = platform.request("user_led", 1)
        rgb = platform.request("rgb_leds")

        self.submodules.pwm = PWM(led)
        self.submodules.rgb = RGB(rgb.r[0], rgb.g[0], rgb.b[0])

SoC = BlinkSoC
