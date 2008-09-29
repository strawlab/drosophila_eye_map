# Copyright (c) 2005-2008, California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Andrew D. Straw
from __future__ import division
import numpy as np
from scikits import delaunay as dlny

import drosophila_eye_map.precomputed_buchner71 as precomputed_buchner_1971
from drosophila_eye_map.util import get_mean_interommatidial_distance, xyz2lonlat
from mpl_toolkits.basemap import Basemap # basemap > 0.9.9.1

rdirs = precomputed_buchner_1971.receptor_dirs
rdir_slicer = precomputed_buchner_1971.receptor_dir_slicer
triangles = precomputed_buchner_1971.triangles

dists = np.array(get_mean_interommatidial_distance( rdirs[rdir_slicer['left']], triangles ))
R2D = 180.0/np.pi
dists = dists*R2D

lon_lats = [xyz2lonlat(*rdir) for rdir in rdirs[rdir_slicer['left']]]

stere = Basemap(projection='stere',
                resolution=None,
                lat_ts = 0.0,
                lat_0 = 0,
                lon_0 = 90,
                llcrnrlon = -45,
                urcrnrlon = -135,
                llcrnrlat= -30,
                urcrnrlat = 30,
                )

def do_projection( proj, lon_lats, dists, xres = 120, yres = 100 ):
    xys = np.array([proj( lon, lat ) for (lon,lat) in lon_lats ])

    x = xys[:,0]
    y = xys[:,1]

    good = x < 1e29 # basemap seems to set bad values to 1e30
    x=x[good]
    y=y[good]
    dists=dists[good]

    tri = dlny.Triangulation(x, y)
    interp = tri.nn_interpolator(dists)

    X,Y = np.mgrid[ min(y):max(y):yres*1j, min(x):max(x):xres*1j]
    vals = interp[ min(y):max(y):yres*1j, min(x):max(x):xres*1j]
    Z = np.ma.masked_array(vals,mask=np.isnan(vals))
    return x,y,X,Y,Z

x,y,X,Y,Z = do_projection(stere,lon_lats,dists)

import matplotlib.pyplot as plt
import matplotlib.cm

# pcolor figure -- stereographic projection
fig3 = plt.figure(3)
ax = plt.subplot(1,1,1)
plt.pcolor(Y,X,Z,shading='flat',cmap=matplotlib.cm.jet_r)

ax.plot(x,y,'wo',ms=4.0)

ax.text( 0.5,0.99, 'dorsal',
         horizontalalignment='center',
         verticalalignment='top',
         transform=ax.transAxes)
ax.text( 0.01,0.5, 'anterior',
         horizontalalignment='left',
         transform=ax.transAxes)
ax.text( 0.99,0.5, 'posterior',
         horizontalalignment='right',
         transform=ax.transAxes)

# draw parallels and meridians.
delat = 20.
circles = np.arange(0.,90.,delat).tolist()+\
          np.arange(-delat,-90,-delat).tolist()
#biw.stere.drawparallels(circles,ax=ax)
stere.drawparallels(circles,ax=ax)

delon = 45.
meridians = np.arange(-180,180,delon)
stere.drawmeridians(meridians,ax=ax)
cbar = plt.colorbar()
cbar.ax.set_ylabel('mean inter-ommatidial distance (deg)')

save_fname = 'interommatidial_distance.png'
print 'saving',save_fname
fig3.savefig(save_fname)
print 'OK'



# contour figure -- stereographic projection
fig1 = plt.figure(1)
ax = plt.subplot(1,1,1)
CS = plt.contour(Y,X,Z,
                   #levels=np.linspace(4,16,25),
                   levels=np.linspace(4,16,13),
                   colors='k',
                   )
plt.clabel(CS,fmt='%.1f',colors='k')

ax.plot(x,y,'wo',ms=4.0)

ax.text( 0.5,0.99, 'dorsal',
         horizontalalignment='center',
         verticalalignment='top',
         transform=ax.transAxes)
ax.text( 0.01,0.5, 'anterior',
         horizontalalignment='left',
         transform=ax.transAxes)
ax.text( 0.99,0.5, 'posterior',
         horizontalalignment='right',
         transform=ax.transAxes)

# draw parallels and meridians.
delat = 20.
circles = np.arange(0.,90.,delat).tolist()+\
          np.arange(-delat,-90,-delat).tolist()
stere.drawparallels(circles,ax=ax)

delon = 45.
meridians = np.arange(-180,180,delon)
stere.drawmeridians(meridians,
                    ax=ax)


# contour figure -- orthographic projection
fig2 = plt.figure(2)

# Match projection of
# http://jeb.biologists.org/cgi/content/full/209/21/4339/FIG1
ortho = Basemap(projection='ortho',
                lat_0=10,
                lon_0=20,
                resolution=None,
                )

x,y,X,Y,Z = do_projection(ortho,lon_lats,dists,xres=500,yres=500)

ax = plt.subplot(1,1,1)
CS = plt.contour(Y,X,Z,
                 #levels=np.linspace(4,16,25),
                 levels=np.arange(4,16.5,1.0),
                 colors='k',
                 linewidths=2.0,
                 )
plt.clabel(CS,fmt='%.1f',colors='k')

#ax.plot(x,y,'wo',ms=4.0)
ax.set_aspect('equal')

# draw parallels and meridians.
delat = 10.
circles = np.arange(0.,90.,delat).tolist()+\
          np.arange(-delat,-90,-delat).tolist()
circles = [c for c in circles if c!= 0.0]
ortho.drawparallels(circles,ax=ax)
ortho.drawparallels([0.0],linestyle='-',dashes=[],ax=ax)

delon = 10.
meridians = np.arange(-180,180,delon).tolist()
meridians = [m for m in meridians if m!=0.0]
ortho.drawmeridians(meridians,ax=ax)
ortho.drawmeridians([0.0],linestyle='-',dashes=[],ax=ax)
ortho.drawmapboundary(ax=ax)

save_fname = 'interommatidial_distance_ortho.png'
print 'saving',save_fname
fig2.savefig(save_fname)
print 'OK'


plt.show()

