from mkutils import save_to_file, create_fig
import numpy as np
import os

dens_mass = np.loadtxt('density_mass.xvg', comments=['#', '@'])
dens_number = np.loadtxt('density_number.xvg', comments=['#', '@'])

# +
fig, ax = create_fig(1, 1)
ax = ax[0]
args = {'lw': 2}
ax.plot(dens_mass[:, 0], dens_mass[:, 1], **args)
ax.plot(dens_mass[:, 0], dens_mass[:, 2], **args)

    
ax.set_xlabel('z / nm')
ax.set_ylabel('$\\rho_\mathrm{mass}\,/\,kg\,m^{-3} $')
#ax.set_ylim(0,25)
ax2 = ax.inset_axes([0.1, 0.2, 0.25, 0.25])
ax2.plot(dens_mass[:, 0], dens_mass[:, 1], **args)
ax2.set_ylim(0, 20)
ax2.set_xlim(-7, -2.5)

# +
fig, ax = create_fig(1, 1)
ax = ax[0]
args = {'lw': 2}
ax.plot(dens_number[:, 0], dens_number[:, 1], **args)
ax.plot(dens_number[:, 0], dens_number[:, 2], **args)

# xw, xc
xw = dens_number[:,1]/(dens_number[:,1]+dens_number[:, 2])
water_in_oil = np.concatenate((xw[:14], xw[36:]))
mean, std = np.mean(water_in_oil), np.std(water_in_oil)

print('xw outer comp.')
print(mean, std)

    
ax.set_xlabel('z / nm')
ax.set_ylabel('$\\rho_\mathrm{mass}\,/\,\,m^{-3} $')
#ax.set_ylim(0,25)
ax2 = ax.inset_axes([0.1, 0.6, 0.25, 0.25])
ax2.plot(dens_number[:, 0], dens_number[:, 1], **args)
ax2.set_ylim(0, 1)
ax2.set_xlim(-7, -2.5)
# -
water_in_oil = np.concatenate((dens_mass[:14, 1], dens_mass[36:, 1]))
mean, std = np.mean(water_in_oil), np.std(water_in_oil)
print('Solubility of Water in Oil: {:.3f}({:.3f}) kg/m^3'.format(mean, std))
print('Solubility of Water in Oil: {:.3e}({:.3e}) g/cm^3'.format(mean/1000, std/1000))
print('Experimental ~ 10^-5')



