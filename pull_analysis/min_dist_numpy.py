import numpy as np
import sys
import re
filestr_in  = sys.argv[1]
filestr_out = sys.argv[2]

mat = np.loadtxt(filestr_in, comments=['#', '@'])

x = np.where(mat == np.amin(mat[1:]))
sed_str = '{:d}'.format(int(x[0][0]))
with open(filestr_out, "r") as sources:
    lines = sources.readlines()
with open(filestr_out, "w") as sources:
    for line in lines:
        sources.write(re.sub(r'XPBCATOMX', sed_str, line))
