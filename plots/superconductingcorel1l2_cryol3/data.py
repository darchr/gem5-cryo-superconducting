import os
import pandas as pd
import numpy as np
import argparse


# list all the folders in the directory
def list_folders(path):
    folders = os.listdir(path)
    return [folder for folder in folders if os.path.isdir(folder)]

def process_data(folders):
    microbench_data = {}
    for folder in folders:
        # print(folder)
        files = os.listdir(folder)
        for file in files:
            if os.path.isdir(file) or file != 'stats.txt':
                continue
            with open(os.path.join(folder, file), 'r') as f:
                cycle = None
                instret = None
                seconds = None
                l1dAccesses = 0
                l1iAccesses = 0
                l2Accesses = 0
                l3Accesses = 0
                l1dmisses = 0
                l1imisses = 0
                l2misses = 0
                l3misses = 0
                l1dhits = 0
                l1ihits = 0
                l2hits = 0
                l3hits = 0
                lsq = 0
                microbench_name = folder.split('.')[0]
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if "board.processor.cores0.core.numCycles" in line:
                        print(line)
                        if cycle is None:
                            cycle = line.split()[1]
                    if "simInsts" in line and "NotNOP" not in line:
                        print(line)
                        if instret is None:
                            instret = line.split()[1]
                    if "simSeconds" in line:
                        print(line)
                        if seconds is None:
                            seconds = line.split()[1]
                    if "board.cache_hierarchy.l1dcaches0.overallAccesses::total" in line or "board.cache_hierarchy.l1dcaches1.overallAccesses::total" in line:
                        print(line)
                        print(line.split())
                        l1dAccesses += int(line.split()[1]) 
                    if "board.cache_hierarchy.l1icaches0.overallAccesses::total" in line or "board.cache_hierarchy.l1icaches1.overallAccesses::total" in line:
                        print(line)
                        l1iAccesses += int(line.split()[1])
                    if "board.cache_hierarchy.l2caches0.overallAccesses::total" in line or "board.cache_hierarchy.l2caches1.overallAccesses::total" in line:
                        print(line)
                        print(line.split())
                        l2Accesses += int(line.split()[1])
                    if "board.cache_hierarchy.l3cache.overallAccesses::total" in line:
                        print(line)
                        l3Accesses += int(line.split()[1])
                    if "board.cache_hierarchy.l1dcaches0.overallMisses::total" in line or "board.cache_hierarchy.l1dcaches1.overallMisses::total" in line:
                        print(line)
                        l1dmisses += int(line.split()[1])
                    if "board.cache_hierarchy.l1icaches0.overallMisses::total" in line or "board.cache_hierarchy.l1icaches1.overallMisses::total" in line:
                        print(line)
                        l1imisses += int(line.split()[1])
                    if "board.cache_hierarchy.l2caches0.overallMisses::total" in line or "board.cache_hierarchy.l2caches1.overallMisses::total" in line:
                        print(line)
                        l2misses += int(line.split()[1])
                    if "board.cache_hierarchy.l3cache.overallMisses::total" in line:
                        print(line)
                        l3misses += int(line.split()[1])

                    if "board.cache_hierarchy.l1dcaches0.overallHits::total" in line or "board.cache_hierarchy.l1dcaches1.overallHits::total" in line:
                        print(line)
                        l1dhits += int(line.split()[1])
                    if "board.cache_hierarchy.l1icaches0.overallHits::total" in line or "board.cache_hierarchy.l1icaches1.overallHits::total" in line:
                        print(line)
                        l1ihits += int(line.split()[1])
                    if "board.cache_hierarchy.l2caches0.overallHits::total" in line or "board.cache_hierarchy.l2caches1.overallHits::total" in line:
                        print(line)
                        l2hits += int(line.split()[1])
                    if "board.cache_hierarchy.l3cache.overallHits::total" in line:
                        print(line)
                        l3hits += int(line.split()[1])

                    if "board.processor.cores0.core.iew.lsqFullEvents" in line or "board.processor.cores1.core.iew.lsqFullEvents" in line:
                        print(line)
                        lsq += int(line.split()[1])
                try:
                    microbench_data[microbench_name] = {
                        'Cycles': cycle,
                        'Instructions': instret,
                        'IPC': float(instret) / float(cycle),
                        'Seconds': seconds,
                        'l1dAccesses' : l1dAccesses,
                        'l1iAccesses' : l1iAccesses,
                        'l2Accesses' : l2Accesses,
                        'l3Accesses' : l3Accesses,
                        'l1dmisses' : l1dmisses,
                        'l1imisses' : l1imisses,
                        'l2misses' : l2misses,
                        'l3misses' : l3misses,
                        'l1dhits' : l1dhits,
                        'l1ihits' : l1ihits,
                        'l2hits' : l2hits,
                        'l3hits' : l3hits,
                        'lsqFullEvents' : lsq
                    }
                except Exception as e:
                    print("Error in file: ", file)
                    print(e)
                    pass
    return microbench_data

# df = pd.DataFrame.from_dict(process_data(list_folders('.')), orient='index')

args = argparse.ArgumentParser()
args.add_argument('--frequency', type=int, default=4)
# args.add_argument('--folder', type=str, default='.')
args = args.parse_args()
# print(os.getcwd())
# os.system(f'cd superconductingcorecryocache-{args.frequency}GHz')
os.chdir(f'superconductingcoresuperl1superl2cryol3-{args.frequency}GHz')
df = pd.DataFrame.from_dict(process_data(list_folders(os.getcwd())), orient='index')
df.to_csv(f'{args.frequency}GHz.csv')

# # move to data folder
os.system(f'mv {args.frequency}GHz.csv ../data/')