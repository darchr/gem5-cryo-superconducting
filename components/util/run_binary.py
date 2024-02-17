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

def run_binary(config, benchmark):

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

    if config == "cryoall":
        cache_hierarchy = CryoCache()

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2)

        board = SimpleBoard(
            clk_freq="4GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "cryocore":
        cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
            l1d_size="32kB",
            l1d_assoc=8,
            l1i_size="32kB",
            l1i_assoc=8,
            l2_size="256kB",
            l2_assoc=8,
            l3_size="8MB",
            l3_assoc=16,
        )

        memory = SingleChannelDDR3_1600(size="8GB")

        processor =  CryoProcessor(num_cores=2)

        board = SimpleBoard(
            clk_freq="4GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "cryocache":
        cache_hierarchy = CryoCache()

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.RISCV, num_cores=2)

        board = SimpleBoard(
            clk_freq="4GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "default":
        cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
            l1d_size="32kB",
            l1d_assoc=8,
            l1i_size="32kB",
            l1i_assoc=8,
            l2_size="256kB",
            l2_assoc=8,
            l3_size="8MB",
            l3_assoc=16,
        )

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.RISCV, num_cores=2)

        board = SimpleBoard(
            clk_freq="4GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    # I don't like this, but it's the only way to get the benchmarks to work since they need arguments and input files
    if benchmark == "minisat":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/llvm-test-suite/build/MultiSource/Applications/minisat/minisat"), arguments=["-verbosity=0"], stdin_file=FileResource("/home/paikunal/personal/llvm-test-suite/build/MultiSource/Applications/minisat/short.cnf")
        )
    if benchmark == "npb-bt":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/serial-binaries/bt.S.x")
        )
    if benchmark == "npb-cg":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/serial-binaries/cg.S.x")
        )
    if benchmark == "npb-ft":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/serial-binaries/ft.S.x")
        )
    if benchmark == "npb-lu":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/serial-binaries/lu.S.x")
        )
    if benchmark == "npb-is":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/NPB3.3-SER/bin/is.S.x")
        )
    if benchmark == "npb-mg":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/NPB3.3.1/serial-binaries/mg.S.x")
        )
    if benchmark == "gapbs-bfs":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/gapbs/bfs"), arguments=["-g", "10", "-n", "1"]
        )
    if benchmark == "gapbs-tc":
        board.set_se_binary_workload(
            CustomResource("/home/paikunal/personal/second-gem5/gapbs/tc"), arguments=["-g", "20", "-n", "10"]
        )
    
    # Lastly we run the simulation.
    simulator = Simulator(board=board)
    simulator.run()
