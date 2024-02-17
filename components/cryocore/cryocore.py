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

from typing import Optional

from m5.objects import (
    BaseCPU,
    BaseMMU,
    Port,
    Process,
)

from m5.objects.RiscvCPU import RiscvO3CPU

# just for x86 testing
#from m5.objects.X86CPU import X86O3CPU as RiscvO3CPU

# just for ARM testing
# from m5.objects.ArmCPU import ArmO3CPU as RiscvO3CPU

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.utils.requires import requires

class CryoIntFU(MinorDefaultIntFU):
    opLat = 1


class CryoIntMulFU(MinorDefaultIntMulFU):
    opLat = 3


class CryoIntDivFU(MinorDefaultIntDivFU):
    opLat = 6


class CryoFloatSimdFU(MinorDefaultFloatSimdFU):
    pass


class CryoPredFU(MinorDefaultPredFU):
    pass


class CryoMemReadFU(MinorDefaultMemFU):
    opClasses = minorMakeOpClassSet(["MemRead", "FloatMemRead"])
    opLat = 2


class CryoMemWriteFU(MinorDefaultMemFU):
    opClasses = minorMakeOpClassSet(["MemWrite", "FloatMemWrite"])
    opLat = 2


class CryoMiscFU(MinorDefaultMiscFU):
    pass


class CryoVecFU(MinorDefaultVecFU):
    pass


class CryoFUPool(MinorFUPool):
    funcUnits = [
        CryoIntFU(),
        CryoIntFU(),
        CryoIntMulFU(),
        CryoIntDivFU(),
        CryoFloatSimdFU(),
        CryoPredFU(),
        CryoMemReadFU(),
        CryoMemWriteFU(),
        CryoMiscFU(),
        CryoVecFU(),
    ]


class CryoBP(TournamentBP):
    # might need to replace with a different branch predictor
    btb = SimpleBTB(numEntries=32)
    ras = ReturnAddrStack(numEntries=12)
    localHistoryTableSize = 4096
    localPredictorSize = 16384
    globalPredictorSize = 16384
    choicePredictorSize = 16384
    localCtrBits = 4
    globalCtrBits = 4
    choiceCtrBits = 4
    indirectBranchPred = SimpleIndirectPredictor()
    indirectBranchPred.indirectSets = 16


class CryoCPU(RiscvO3CPU):
    # Fetch1 stage
    fetchToDecodeDelay = 1

    # Fetch2 stage
    decodeWidth = 4

    # Decode stage
    renameWidth = 4

    # Execute stage
    dispatchWidth = 4
    issueWidth = 4
    wbWidth = 4
    numPhysCCRegs = 10 # I got an error when I set this to 0; error was "src/cpu/o3/cpu.cc:206: gem5::o3::CPU::CPU(const gem5::BaseO3CPUParams&): Assertion `params.numPhysCCRegs >= numThreads * regClasses.at(CCRegClass)->numRegs()' failed."

    commitWidth = 4
    squashWidth = 4

    # from CryoCore paper
    cacheLoadPorts = 1  # Cache Ports. Constrains loads only.
    cacheStorePorts = 1  # Cache Ports. Constrains stores only.

    fetchWidth = 4  # Fetch width
    fetchQueueSize = 24  # Fetch queue size in micro-ops per-thread

    LQEntries = 24  # Number of load queue entries
    SQEntries = 24  # Number of store queue entries

    numIQEntries = 72  # Number of instruction queue entries
    numROBEntries = 96  # Number of reorder buffer entries

    numPhysIntRegs = 180  # Number of physical integer registers
    numPhysFloatRegs = 168  # Number of physical floating point registers

    # Assuming the total number of physical vector registers is the sum of the individual counts
    numPhysVecRegs = 100 + 100  # Number of physical vector registers

    # Assuming the total number of physical predicate registers is the given count
    numPhysVecPredRegs = 100  # Number of physical predicate registers

    # Assuming the total number of physical matrix registers is the given count
    numPhysMatRegs = 100  # Number of physical matrix registers

    # Setting other parameters (assuming default values for unspecified parameters)
    activity = 0  # Initial count
    decodeToFetchDelay = 1  # Decode to fetch delay
    renameToFetchDelay = 1  # Rename to fetch delay
    iewToFetchDelay = 1  # Issue/Execute/Writeback to fetch delay
    commitToFetchDelay = 1  # Commit to fetch delay

    smtNumFetchingThreads = 1  # SMT Number of Fetching Threads
    smtFetchPolicy = "RoundRobin"  # SMT Fetch policy
    smtLSQPolicy = "Partitioned"  # SMT LSQ Sharing Policy
    smtLSQThreshold = 100  # SMT LSQ Threshold Sharing Parameter
    smtIQPolicy = "Partitioned"  # SMT IQ Sharing Policy
    smtIQThreshold = 100  # SMT IQ Threshold Sharing Parameter
    smtROBPolicy = "Partitioned"  # SMT ROB Sharing Policy
    smtROBThreshold = 100  # SMT ROB Threshold Sharing Parameter
    smtCommitPolicy = "RoundRobin"  # SMT Commit Policy
    needsTSO = False  # Enable TSO Memory model


    # Functional Units and Branch Prediction
    executeFuncUnits = CryoFUPool()
    branchPred = CryoBP()


class CryoCore(BaseCPUCore):
    def __init__(
        self,
        core_id,
    ):
        super().__init__(core=CryoCPU(cpu_id=core_id), isa=ISA.RISCV)
        self.core.isa[0].enable_rvv = False


class CryoProcessor(BaseCPUProcessor):
    """
    A CryoProcessor contains a number of cores of CryoCore.
    """

    def __init__(
        self,
        num_cores: int = 1,
    ) -> None:
        self._cpu_type = CPUTypes.O3
        self._num_cores = num_cores
        super().__init__(cores=self._create_cores())

    def _create_cores(self):
        return [CryoCore(core_id=i) for i in range(self._num_cores)]
