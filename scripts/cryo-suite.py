# Copyright (c) 2024 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This gem5 configuation script creates a simple board to run a RISC-V
"hello world" binary using a processor model that implements the
CryoCore described in the paper "CryoCore: A Fast and Dense Processor 
Architecture for Cryogenic Computing" by Byun, et al. (ISCA 2020).


Usage
-----

```
cd gem5
scons build/RISCV/gem5.opt
cd ..
./gem5/build/RISCV/gem5.opt scripts/cryocore-suite.py
```
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
from gem5.resources.resource import CustomResource, FileResource
from time import sleep
from gem5.utils.multiprocessing import Process
import argparse

import sys
from pathlib import Path

# Get the directory containing the current file
here = Path(__file__).parent

# Add the parent directory of `here` to the Python path
sys.path.append(str(here.parent))

from components.cryocore.cryocore import CryoProcessor
from components.cryocache.private_l1_private_l2_shared_l3_cache_hierarchy import PrivateL1PrivateL2SharedL3CacheHierarchy
from components.cryocache.cryocache import CryoCache
from components.util.run_binary import run_binary
from components.util.run_different_clock_domains import run_different_clock_domains

argparser = argparse.ArgumentParser()
argparser.add_argument("--config", type=str, default="default", help="Configuration to run")
argparser.add_argument("--clk_freq", type=str, default="4GHz", help="Clock frequency")

# construct the board depending on the argparser
args = argparser.parse_args()

clock_freq = args.clk_freq



if __name__ == "__m5_main__":
    #workloads = [ workload for workload in obtain_resource("riscv-getting-started-benchmark-suite") ]
    workloads = [ obtain_resource("riscv-npb-cg-size-s-run"),  
                obtain_resource("riscv-npb-bt-size-s-run"),
                obtain_resource("riscv-npb-is-size-s-run"), 
                obtain_resource("riscv-npb-lu-size-s-run"),
                obtain_resource("riscv-npb-ft-size-s-run"),
                obtain_resource("riscv-gapbs-bfs-run"),
                obtain_resource("riscv-gapbs-tc-run"),
                obtain_resource("riscv-llvm-minisat-run"),
    ]
    processes = []
    for i, bm in enumerate(workloads):
        print(f"Running {bm.get_id()} on CryoCore")
        if len(processes) > 9:
            for process in processes:
                if not process.is_alive():
                    processes.remove(process)
            sleep(10)
        process = Process(target=run_different_clock_domains, args=(args.config,bm,clock_freq), name=bm.get_id())
        # process = Process(target=run_binary, args=(args.config,bm), name=bm.get_id())
        process.start()
        processes.append(process)
        if i == 9:
            break

    while processes:
        for process in processes:
            if not process.is_alive():
                processes.remove(process)
        sleep(10)