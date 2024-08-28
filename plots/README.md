# Plots

This directory contains the data and plots for different configurations of the cryogenic components in gem5.

These configurations are `superconductingcorecryocache`, `superconductingcoresuperl1cryol2l3`, `superconductingcoresuperl1superl2cryol3`, `superconductingcorel1l2l3`, `superconductingeverything`.
They mean the following:
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

There are also in-order and out-of-order configurations for these configurations.

The plots can be seen in `plots.ipynb`.
