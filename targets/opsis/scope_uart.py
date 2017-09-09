from litex.gen import *

from litex.soc.cores.uart import UARTWishboneBridge

from litex.soc.integration.soc_core import mem_decoder
from litex.soc.integration.soc_sdram import *

from litescope import LiteScopeIO, LiteScopeAnalyzer

from targets.utils import csr_map_update
from targets.opsis.base import SoC as BaseSoC


class UARTScopeSoC(BaseSoC):

    csr_peripherals = (
        "analyzer",
        "io",
    )
    csr_map_update(BaseSoC.csr_map, csr_peripherals)

    def __init__(self, platform, **kwargs):
        kwargs['cpu_type'] = None
        BaseSoC.__init__(self, platform,
            ident="Litescope using EtherBone",
            with_uart=False,
            with_timer=False,
            **kwargs,
        )

        self.submodules.io = LiteScopeIO(8)
        for i in range(8):
            try:
                self.comb += platform.request("user_led", i).eq(self.io.output[i])
            except:
                pass

        # use name override to keep naming in capture
        counter = Signal(4, name_override="counter")
        counter0 = Signal(name_override="counter0")
        counter1 = Signal(name_override="counter1")
        counter2 = Signal(name_override="counter2")
        counter3 = Signal(name_override="counter3")
        self.sync += counter.eq(counter + 1)
        self.comb += [
            counter0.eq(counter[0]),
            counter1.eq(counter[1]),
            counter2.eq(counter[2]),
            counter3.eq(counter[3]),
        ]

        # group for vcd capture
        vcd_group = [
            counter
        ]
        # group for sigrok capture (no bus support)
        sigrok_group = [
            counter0,
            counter1,
            counter2,
            counter3
        ]
        analyzer_signals = {
            0 : vcd_group,
            1 : sigrok_group
        }
        self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals, 512)

        self.add_cpu_or_bridge(UARTWishboneBridge(platform.request("fx2_serial"), self.clk_freq, baudrate=115200))
        self.add_wb_master(self.cpu_or_bridge.wishbone)

    def do_exit(self, vns, filename="test/analyzer.csv"):
        self.analyzer.export_csv(vns, filename)


SoC = UARTScopeSoC
