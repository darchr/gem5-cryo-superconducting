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

from components.cryocache.private_l1_private_l2_shared_l3_cache_hierarchy import PrivateL1PrivateL2SharedL3CacheHierarchy

class AllSRAMOptCache(PrivateL1PrivateL2SharedL3CacheHierarchy):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            l1d_size="32kB",
            l1d_assoc=8,
            l1i_size="32kB",
            l1i_assoc=8,
            l2_size="256kB",
            l2_assoc=8,
            l3_size="8MB",
            l3_assoc=16,
            l1d_data_latency=2,
            l1i_data_latency=2,
            l2_data_latency=6,
            l3_data_latency=18,
            **kwargs
        )
        self._citations += '''@inproceedings{10.1145/3373376.3378513,
        author = {Min, Dongmoon and Byun, Ilkwon and Lee, Gyu-Hyeon and Na, Seongmin and Kim, Jangwoo},
        title = {CryoCache: A Fast, Large, and Cost-Effective Cache Architecture for Cryogenic Computing},
        year = {2020},
        isbn = {9781450371025},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3373376.3378513},
        doi = {10.1145/3373376.3378513},
        booktitle = {Proceedings of the Twenty-Fifth International Conference on Architectural Support for Programming Languages and Operating Systems},
        pages = {449–464},
        numpages = {16},
        keywords = {technology comparison and analysis, simulation, modeling, cryogenic computing, cryogenic cache},
        location = {Lausanne, Switzerland},
        series = {ASPLOS '20}
        }
        '''
