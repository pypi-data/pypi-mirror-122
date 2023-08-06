import sys, os
sys.path.append(".")
import unittest

from seawave.retracking import pulses
from seawave import config

f = pulses.get_files('seawave/retracking/.*.dat')


for i in range(len(f)):
    pulses.karaev(config, file=f[i])
# from seawave import config 


# pulses = get_files('./seawave/retracking/aver*.dat')
# print(pulses)

# config['Dataset']['RetrackingFileName'] = 'kek.xlsx'
# df0, df = retracking.from_file('impulses/.*.txt', config)
# print(df)