from litex.gen import *

from litex.soc.integration.soc_core import mem_decoder
from litex.soc.integration.soc_sdram import *

from liteeth.common import convert_ip
from gateware.s6rgmii import LiteEthPHYRGMII
from liteeth.core import LiteEthUDPIPCore
from liteeth.frontend.etherbone import LiteEthEtherbone

from litescope import LiteScopeIO, LiteScopeAnalyzer

from targets.utils import csr_map_update
from targets.atlys.base import SoC as BaseSoC


class EthScopeSoC(BaseSoC):

    csr_peripherals = (
        "ethphy",
        "ethcore",
        "analyzer",
        "io",
    )
    csr_map_update(BaseSoC.csr_map, csr_peripherals)

    def __init__(self, platform, **kwargs):
        kwargs['cpu_type'] = None
        BaseSoC.__init__(self, platform,
            ident="Litescope using EtherBone",
            with_timer=False,
            **kwargs)

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

        # Ethernet PHY and UDP/IP stack
        mac_address=0x10e2d5000000
        ip_address="192.168.100.50"

        self.submodules.ethphy = LiteEthPHY(
            platform.request("eth_clocks"),
            platform.request("eth"),
            self.clk_freq)

        self.submodules.ethcore = LiteEthUDPIPCore(
            self.ethphy,
            mac_address,
            convert_ip(ip_address),
            self.clk_freq,
            with_icmp=True)

        # Etherbone bridge
        self.submodules.etherbone = LiteEthEtherbone(self.ethcore.udp, 1234, mode="master")
        self.add_cpu_or_bridge(self.etherbone)
        self.add_wb_master(self.etherbone.wishbone.bus)

        self.ethphy.crg.cd_eth_rx.clk.attr.add("keep")
        self.ethphy.crg.cd_eth_tx.clk.attr.add("keep")
        self.platform.add_period_constraint(self.ethphy.crg.cd_eth_rx.clk, 8.0)

        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.ethphy.crg.cd_eth_rx.clk,
        )

        self.platform.add_platform_command("""
# FIXME: ERROR:Place:1108 - A clock IOB / BUFGMUX clock component pair have
# been found that are not placed at an optimal clock IOB / BUFGMUX site pair.
# The clock IOB component <eth_clocks_rx> is placed at site <K15>.
NET "{eth_clocks_rx}" CLOCK_DEDICATED_ROUTE = FALSE;
# The IOB component <eth_clocks_tx> is placed at site <K16>.
NET "{eth_clocks_tx}" CLOCK_DEDICATED_ROUTE = FALSE;
""",
            eth_clocks_rx=platform.lookup_request("eth_clocks").rx,
            eth_clocks_tx=platform.lookup_request("eth_clocks").tx,
        )

    def configure_iprange(self, iprange):
        iprange = [int(x) for x in iprange.split(".")]
        while len(iprange) < 4:
            iprange.append(0)
        # Our IP address
        self._configure_ip("LOCALIP", iprange[:-1]+[50])
        # IP address of tftp host
        self._configure_ip("REMOTEIP", iprange[:-1]+[100])

    def _configure_ip(self, ip_type, ip):
        for i, e in enumerate(ip):
            s = ip_type + str(i + 1)
            s = s.upper()

    def do_exit(self, vns, filename="test/analyzer.csv"):
        self.analyzer.export_csv(vns, filename)


SoC = EthScopeSoC
