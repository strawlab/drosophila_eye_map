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

"""Graphical program to inspect weightmap

This GUI program is used to inspect the precomputed_buchner_1971.py
file to make sure its results are what is expected.

WARNING: all dependencies are in this program -- will not load
anything other than precomputed_buchner_1971.py from current
directory or an installed drosophila_eye_map package.  (The reason
is that because this program might be used outside the normal
environment of a drosophila_eye_map package directory, it carries
all its dependencies with it.) This could be a problem if, for
example, the cube_order ever changes.
"""

import numpy as np
import math

import precomputed_buchner71 as precomputed_buchner_1971
from mpl_toolkits.basemap import Basemap # basemap > 0.9.9.1

import matplotlib
rcParams = matplotlib.rcParams
rcParams['font.size'] = 10
rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = 'Times'
#rcParams['font.sans-serif'] = 'Arial'
if 0:
    from matplotlib import verbose
    verbose.level = 'debug-annoying'

import matplotlib.pyplot as plt

cube_order = ['posx', 'negx', 'posy', 'negy', 'posz', 'negz']

def xyz2lonlat(x,y,z):
    R2D = 180.0/math.pi
    try:
        lat = math.asin(z)*R2D
    except ValueError,err:
        if z>1 and z < 1.1:
            lat = math.asin(1.0)*R2D
        else:
            raise
    lon1 = math.atan2(y,x)*R2D
    return lon1,lat

def unflatten_cubemap( rank1 ):
    rank1 = np.asarray(rank1)
    assert rank1.ndim==1
    total_n_pixels = rank1.shape[0]
    n_pixels_per_face = total_n_pixels//6
    n_pixels_per_side = int(np.sqrt(n_pixels_per_face))
    assert 6*n_pixels_per_side**2==total_n_pixels

    cubemap = {}
    for count,dir in enumerate(cube_order):
        start_idx = count*n_pixels_per_face
        this_face_pixels = rank1[ start_idx:start_idx+n_pixels_per_face ]
        this_face_pixels = np.reshape(this_face_pixels,(n_pixels_per_side,n_pixels_per_side))
        cubemap[dir]=this_face_pixels
    return cubemap

def do_projection( proj, lon_lats):
    xys = np.array([proj( lon, lat ) for (lon,lat) in lon_lats ])

    x = xys[:,0]
    y = xys[:,1]

    return x,y

class App:
    def on_pick(self,event):
        self.show_index(event.ind[0]) # only show first point

    def show_index(self,ind):
        vec = self.left_weights[ind,:]

        cubemap = unflatten_cubemap( vec )

        for dir in cube_order:
            self.cubeax[dir].imshow( cubemap[dir],
                                     aspect='auto',
                                     vmin=0.0,
                                     vmax=0.1,
                                     origin='lower',
                                     )

        ax = self.picker_axes

        if self.highlight is None:
            self.highlight, = ax.plot([self.x[ind]],[self.y[ind]],'ro',
                                      ms=4.0,
                                      picker=0, # don't pick this red dot
                                      )
        else:
            self.highlight.set_xdata( [self.x[ind]] )
            self.highlight.set_ydata( [self.y[ind]] )
        plt.draw()

    def __init__(self):
        self.highlight = None
        # modified from make_buchner_interommatidial_distance_figure

        rdirs = precomputed_buchner_1971.receptor_dirs
        rdir_slicer = precomputed_buchner_1971.receptor_dir_slicer
        triangles = precomputed_buchner_1971.triangles
        weights = precomputed_buchner_1971.receptor_weight_matrix_64
        weights = np.asarray(weights.todense())

        self.left_rdirs = rdirs[rdir_slicer['left']]
        self.left_weights = weights[rdir_slicer['left']]

        lon_lats = [xyz2lonlat(*rdir) for rdir in self.left_rdirs]

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

        self.x,self.y = do_projection(stere,lon_lats)

        # pcolor figure -- stereographic projection
        self.fig = plt.figure(figsize=(8,12))
        ax = plt.subplot(2,1,1)
        ax.set_title('click on an ommatidium to show weightmap')
        self.picker_axes = ax

        good = self.x < 1e29 # basemap seems to set bad values to 1e30
        ax.plot(self.x[good],self.y[good],'wo',
                ms=4.0,
                picker=5, # 5 points tolerance
                )

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

        # create axes for cube map
        xinc = 0.2
        yinc = 0.13
        xbase = 0.05
        ybase = 0.05

        self.cubeax = {}
        frameon = True

        # +y
        rect = xbase, (ybase+yinc), xinc, yinc
        self.cubeax['posy'] = self.fig.add_axes(rect,frameon=frameon)

        # +x
        rect = (xbase+xinc), (ybase+yinc), xinc, yinc
        self.cubeax['posx'] = self.fig.add_axes(rect,frameon=frameon)

        # -y
        rect = (xbase+2*xinc), (ybase+yinc), xinc, yinc
        self.cubeax['negy'] = self.fig.add_axes(rect,frameon=frameon)

        # -x
        rect = (xbase+3*xinc), (ybase+yinc), xinc, yinc
        self.cubeax['negx'] = self.fig.add_axes(rect,frameon=frameon)

        # +z
        rect = (xbase+xinc), (ybase+2*yinc), xinc, yinc
        self.cubeax['posz'] = self.fig.add_axes(rect,frameon=frameon)

        # -z
        rect = (xbase+xinc), ybase, xinc, yinc
        self.cubeax['negz'] = self.fig.add_axes(rect,frameon=frameon)


        for dir in cube_order:
            ## if dir not in self.cubeax:
            ##     continue
            self.cubeax[dir].set_xticks([])
            self.cubeax[dir].set_yticks([])
            title = dir
            title = title.replace('pos','+')
            title = title.replace('neg','-')
            self.cubeax[dir].text(0,0,title,color='white')

        self.show_index(0)

    def mainloop(self):
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        plt.show()

def main():
    app = App()
    app.mainloop()

if __name__=='__main__':
    main()
