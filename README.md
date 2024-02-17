# gem5-cryo-supercomputing
For the gem5 + cryo + supercomputing project

# Run gem5 with cryo

1. Compile gem5 with RISC-V ISA
```bash
scons build/RISCV/gem5.opt -j8
```

2. Run cryo-suite.py
```bash
GEM5_RESOURCE_JSON_APPEND=/home/paikunal/personal/cryo/gem5-cryo-supercomputing/getting_started_riscv.json ./gem5/build/RISCV/gem5.opt scripts/cryo-suite.py 
```
