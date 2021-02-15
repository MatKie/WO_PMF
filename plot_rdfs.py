from mkutils import create_fig, save_to_file
import os
import numpy as np

# +
nhpr = 'npt_nh'
vrbe = 'npt'

carbon = 'Dodecane'
files = ['CM_rdf.xvg', 'CT_rdf.xvg', 'CMCT_rdf.xvg']
def plot_stuff(carbon, cases, files):
    nr_cases = len(cases)
    nr_files = len(files)
    fig, ax = create_fig(nr_cases, nr_files, sharex=True, sharey=True, fig_width=10, fig_height=8)
    
    for i, case in enumerate(cases):
        for ii, file in enumerate(files):
            data = np.loadtxt(os.path.join(case, file), comments=['@', '#'])
            for datai in data[:, 1:].T:
                ax[i*nr_files+ii].plot(data[:, 0], datai, lw=2)
                
plot_stuff(carbon, [nhpr, vrbe], files)
# +
fig, ax = create_fig(1,1)
ax = ax[0]

data = np.loadtxt(os.path.join('npt', 'CMCT_rdf.xvg'), comments=['@', '#'])

ax.plot(data[:, 0], data[:, 1], lw=2, label='CM/CT', color='k')
max_x = np.where(data[:,1] == np.max(data[:,1]))[0][0]
print('First maximum: ',data[max_x, 0])
min_x = np.where(data[:,1] == np.min(data[max_x:,1]))[0][0]
print('First minimum: ',data[min_x, 0])

# -



