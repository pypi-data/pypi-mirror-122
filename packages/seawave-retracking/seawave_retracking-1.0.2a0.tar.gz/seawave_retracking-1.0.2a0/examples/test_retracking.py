import sys, os
sys.path.append(".")

from seawave_retracking import pulses, config

f = pulses.get_files('examples/impulses/.*.dat')

pulse = []
for i in range(len(f)):
    pulse.append(pulses.karaev(config, file=f[i]))
pulses.to_xlsx(pulse)
# 