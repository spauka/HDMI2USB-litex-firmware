from litex.gen import *
from litex.soc.interconnect.csr import *

class PWM(Module):
    def __init__(self, pin, period, count_bits=12):
        counter = Signal(count_bits)
        on_val = CSRStorage(count_bits)

        self.sync += counter.eq(counter - 1)
        self.sync += If(counter == on_val.storage,
                        pin.eq(~pin))
        self.comb += on_val.storage.eq(2**11)

class Blinker(Module):
    def __init__(self, led, sw1, sw2):
        self.comb += [
            led.eq(sw1 ^ sw2),
        ]

class BlinkSoC(Module):
    cpu_type = None

    def __init__(self, platform, *args, **kwargs):
        led = platform.request("user_led")
        led2 = platform.request("user_led")
        sw1 = platform.request("user_sw")
        sw2 = platform.request("user_sw")
        rgb = platform.request("rgb_leds")
        self.comb += rgb.r[0].eq(1)
        self.comb += led2.eq(1)
        self.submodules.blinker = \
                PWM(led, 0.99)
                #Blinker(led, sw1, sw2)

SoC = BlinkSoC
