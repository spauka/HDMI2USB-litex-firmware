#!/usr/bin/env python3

from litescope.software.driver.analyzer import LiteScopeAnalyzerDriver
from common import *

def main():
    args, wb = connect("LiteScope Analyzer Test")
    print_memmap(wb)
    print()

    analyzer_csv = '{}/analyzer.csv'.format(make_testdir(args))
    analyzer = LiteScopeAnalyzerDriver(wb.regs, "analyzer", config_csv=analyzer_csv, debug=True)
    print("Configuring...")
    analyzer.configure_trigger(cond={})
    analyzer.configure_subsampler(1)
    analyzer.run(offset=16, length=int(analyzer.depth/2))
    print("Waiting...", end="", flush=True)
    while not analyzer.done():
        print(".")
        time.sleep(1)
    print()
    print("Downloading...")
    analyzer.upload()
    print("Saving...")
    analyzer.save("dump.vcd")
    analyzer.save("dump.sr")
    print("Exiting..")
    wb.close()


if __name__ == "__main__":
    main()
