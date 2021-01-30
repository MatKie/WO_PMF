import numpy as np
import sys

if len(sys.argv) > 1:
    dist = float(sys.argv[1])
else:
    dist = 7.5

pairdist = np.loadtxt('dist.xvg', comments=['@', '#'])

pairdist_min = [abs(item - dist) for item in pairdist[1:]]

min_res = np.where(pairdist_min == np.amin(pairdist_min))[0][0]

print(len(pairdist_min))
min_dist = pairdist[min_res+1]

print("Min Residue (counting from zero): {:d}".format(min_res))
print("Min Residue distance: {:.4f}".format(min_dist))
