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

from typing import Optional, Type, Union
from m5.objects import (
    SrcClockDomain,
    VoltageDomain,
    DRAMInterface,
    SubSystem,
)

from gem5.components.memory.memory import ChanneledMemory
from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
# from gem5.components.memory.dram_interfaces.ddr3 import DDR3_1600_8x8

class DDR3_1600_8x8(DRAMInterface):
    """
    A single DDR3-1600 x64 channel (one command and address bus), with
    timings based on a DDR3-1600 4 Gbit datasheet (Micron MT41J512M8) in
    an 8x8 configuration.
    """

    def __init__(self, clock: Optional[str] = None, **kwargs):
        super(DDR3_1600_8x8, self).__init__(**kwargs)

        # Optionally set the clock domain
        if clock is not None:
            self.clk_domain = SrcClockDomain(clock=clock, voltage_domain=VoltageDomain())

        # The rest of your class remains unchanged
        self.device_size = "512MiB"
        self.device_bus_width = 8
        self.burst_length = 8
        self.device_rowbuffer_size = "1KiB"
        self.devices_per_rank = 8
        self.ranks_per_channel = 2
        self.banks_per_rank = 8
        self.tCK = "1.25ns"
        self.tBURST = "5ns"
        self.tRCD = "13.75ns"
        self.tCL = "13.75ns"
        self.tRP = "13.75ns"
        self.tRAS = "35ns"
        self.tRRD = "6ns"
        self.tXAW = "30ns"
        self.activation_limit = 4
        self.tRFC = "260ns"
        self.tWR = "15ns"
        self.tWTR = "7.5ns"
        self.tRTP = "7.5ns"
        self.tRTW = "2.5ns"
        self.tCS = "2.5ns"
        self.tREFI = "7.8us"
        self.tXP = "6ns"
        self.tXS = "270ns"
        self.IDD0 = "55mA"
        self.IDD2N = "32mA"
        self.IDD3N = "38mA"
        self.IDD4W = "125mA"
        self.IDD4R = "157mA"
        self.IDD5 = "235mA"
        self.IDD3P1 = "38mA"
        self.IDD2P1 = "32mA"
        self.IDD6 = "20mA"
        self.VDD = "1.5V"

def create_clocked_memory_system(
    clock: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    Create a memory system with a clock domain.

    Args:
    size: The size of the memory system.
    dram_interface_class: The DRAM interface to use.
    num_channels: The number of channels to use.
    interleaving_size: The size of the interleaving.
    clock: The clock to use.

    Returns:
    The memory system.
    """
    if clock is not None:
        return DDR3_1600_8x8(clock=clock)
    return DDR3_1600_8x8()

    
def SingleChannelDDR3_1600WithClockDomain(size: str, clock: Optional[str] = None) -> AbstractMemorySystem:
    dram_interface_class = create_clocked_memory_system(clock=clock)
    return ChanneledMemory(size=size, dram_interface_class=dram_interface_class, num_channels=1, interleaving_size=64)
