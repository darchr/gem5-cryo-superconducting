# Cryogenic Computing and Superconducting Circuits with gem5

This repository contains the gem5 models for cryogenic components.
The repository is a part of the project to model cryogenic computing and superconducting circuits in gem5.

The cryogenic cache has been adapted from the [CryoCache: A fast, large, and cost-effective cache architecture for cryogenic computing](https://dl.acm.org/doi/pdf/10.1145/3373376.3378513) paper by Min et al.

The cryogenic core has been adapted from the [CryoCore: A High-Performance Cryogenic Processor](https://ieeexplore.ieee.org/iel7/9136582/9138908/09138996.pdf) paper by Byun and Min et al.

## Working with This Repository

To checkout (with all submodules) use:
```bash
git clone --recurse-submodules https://github.com/darchr/gem5-cryo-superconducting.git
```

If you checked out this repo without `--recurse-submodules` then you can run the following to sync the `gem5/` directory.

```sh
git submodule update --init
```

When needed, to update the submodule, run the following command.

```sh
git submodule update --remote gem5
```

## Building gem5

After checking out the gem5 directory (See [above](#working-with-this-repository)), you need to compile gem5 with the RISC-V ISA.

```bash
cd gem5
scons build/RISCV/gem5.opt -j `nproc`
```

## Running a Workload
To run a workload, you can use the `cryo-hello.py` script. 
This script runs a simple hello world program on a board with a cryogenic core and cache.
To change the workload, you can modify the `board.set_se_binary_workload(obtain_resource("riscv-hello"))` line in the script.
Replace `riscv-hello` with the ID of the workload you want to run.
Note that this assumes that the resource you want to run is part of the `gem5-resources` infrastructure, and can be found on the `gem5-resources` [website](http://resources.gem5.org/).

You can run the workload using the following command:
```bash
./gem5/build/RISCV/gem5.opt scripts/cryo-hello.py
```

The above script assumes all the components of the board are in the same clock domain.

If you want to run a workload with components in different clock domains, you can use the `cryo-clock-domains.py` script.
This script runs the same workload as `cryo-hello.py`, but with the core, L1, L2 and L3 caches in different clock domains.

You can run the workload using the following command:
```bash
./gem5/build/RISCV/gem5.opt scripts/cryo-clock-domains.py
```

## Running a Suite (Group of Workloads)
To run a suite of workloads, you can use the `cryo-suite.py` script.
This script runs a suite of workloads on a board with a cryogenic core and cache, defined in the `workloads` list in the script.
To change the workloads, you can modify the `workloads` list in the script.
Replace the IDs in the list with the IDs of the workloads you want to run.
The workloads used for our experiment have their metadata defined in the `getting_started_riscv.json` file.

The suite script accepts two command line arguments:
- `--clk_freq` to set the clock frequency of the components in the board which are in the superconducting clock domain.
The other components are assumed to be in the cryogenic clock domain, and their clock frequency is set to a constant value of 4 GHz.
- `--config` to set the configuration of the board.
This is used to decide which components are in the superconducting clock domain and which are in the cryogenic clock domain.
The valid values for this argument are `superconductingcorecryocache`, `superconductingcoresuperl1cryol2l3`, `superconductingcoresuperl1superl2cryol3`, `superconductingcorel1l2l3`, `superconductingeverything`.
These values correspond to the following configurations:
  - `superconductingcorecryocache`: The core is in the superconducting clock domain, and the L1, L2 and L3 caches are in the cryogenic clock domain.
  The board is at 1 GHz, and the memory is at its default frequency of 800 MHz.
  - `superconductingcoresuperl1cryol2l3`: The core and L1 cache are in the superconducting clock domain, and the L2 and L3 caches are in the cryogenic clock domain.
  The board is at 1 GHz, and the memory is at its default frequency of 800 MHz.
  - `superconductingcoresuperl1superl2cryol3`: The core and L1 and L2 caches are in the superconducting clock domain, and the L3 cache is in the cryogenic clock domain.
  The board is at 1 GHz, and the memory is at its default frequency of 800 MHz.
  - `superconductingcorel1l2l3`: The core, L1, L2 and L3 caches are in the superconducting clock domain.
  The board is at 1 GHz, and the memory is at its default frequency of 800 MHz.
  - `superconductingeverything`: The core, L1, L2 and L3 caches and the board are in the superconducting clock domain.
    The memory is at its default frequency of 800 MHz.

To see the above configurations in detail, you can refer to the `components/util/run_different_clock_domains.py` script, and potentially modify it to create your own configurations.

You can run the suite using the following command:
```bash
GEM5_RESOURCE_JSON_APPEND=./getting_started_riscv.json ./gem5/build/RISCV/gem5.opt scripts/cryo-suite.py --clk_freq 4GHz --config superconductingcorecryocache
```

## Directory Structure
- `components/`: Contains the cryogenic components.
  - `cryocore/`: Contains the cryogenic core.
    - `cryocore.py`: Contains the model for the cryogenic core.
  - `cryocache/`: Contains the cryogenic cache.
    - `cryocache.py`: Contains the model for the cryogenic cache.
    - `alledramcache.py`: Contains the model for the all EDRAM cache described in the CryoCache paper.
    - `allsramoptcache.py`: Contains the model for the all SRAM optimized cache described in the CryoCache paper.
    - `allsramnooptcache.py`: Contains the model for the all SRAM non-optimized cache described in the CryoCache paper.
  - `util/`: Contains utility scripts to run the suite of workloads with components in different clock domains.
    - `run_different_clock_domains.py`: Contains the script to run a workload with components in different clock domains.
    - `run_binary.py`: Contains the script to run a workload with components in the same clock domain.
- `scripts/`: Contains the scripts to run workloads and suites.
    - `cryo-hello.py`: Contains the script to run a simple hello world program on a board with a cryogenic core and cache.
    - `cryo-clock-domains.py`: Contains the script to run a workload with components in different clock domains.
    - `cryo-suite.py`: Contains the script to run a suite of workloads on a board with a cryogenic core and cache.
- `plots/`: Contains the plots generated from the experiment.
There are different directories for different configurations of the board as described in the [`--config` argument of the `cryo-suite.py` script](#running-a-suite-group-of-workloads), for clock frequencies of 4 GHz, 10 GHz, 20 GHz, 50 GHz and 100 GHz.
The plots are in Python notebooks inside these directories.
- `gem5/`: Contains the gem5 source code.
- `getting_started_riscv.json`: Contains the metadata for the workloads used in our experiment.
- `README.md`: Contains the documentation for the repository.

## Citation
If you use this repository in your research, please cite the following paper:

```
@misc{pai2024potentiallimitationhighfrequencycores,
      title={Potential and Limitation of High-Frequency Cores and Caches}, 
      author={Kunal Pai and Anusheel Nand and Jason Lowe-Power},
      year={2024},
      eprint={2408.03308},
      archivePrefix={arXiv},
      primaryClass={cs.AR},
      url={https://arxiv.org/abs/2408.03308}, 
}
```
