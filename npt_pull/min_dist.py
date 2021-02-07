import MDAnalysis as mda
import numpy as np

uni = mda.Universe('../npt/topol.tpr', 'traj_cat.xtc')

SDS = uni.select_atoms('resname SDS')

min_res = -1.
min_frame = -1.
min_distance = 1000.
for i, frame in enumerate(uni.trajectory):
    this_dist = 1000. 
    this_res = -1. 
    for j, residue in enumerate(SDS.residues):
        distance = np.subtract(residue.atoms.center_of_mass(), SDS.center_of_mass())
        distance_sq = np.multiply(distance, distance)
        sum_distance = np.sum(distance_sq)
        real_distance = np.sqrt(sum_distance)
        if real_distance < this_dist:
            this_res = j
            this_dist= real_distance
    if this_dist <= min_distance:
        min_res = this_res
        min_distance = this_dist
        min_frame = i 

print("Min Residue (counting from zero): {:d}".format(min_res))
print("Min Time index (counting from zero): {:d}".format(min_frame))
print("Min Residue distance: {:.4f}".format(min_distance))

for frame in uni.trajectory[min_frame:min_frame+1]:
    if min_res < 0.5:
        select_string  = 'resid 1-{:d}'.format(SDS.n_residues-1)
    else:
        select_string = 'resid 0-{:d} or resid {:d}-{:d}'.format(
                        min_res, min_res+2, SDS.n_residues-1)
    micelle = uni.select_atoms(select_string)
    com = micelle.center_of_mass()
    min_distance, min_atom = 1000, -1
    for j, atom in enumerate(SDS.atoms):
        distance = np.subtract(atom.position, com)
        sum_distance = np.sum(np.multiply(distance, distance))
        real_distance = np.sqrt(sum_distance)
        if real_distance <= min_distance:
            min_distance = real_distance
            min_atom     = j

print('min atom (index from zero), min distance')
print(min_atom, min_distance)
