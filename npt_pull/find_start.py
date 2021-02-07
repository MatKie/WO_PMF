import numpy as np
import sys

pairdist = np.loadtxt('dist.xvg', comments=['@', '#'])

min_res = np.where(pairdist == np.amin(pairdist[:, 1:]))

time_index = min_res[0][0]
res_index = min_res[1][0]

print("Min Residue (counting from zero): {:d}".format(res_index-1))
print("Min Time : {:.2f}".format(pairdist[time_index, 0]))
print("Min Time index (counting from zero): {:d}".format(time_index))
print("Min Residue distance: {:.4f}".format(pairdist[time_index, res_index]))
