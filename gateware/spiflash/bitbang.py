
from litex.gen import *

from litex.soc.interconnect.csr import *


class SPIBitBang(Module, AutoCSR):
    def __init__(self, pads):
        spiwidth = len(pads.dqs)

        self.width = CSRConstant(spiwidth)
        self.enable = CSRStatus(1)
        self.cs_n = CSRStorage(1)
        self.clk = CSRStorage(spiwidth)
        self.dqs_oe = CSRStorage(spiwidth)
        self.dqs_in = CSRStatus(spiwidth)
        self.dqs_out = CSRStorage(spiwidth)

        dqs_tri = TSTriple(spiwidth)
        self.specials += dqs_tri.get_tristate(pads.dqs)
        self.comb += [
            If(self.enable,
                dqs_tri.oe.eq(self.dqs_oe),
            ).Else(
                dqs_tri.oe.eq(0),
            ),
            dq_tri.o.eq(self.dqs_o),
            dq_tri.i.eq(self.dqs_i),
        ]

        clk_tri = TSTriple(1)
        self.specials += cs_tri.get_tristate(pads.clk)
        self.comb += [
            clk_tri.oe.eq(self.enable),
            clk_tri.o.eq(self.clk),
        ]

        cs_tri = TSTriple(1)
        self.specials += cs_tri.get_tristate(pads.cs_n)
        self.comb += [
            cs_tri.oe.eq(self.enable),
            cs_tri.o.eq(self.cs_n),
        ]
