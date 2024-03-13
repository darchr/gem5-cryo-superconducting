import os
import pandas as pd
import numpy as np


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
                l1dAccesses = None
                l1iAccesses = None
                l2Accesses = None
                l3Accesses = None
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
                    if "board.cache_hierarchy.l1dcaches0.overallAccesses::total" in line:
                        print(line)
                        if l1dAccesses is None:
                            l1dAccesses = line.split()[1]
                    if "board.cache_hierarchy.l1icaches0.overallAccesses::total" in line:
                        print(line)
                        if l1iAccesses is None:
                            l1iAccesses = line.split()[1]
                    if "board.cache_hierarchy.l2caches0.overallAccesses::total" in line:
                        print(line)
                        if l2Accesses is None:
                            l2Accesses = line.split()[1]
                    if "board.cache_hierarchy.l3cache.overallAccesses::total" in line:
                        print(line)
                        if l3Accesses is None:
                            l3Accesses = line.split()[1]
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
                    }
                except Exception as e:
                    print("Error in file: ", file)
                    print(e)
                    pass
    return microbench_data

df = pd.DataFrame.from_dict(process_data(list_folders('.')), orient='index')
df.to_csv('4GHz.csv')