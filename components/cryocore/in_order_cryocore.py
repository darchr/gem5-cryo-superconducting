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
    SrcClockDomain,
    VoltageDomain,
)
from m5.objects.BaseMinorCPU import *
from m5.objects.RiscvCPU import RiscvMinorCPU

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

class InOrderCryoCPU(RiscvMinorCPU):
    """
    The fetch, decode, and execute stage parameters from the ARM HPI CPU
    This information about the CPU can be found on page 15 of
    `gem5_rsk_gem5-21.2.pdf` at https://github.com/arm-university/arm-gem5-rsk

    The parameters that are changed are:
    - threadPolicy:
        This is initialized to "SingleThreaded".
    - decodeToExecuteForwardDelay:
        This is changed from 1 to 2 to avoid a PMC address fault.
    - fetch1ToFetch2BackwardDelay:
        This is changed from 1 to 0 to better match hardware performance.
    - fetch2InputBufferSize:
        This is changed from 2 to 1 to better match hardware performance.
    - decodeInputBufferSize:
        This is changed from 3 to 2 to better match hardware performance.
    - decodeToExecuteForwardDelay:
        This is changed from 2 to 1 to better match hardware performance.
    - executeInputBufferSize:
        This is changed from 7 to 4 to better match hardware performance.
    - executeMaxAccessesInMemory:
        This is changed from 2 to 1 to better match hardware performance.
    - executeLSQStoreBufferSize:
        This is changed from 5 to 3 to better match hardware performance.
    - executeBranchDelay:
        This is changed from 1 to 2 to better match hardware performance.
    - enableIdling:
        This is changed to False to better match hardware performance.

    """

    threadPolicy = "SingleThreaded"

    # Fetch1 stage
    fetch1LineSnapWidth = 0
    fetch1LineWidth = 0
    fetch1FetchLimit = 1
    fetch1ToFetch2ForwardDelay = 1
    fetch1ToFetch2BackwardDelay = 0

    # Fetch2 stage
    fetch2InputBufferSize = 1
    fetch2ToDecodeForwardDelay = 1
    fetch2CycleInput = True

    # Decode stage
    decodeInputBufferSize = 2
    decodeToExecuteForwardDelay = 1
    decodeInputWidth = 2
    decodeCycleInput = True

    # Execute stage
    executeInputWidth = 2
    executeCycleInput = True
    executeIssueLimit = 2
    executeMemoryIssueLimit = 1
    executeCommitLimit = 2
    executeMemoryCommitLimit = 1
    executeInputBufferSize = 4
    executeMaxAccessesInMemory = 1
    executeLSQMaxStoreBufferStoresPerCycle = 2
    executeLSQRequestsQueueSize = 1
    executeLSQTransfersQueueSize = 2
    executeLSQStoreBufferSize = 3
    executeBranchDelay = 2
    executeSetTraceTimeOnCommit = True
    executeSetTraceTimeOnIssue = False
    executeAllowEarlyMemoryIssue = True
    enableIdling = False

    # Functional Units and Branch Prediction
    executeFuncUnits = CryoFUPool()
    branchPred = CryoBP()

class CryoInOrderCore(BaseCPUCore):
    def __init__(
        self,
        core_id,
    ):
        super().__init__(core=InOrderCryoCPU(cpu_id=core_id), isa=ISA.RISCV)
        self.core.isa[0].enable_rvv = False

class CryoInOrderProcessor(BaseCPUProcessor):
    """
    A CryoProcessor contains a number of cores of CryoCore.
    """

    def __init__(
        self,
        num_cores: int = 1,
        clock: str = "4GHz"
    ) -> None:
        self._cpu_type = CPUTypes.O3
        self._num_cores = num_cores
        self._clock = clock
        super().__init__(cores=self._create_cores())

    def _create_cores(self):
        cores = [CryoInOrderCore(core_id=i) for i in range(self._num_cores)]
        for core in cores:
            core.clk_domain = SrcClockDomain(clock=self._clock, voltage_domain=VoltageDomain())
        return cores
