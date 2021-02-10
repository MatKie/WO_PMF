import numpy as np
from mkutils import create_fig, save_to_file
import os
from scipy.signal import savgol_filter as svg

x = np.loadtxt(os.path.join('..','npt_pull', 'pullx.xvg'), comments=['#', '@'])
f = np.loadtxt(os.path.join('..','npt_pull', 'pullf.xvg'), comments=['#', '@'])

# +
fig, ax = create_fig(2, 1, sharex=True)
ax2 = ax[1]
ax = ax[0]

ax.plot(x[:,0], x[:,1], color='k', lw=2)
ax2.plot(f[:,0], f[:, 1], lw=2)
ax2.plot(f[:,0], svg(f[:,1], 15,1), color='k', lw=2)

ax2.set_xlabel('Time / ps')
ax.set_ylabel('z / nm')
ax2.set_ylabel('Force / kJ/mol/nm')
if not os.path.isdir('plots'):
    os.makedirs('plots')
save_to_file('plots/pull_force_position')
# -


