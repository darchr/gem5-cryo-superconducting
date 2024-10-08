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


def run_different_clock_domains(config, workload, clock_freq):

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
    from components.cryocore.in_order_cryocore import CryoInOrderProcessor
    from components.cryocache.private_l1_private_l2_shared_l3_cache_hierarchy import PrivateL1PrivateL2SharedL3CacheHierarchy
    from components.cryocache.cryocache import CryoCache

    if config == "superconductingcorecryocache":
        cache_hierarchy = CryoCache(l1d_clock="4GHz", l1i_clock="4GHz", l2_clock="4GHz", l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )
    
    if config == "cryocorecryocache":
        cache_hierarchy = CryoCache(l1d_clock="4GHz", l1i_clock="4GHz", l2_clock="4GHz", l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock="4GHz")

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "superconductingcoresuperl1cryol2l3":
        cache_hierarchy = CryoCache(l1d_clock=clock_freq, l1i_clock=clock_freq, l2_clock="4GHz", l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "superconductingcoresuperl1superl2cryol3":
        cache_hierarchy = CryoCache(l1d_clock=clock_freq, l1i_clock=clock_freq, l2_clock=clock_freq, l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )
    
    if config == "superconductingcorel1l2l3":
        cache_hierarchy = CryoCache(l1d_clock=clock_freq, l1i_clock=clock_freq, l2_clock=clock_freq, l3_clock=clock_freq)

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "superconductingeverything":
        cache_hierarchy = CryoCache(l1d_clock=clock_freq, l1i_clock=clock_freq, l2_clock=clock_freq, l3_clock=clock_freq)

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq=clock_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "cryoinordercorecryocache":
        cache_hierarchy = CryoCache(l1d_clock="4GHz", l1i_clock="4GHz", l2_clock="4GHz", l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoInOrderProcessor(num_cores=2, clock="4GHz")

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "superinordercoresupercache":
        cache_hierarchy = CryoCache(l1d_clock=clock_freq, l1i_clock=clock_freq, l2_clock=clock_freq, l3_clock=clock_freq)

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoInOrderProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq=clock_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    if config == "superinordercorecryocache":
        cache_hierarchy = CryoCache(l1d_clock="4GHz", l1i_clock="4GHz", l2_clock="4GHz", l3_clock="4GHz")

        memory = SingleChannelDDR3_1600(size="8GB")

        processor = CryoInOrderProcessor(num_cores=2, clock=clock_freq)

        board = SimpleBoard(
            clk_freq="1GHz",
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )



    print(f"Running {workload.get_id()} on {config} configuration")
    board.set_workload(workload)
    
    # Lastly we run the simulation.
    simulator = Simulator(board=board)
    simulator.run()