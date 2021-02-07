#!/usr/bin/env python
# coding: utf-8
# %%

# %%
from clustercode import ClusterEnsemble
from mkutils import statistics, create_fig, save_to_file
import os
import numpy as np
import pickle
import sys
import functools
from scipy.signal import savgol_filter as sav

# %%
#traj = sys.argv[1]
#t0 = float(sys.argv[2])
#tE = float(sys.argv[3])
traj = 'traj.trr'
t0 = 10000.
tE = 30000.
traj = os.path.join('..', traj)
tpr = os.path.join('..', 'topol.tpr')
agg_spec = ['C{:d}'.format(i) for i in range(1,5)]
sasa = np.loadtxt('area.xvg', comments=['#', '@'])
times = (t0, tE)

n_na = 60.
n_sds = 60.
plot = True


rdf_su = np.loadtxt('rdf_headgroup.xvg', comments=['@', '#'])


# %%
system = ClusterEnsemble(tpr, traj, agg_spec)
system.cluster_analysis(times=times)


# %%
condensed_ions = []
gyration = []
inertia = []
rgyr = []
f_factors = []
volume = []
rs = []
angles = []
bl_1 = []
bl_2 = []
bl_3 = []
a_1 = []
a_2 = []
a_3 = []
ecc = []
bonds = [[],[],[],[]]
for i, clusters in enumerate(system.cluster_list):
    for cluster in clusters:
        if len(cluster) > 20:
            if i % 100 == 0: print('Frame {:d}'.format(i))
            system.unwrap_cluster(cluster)
            ci = system.condensed_ions(cluster, 'SU', 'NA', [4.25, 7.6])
            gy = system.gyration(cluster) # Eigenvalues of gyration tensor
            ine = system.inertia_tensor(cluster)
            ecc.append(1.0 - min(ine)/np.mean(ine))
            rg = system.rgyr(cluster) # Radii of gyration cumulative and per princ. axis.
            f32, f21 = system.calc_f_factors(cluster)
            condensed_ions.append(ci)
            gyration.append(gy)
            inertia.append(ine)
            rgyr.append(rg)
            f_factors.append([f32, f21])
            volume.append(functools.reduce(lambda a,b: a*b, system.universe.dimensions[:3]))
            sulfates = cluster.atoms.select_atoms('name SU')
            rs.append(system.rgyr(sulfates, pca=False, mass=False)[0])

            temp_angles = system.angle_distribution(cluster, 'C4', 'C1', 'COM')
            temp_a1 = system.angle_distribution(cluster, 'SU', 'C1', 'C2')
            temp_a2 = system.angle_distribution(cluster, 'C1', 'C2', 'C3')
            temp_a3 = system.angle_distribution(cluster, 'C2', 'C3', 'C4')
            temp_bl1 = system.distance_distribution(cluster, 'SU', 'C2')
            temp_bl2 = system.distance_distribution(cluster, 'C1', 'C3')
            temp_bl3 = system.distance_distribution(cluster, 'C2', 'C4')
            tb1 = system.distance_distribution(cluster, 'SU', 'C1')
            tb2 = system.distance_distribution(cluster, 'C1', 'C2')
            tb3 = system.distance_distribution(cluster, 'C2', 'C3')
            tb4 = system.distance_distribution(cluster, 'C3', 'C4')
            
            angles.extend(temp_angles)
            bl_1.extend(temp_bl1)
            bl_2.extend(temp_bl2)
            bl_3.extend(temp_bl3)
            a_1.extend(temp_a1)
            a_2.extend(temp_a2)
            a_3.extend(temp_a3)
            for i, tb in enumerate([tb1, tb2, tb3, tb4]):
                bonds[i].extend(tb)

# %%
with open('Bond_Angles.pkl', 'wb') as f:
    pickle.dump((angles, bonds, bl_1, bl_2, bl_3, a_1, a_2, a_3), f) 

if plot:
    fig, ax = create_fig(1,1)
    ax = ax[0]
    
    ax.hist(angles, bins=90, histtype='step', lw=2, density=True, color='k', label='Angle COM - C1 - C4')
    ax.set_xlabel('Angle / °')
    ax.set_ylabel('Probability Density / -')
    ax.set_xticks([25*i for i in range(7)])
    ax.legend()
    save_to_file('Angle_Distrib')

# %%
print(len(bl_1), len(bl_2), len(bl_3))

if plot:
    fig, ax = create_fig(1,1)
    ax = ax[0]
    
    ax.hist(bl_1, bins=100, histtype='step', lw=2, density=True, color='C0', label='Distance SU - C2')
    ax.hist(bl_2, bins=100, histtype='step', lw=2, density=True, color='C1', label='Distance C1 - C3')
    ax.hist(bl_3, bins=100, histtype='step', lw=2, density=True, color='C3', label='Distance C2 - C4')

    ax.set_xlabel('Distance / Å')
    ax.set_ylabel('Probability Density / -')
    ax.legend(loc='upper left')
    save_to_file('Distances_1_3_neighbours')

# %%
print(len(a_1), len(a_2), len(a_3))

if plot:
    fig, ax = create_fig(1,1)
    ax = ax[0]
    
    ax.hist(a_1, bins=50, histtype='step', lw=2, density=True, color='C0', label='SU - C1 - C2')
    ax.hist(a_2, bins=50, histtype='step', lw=2, density=True, color='C1', label='C1 - C2 - C3')
    ax.hist(a_3, bins=50, histtype='step', lw=2, density=True, color='C3', label='C2 - C3 - C4')

    ax.set_xlabel('Angle / °')
    ax.set_ylabel('Probability Density / -')
    ax.legend(loc='upper left')
    save_to_file('Common_angles')

# %%
tb1, tb2, tb3, tb4 = bonds
print(len(tb2))

if plot:
    fig, ax = create_fig(1,1)
    ax = ax[0]
    
    ax.hist(tb1, bins=100, histtype='step', lw=2, density=True, color='C0', label='SU - C1')
    ax.hist(tb2, bins=100, histtype='step', lw=2, density=True, color='C1', label='C1 - C2')
    ax.hist(tb3, bins=100, histtype='step', lw=2, density=True, color='C3', label='C2 - C3')
    ax.hist(tb4, bins=100, histtype='step', lw=2, density=True, color='C5', label='C3 - C4')

    ax.set_xlabel('Distance / Å')
    ax.set_ylabel('Probability Density / -')
    ax.legend(loc='upper left')
    save_to_file('Common_bonds')

# %%
# Lets plot the COM stuff
rdf_weight = np.loadtxt('rdf.xvg', comments=['@', '#'])
rdf_number = np.loadtxt('rdf.xvg', comments=['@', '#'])
volume = np.mean(volume)

# 0 11 12 14 7  6      13
# x CM CT SU NA SDS/NA C
# 
def get_factor(selection, volume, measure='weight'):
    su = system.universe.select_atoms(selection)
    if measure=='weight':
        weight = su.total_mass()
        factor = 10**4/6.022 # also taking care of g/mol to kg/mol
    elif measure == 'number':
        weight = su.n_atoms
        factor = 1000.
    raw_dens = weight/volume # #/A^3
    

    return raw_dens * factor 

if plot:
    fig, ax = create_fig(1, 1)
    ax = ax[0]
    # x, CM, CT, SO4, Water, NA, CM_CT
    selections = [{'selection': 'name SU', 'index': 3, 'color': '#E9C46A', "label":'Headgroup'},
                 {'selection': 'name C1 C2 C3 C4', 'index': 6, 'color': '#0099CC', "label":'Tailgroups'},

                 {'selection': 'name C4', 'index': 2, 'color': '#0099CC', 'alpha':0.5, 'label':'Terminal C'},
                 {'selection': 'name NA', 'index': 5, 'color': '#ED553B', "label":'Sodium'},
                 {'selection': 'resname SOL', 'index': 4, 'color': '#003366', "label":'Water'}]
    
    for item in selections:
        factor = get_factor(item.get('selection'), volume)
        rdf_weight[:, item.get('index')] *= factor
        ydata = sav(rdf_weight[:, item.get('index')], 3, 1)
        ax.plot(rdf_weight[:, 0], ydata, lw=2, color=item.get('color', 'C0'), alpha=item.get('alpha', 1),
               label=item.get('label'))
    ax.set_xlabel('$r\,/\,nm$')
    ax.set_ylabel('$\\rho_i\,/\,kg\,m^{-3}$')
    ax.legend()
    ax.set_ylim(0, ax.get_ylim()[1])
    ax.set_xlim(0, 3)
    
    save_to_file('COM_rdf_weight')

    fig, ax = create_fig(1, 1)
    ax = ax[0]
    for item in selections:
        factor = get_factor(item.get('selection'), volume, measure='number')
        rdf_number[:, item.get('index')] *= factor
        ydata = sav(rdf_number[:, item.get('index')], 3, 1)
        ax.plot(rdf_number[:, 0], ydata, lw=2, color=item.get('color', 'C0'), alpha=item.get('alpha', 1),
               label=item.get('label'))
    ax.set_xlabel('$r\,/\,nm$')
    ax.set_ylabel('$\\rho_i\,/\,nm^{-3}$')
    ax.legend()
    ax.set_ylim(0, 15)
    ax.set_xlim(0, 3)
    
save_to_file('COM_rdf_nr')


# %%
#Condensation of sodium around micelle

def bin_fct(data):
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d)/2
    right_of_last_bin = data.max() + float(d)/2

    return np.arange(left_of_first_bin, right_of_last_bin + d, d)


condensed_ions = np.asarray(condensed_ions)
Cond1 = statistics.MultiModalEvaluation(condensed_ions[:,0])
m, s = np.mean(condensed_ions[:,0]), np.std(condensed_ions[:,0])
Cond1.fit(m, s, model='standard', bins=50)

Cond2 = statistics.MultiModalEvaluation(condensed_ions[:,1]-condensed_ions[:,0])
m, s = np.mean(condensed_ions[:,1]-condensed_ions[:,0]), np.std(condensed_ions[:,1]-condensed_ions[:,0])
Cond2.fit(m, s, model='standard', bins=50)

Cond3 = statistics.MultiModalEvaluation(condensed_ions[:,1])
m, s = np.mean(condensed_ions[:,1]), np.std(condensed_ions[:,1])
Cond3.fit(m,s, model='standard', bins=50)

cond_1 = 100*Cond1.params/float(n_na)
cond_2 = 100*Cond2.params/float(n_na)
cond_3 = 100*Cond3.params/float(n_na)

print('Percentage of ions in first, second and combined shells\nTest between bin sizes')
print(cond_1, cond_2, cond_3)


# %%
# Plot Histograms for first, second shell etc.
if plot:
    fig,ax = create_fig(1,1)
    ax = ax[0]

    bins = bin_fct(condensed_ions[:, 0])
    ax.hist(condensed_ions[:, 0], bins=bin_fct(condensed_ions[:, 0]), density=True, width=0.4)
    ax.hist(condensed_ions[:, 1]-condensed_ions[:, 0], bins=bin_fct(condensed_ions[:, 1]-condensed_ions[:, 0]), density=True, width=0.4)
    ax.hist(condensed_ions[:, 1], bins=bin_fct(condensed_ions[:, 1]), density=True, alpha=0.5, color='C3', width=0.4)
    
    x = np.linspace(0, 30, 100)
    ax.plot(x, Cond1.obj_fct(x, *Cond1.params), color='C0', lw=2, label='First Shell')
    ax.plot(x, Cond2.obj_fct(x, *Cond2.params), color='C1', lw=2, label='Second Shell')
    ax.plot(x, Cond3.obj_fct(x, *Cond3.params), color='C3', lw=2, label='First and Second Shell')

    ax.legend()
    ax.set_xlabel('Number of ions')
    ax.set_ylabel('Probability')
    save_to_file('Condensation')


# %%
# Fit gaussians to all the measures.
gyration = np.asarray(gyration)
inertia = np.asarray(inertia)
ecc = np.asarray(ecc)
rgyr = np.asarray(rgyr)
f_factors = np.asarray(f_factors)
Gyr, In, RG, RootGyr = [], [], [], []
F = []
RG.append(statistics.MultiModalEvaluation(rgyr[:, 0]))
RS = statistics.MultiModalEvaluation(rs[:])
Ecc = statistics.MultiModalEvaluation(ecc[:])  
for i in range(3):
    RootGyr.append(statistics.MultiModalEvaluation(np.sqrt(gyration[:, i])))
    Gyr.append(statistics.MultiModalEvaluation(gyration[:, i]))
    In.append(statistics.MultiModalEvaluation(inertia[:, i]))
    RG.append(statistics.MultiModalEvaluation(rgyr[:, i+1]))

for i in range(2):
    F.append(statistics.MultiModalEvaluation(f_factors[:, i]))

RS.fit(1.8, 0.1, model='standard', bins=50)
Ecc.fit(np.mean(ecc), np.std(ecc), model='standard', bins=50)
print(Ecc.params)
for item in Gyr:
    item.fit(1., 1., model='standard', bins=50)
    if 1. in item.params: 
        print('Probably the fit didn\'t work')
for item in RootGyr:
    item.fit(1., 1., model='standard', bins=50)
    if 1. in item.params: 
        print('Probably the fit didn\'t work')
for item in In:
    item.fit(1., 1., model='standard', bins=50)
    if 1.0 in item.params: 
        print('Probably the fit didn\'t work')
for item in RG:
    item.fit(1., 1., model='standard', bins=50)
    if 1. in item.params: 
        print('Probably the fit didn\'t work')
for item in F:
    item.fit(0.5, 0.1, bins=50)
    if 0.5 in item.params or 0.1 in item.params:
        print('Probably the fit didn\'t work')
        



# %%
# Plot all the measured quantities
if plot:
    fig ,ax = create_fig(1,1)
    ax = ax[0]
    for Gi, i, color in zip(Gyr, range(3), ['C0', 'C1', 'C3']):
        ax.hist(gyration[:, i], bins=50, density=True, color=color, alpha=0.7)
        m, s = Gi.params
        x = np.linspace(m - 5*s, m + 5*s, 100)
        ax.plot(x, Gi.obj_fct(x, m, s), color=color, lw=3, label=r"$Rg_{}^2$".format('{0:d}{0:d}'.format(i+1)))
        ax.legend()
        ax.set_xlabel('$Rg_{ii}\,/\,nm^2$')
        ax.set_ylabel('Probability')
    save_to_file('GyrationRadius')
    
    fig ,ax = create_fig(1,1)
    ax = ax[0]
    for Gi, i, color in zip(In, range(3), ['C0', 'C1', 'C3']):
        ax.hist(inertia[:, i], bins=50, density=True, color=color, alpha=0.7)
        m, s = Gi.params
        x = np.linspace(m - 5*s, m + 5*s, 100)
        ax.plot(x, Gi.obj_fct(x, m, s), color=color, lw=3, label="$I_{}^2$".format('{0:d}{0:d}'.format(i+1)))
        ax.legend()
        ax.set_xlabel('$Inertial Momemnt\,/\,nm^2$')
        ax.set_ylabel('Probability')
    save_to_file('Inertia')

    fig ,ax = create_fig(1,1)
    ax = ax[0]       
    
    
    for Gi, i, color in zip(RG, range(4), ['C4', 'C0', 'C1', 'C3']):
        ax.hist(rgyr[:, i], bins=50, density=True, color=color, alpha=0.7)
        m, s = Gi.params
        x = np.linspace(m - 5*s, m + 5*s, 100)
        if i == 0:
            label = 'Rg'
        else:
            label = label="$Rg_{}$".format('{0:d}{0:d}'.format(i))
        ax.plot(x, Gi.obj_fct(x, m, s), color=color, lw=3, label=label)
        ax.legend()
        ax.set_xlabel('$Radius of Gyration\,/\,nm$')
        ax.set_ylabel('Probability')
    save_to_file('Rgyr')
    
    fig ,ax = create_fig(1,1)
    ax = ax[0]     
    for Gi, i, label, color in zip(F, range(2), ['$f_32$', '$f_21$'], ['C0', 'C1']):
        ax.hist(f_factors[:, i], bins=50, density=True, color=color, alpha=0.7)
        m, s = Gi.params
        x = np.linspace(m - 5*s, m + 5*s, 100)
        
        ax.plot(x, Gi.obj_fct(x, m, s), color=color, lw=3, label=label)
        ax.legend()
        ax.set_xlabel('$f_{ii}\,/\,-$')
        ax.set_ylabel('Probability')
    save_to_file('F_factors')    
    
    fig, ax = create_fig(1,1)
    ax = ax[0]
    color, label = 'C0', 'RMS(SO$_4$)'
    ax.hist(rs, bins=50, density=True, color=color, alpha=0.7)
    m, s = RS.params
    x = np.linspace(m - 5*s, m + 5*s, 100)
    ax.plot(x, RS.obj_fct(x, m, s), color=color, lw=3, label="$I_{}^2$".format('{0:d}{0:d}'.format(i+1)))
    ax.legend()
    ax.set_xlabel('$R_s\,/\,nm^2$')
    ax.set_ylabel('Probability')
    save_to_file('Rs_SO4')    
# %%
# Make the f21, f32 plot
import matplotlib.pyplot as plt
if plot:
    fig, ax = create_fig(1, 1)
    ax = ax[0]
    bins=50
    rmin, rmax = 0., 1.
    edge = (rmax - rmin)/float(bins)
    edge = 0. 
    
    hist, xedges, yedges = np.histogram2d(f_factors[:, 0]+edge, f_factors[:, 1]+edge, bins=bins, 
                                          range=[[rmin, rmax], [rmin, rmax]], density=False
                                         )

    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    dz = hist.ravel()
    sc = ax.scatter(xpos, ypos, s=100., c=dz, cmap='binary', marker='s')
    #plt.colorbar(sc)
    ax.axvline(0.33, 0, 0.66, color='k')
    ax.axvline(0.66, 0, 1., color='k')
    ax.axhline(0.33, 0, 0.66, color='k')
    ax.axhline(0.66, 0, 1., color='k')
    ax.text(0.08, 0.2, 'Spherical', fontsize=18)
    ax.text(0.08, 0.5, 'Oblate', fontsize=18)
    ax.text(0.2, 0.8, 'Disk-like', fontsize=18)
    ax.text(0.4, 0.2, 'Prolate', fontsize=18)
    ax.text(0.4, 0.5, 'Ellipsoid', fontsize=18)
    ax.text(0.7, 0.33, 'Rod-Like', fontsize=18)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('$f_{32}$')
    ax.set_ylabel('$f_{21}$')
    
    save_to_file('f_plot')

# %%
# Sasa, tSASA, HSASA calculations.
# overall, tailgrou, head
SASA = statistics.MultiModalEvaluation(sasa[:, 1])
TSASA = statistics.MultiModalEvaluation(sasa[:, 2])
HSASA = statistics.MultiModalEvaluation(sasa[:, 3])
HT_Ratio = statistics.MultiModalEvaluation(sasa[:, 3]/sasa[:,2])

sasa_list = [(SASA, np.mean(sasa[:, 1]), np.std(sasa[:, 1])),
             (TSASA, np.mean(sasa[:, 2]), np.std(sasa[:, 2])),
             (HSASA, np.mean(sasa[:, 3]), np.std(sasa[:, 3])),
             (HT_Ratio, np.mean(sasa[:, 3])/np.mean(sasa[:,2]), np.std(sasa[:, 3])+np.std(sasa[:,2]))
            ]
for item, m, s in sasa_list[:3]:
    item.fit(m, s, bins=50)

HT_Ratio.fit(sasa_list[-1][-2], sasa_list[-1][-1], bins=50)

try:
    assert abs(HT_Ratio.params[0] - HSASA.params[0]/TSASA.params[0]) < 0.01
except:
    print(HT_Ratio.params[0], HSASA.params[0], TSASA.params[0])

if plot:
    fig ,ax = create_fig(1,1)
    ax = ax[0]
    for Gi, i, color, label in zip(sasa_list, range(3), ['C0', 'C1', 'C3'], ['Overall', 'Tail', 'Head']):
        Gi = Gi[0]
        ax.hist(sasa[:, i+1], bins=50, density=True, color=color, alpha=0.7)
        m, s = Gi.params
        x = np.linspace(m - 5*s, m + 5*s, 100)
        ax.plot(x, Gi.obj_fct(x, m, s), color=color, lw=3, label=label)
        ax.legend()
        ax.set_xlabel('$SASA\,/\,nm^2$')
        ax.set_ylabel('Probability')
    save_to_file('Sasa')


# %%

# %%

# %%
# pickle party

Gyr_mean = [item.params[0] for item in Gyr]
Gyr_std = [item.params[1] for item in Gyr]
In_mean = [item.params[0] for item in In]
In_std = [item.params[1] for item in In]
RG_mean = [item.params[0] for item in RG]
RG_std = [item.params[1] for item in RG]
RGyr_mean = [item.params[0] for item in RootGyr]
RGyr_std = [item.params[1] for item in RootGyr]
Sasa_mean = [item[0].params[0] for item in sasa_list]
Sasa_std = [item[0].params[1] for item in sasa_list]
F_mean = [item.params[0] for item in F]
F_std = [item.params[1] for item in F]
ecc_mean, ecc_std = Ecc.params

with open('Results.pkl', 'wb') as f:
    pickle.dump((Gyr_mean, Gyr_std, RGyr_mean, RGyr_std, In_mean, 
                 In_std, RG_mean, RG_std, Sasa_mean, Sasa_std, F_mean, F_std, RS.params[0], RS.params[1]), f)
    pickle.dump((rdf_weight, rdf_number, rdf_su), f)
    pickle.dump((cond_1, cond_2, cond_3), f)


# %%
name = os.getcwd().split(os.sep)[-3]
def write_str(file, names, means, stds):
    for name, mean, std in zip(names, means, stds):
        string = '{:<12s}:    {:<8.3f} +- {:<8.3f}\n'.format(name, mean, std)
        file.write(string)
        
with open('Results.txt', 'w') as f:
    f.write('*****Results from {:s}*****\n\n'.format(name))
    f.write('Gyration Tensor eigenvalues along principal axis in nm^2\n')
    write_str(f, ['Gyr_p{:d}'.format(i) for i in range(1,10)], Gyr_mean, Gyr_std)
    f.write('Root of Gyration Tensor eigenvalues along principal axis in nm\n')
    write_str(f, ['RG_p{:d}'.format(i) for i in range(1,10)], RGyr_mean, RGyr_std)
    f.write('Radii of gyration along principal axis in nm\n')
    write_str(f, ['RG_OA', 'RG_p1', 'RG_p2', 'RG_p3'], RG_mean, RG_std)
    f.write('Radius of gyration of sulfates in nm\n')
    write_str(f, ['RS'], [RS.params[0]], [RS.params[1]])
    f.write('Inertia Tensor eigenvalues along principal axis in amu nm^2\n')
    write_str(f, ['Ine_p{:d}'.format(i) for i in range(1,10)], In_mean, In_std)
    
    f.write('Sasa along principal axis in nm\n')
    write_str(f, ['SASA_{:s}'.format(i) for i in ['OA', 'C', 'SU']], Sasa_mean, Sasa_std)
    

    f.write('F along principal axis in nm\n')
    write_str(f, ['f_{:s}'.format(i) for i in ['32', '21']], F_mean, F_std)

    f.write('Eccentricity in nm\n')
    write_str(f, ['ecc'], [ecc_mean], [ecc_std])
    
    f.write('Condensed ions in percent\n')
    write_str(f, ['first shell', 'second shell', 'both'], [item[0] for item in [cond_1, cond_2, cond_3]],
                                                           [item[1] for item in [cond_1, cond_2, cond_3]])

# %%
name

# %%




