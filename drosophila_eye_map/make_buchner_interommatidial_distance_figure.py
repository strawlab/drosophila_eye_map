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
import numpy
from scikits import delaunay as dlny

import drosophila_eye_map.precomputed_buchner71 as precomputed_buchner_1971
from drosophila_eye_map.util import get_mean_interommatidial_distance, xyz2lonlat
from mpl_toolkits.basemap import Basemap # basemap > 0.9.9.1

rdirs = precomputed_buchner_1971.receptor_dirs
rdir_slicer = precomputed_buchner_1971.receptor_dir_slicer
triangles = precomputed_buchner_1971.triangles

dists = numpy.array(get_mean_interommatidial_distance( rdirs[rdir_slicer['left']], triangles ))
R2D = 180.0/numpy.pi
dists = dists*R2D

lon_lats = [xyz2lonlat(*rdir) for rdir in rdirs[rdir_slicer['left']]]

basemap_instance = Basemap(projection='stere',
                           resolution=None,
                           lat_ts = 0.0,
                           lat_0 = 0,
                           lon_0 = 90,
                           llcrnrlon = -45,
                           urcrnrlon = -135,
                           llcrnrlat= -30,
                           urcrnrlat = 30,
                           )

xys = numpy.array([basemap_instance( lon, lat ) for (lon,lat) in lon_lats ])

x = xys[:,0]
y = xys[:,1]
tri = dlny.Triangulation(x, y)
interp = tri.nn_interpolator(dists)

yres = 100
xres = 120

X,Y = numpy.mgrid[ min(y):max(y):yres*1j, min(x):max(x):xres*1j]
vals = interp[ min(y):max(y):yres*1j, min(x):max(x):xres*1j]
Z = numpy.ma.masked_array(vals,mask=numpy.isnan(vals))

import pylab
import matplotlib.cm

# pcolor figure
fig2 = pylab.figure(2)
ax = pylab.subplot(1,1,1)
pylab.pcolor(Y,X,Z,shading='flat',cmap=matplotlib.cm.jet_r)

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
circles = numpy.arange(0.,90.,delat).tolist()+\
          numpy.arange(-delat,-90,-delat).tolist()
#biw.basemap_instance.drawparallels(circles,ax=ax)
basemap_instance.drawparallels(circles,ax=ax)

delon = 45.
meridians = numpy.arange(-180,180,delon)
#biw.basemap_instance.drawmeridians(meridians,
#                                   ax=ax)
basemap_instance.drawmeridians(meridians,
                               ax=ax)
cbar = pylab.colorbar()
cbar.ax.set_ylabel('mean inter-ommatidial distance (deg)')

save_fname = 'interommatidial_distance.png'
print 'saving',save_fname
fig2.savefig(save_fname)
print 'OK'

# contour figure
fig1 = pylab.figure(1)
ax = pylab.subplot(1,1,1)
CS = pylab.contour(Y,X,Z,
                   #levels=numpy.linspace(4,16,25),
                   levels=numpy.linspace(4,16,13),
                   colors='k',
                   )
pylab.clabel(CS,fmt='%.1f',colors='k')

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
circles = numpy.arange(0.,90.,delat).tolist()+\
          numpy.arange(-delat,-90,-delat).tolist()
#biw.basemap_instance.drawparallels(circles,ax=ax)
basemap_instance.drawparallels(circles,ax=ax)

delon = 45.
meridians = numpy.arange(-180,180,delon)
## biw.basemap_instance.drawmeridians(meridians,
##                                    ax=ax)
basemap_instance.drawmeridians(meridians,
                               ax=ax)
pylab.show()

