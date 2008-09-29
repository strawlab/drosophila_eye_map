=======================
 `Drosophila eye map`_
=======================

.. _drosophila eye map: http://code.astraw.com/drosophila_eye_map

Overview
========

This software package concerns the eye-map of `Drosophila
melanogaster` made by Erich Buchner during his diplom thesis in
1971. These data were digitized from a high resolution scan of
Buchner's figure and coverted to 3D and saved to the included file
receptor_directions_buchner71.csv.

.. figure:: http://code.astraw.com/drosophila_eye_map/download/eye_map_small.gif
    :alt: Drosophila eye map
    :width: 400
    :height: 278
    :target: http://code.astraw.com/drosophila_eye_map/download/eye_map.gif

    The `Drosophila melanogaster` eye map of Buchner (1971) [#Buchner]_, as
    published in Heisenberg and Wolf (1984) [#Heisenberg]_ on page 11, Fig. 2.

.. figure:: http://code.astraw.com/drosophila_eye_map/download/interommatidial_distance_small.gif
   :alt: Drosophila eye map with interommatidial distance
   :width: 400
   :height: 300
   :target: http://code.astraw.com/drosophila_eye_map/download/interommatidial_distance.png

   Data of Buchner showing the eye map of `Drosophila melanogaster`
   eye map overlaid on a colormap showing interommatidial distance
   averaged over each ommatidiums nearest neighbors. (This image was
   generated using the make_buchner_interommatidial_distance_figure.py
   script included in the package.)

Download
========

To download current and older versions of this package, go to the `download page`_

.. _download page: http://code.astraw.com/drosophila_eye_map/download

History
=======

These programs and files have been extraced from Andrew Straw's "fsee"
`software package`_ for simulating the visual world of Drosophila
described in Dickson, Straw, and Dickinson (2008) [#Dickson]_. At
the 2nd International Conference on Invertebrate Vision in Sweden,
2008, Andrew learned that a digitized form of the Drosophila eye map
would be useful to others, and so he created this package.

This is release 0.2, released August 20, 2008.

.. _software package: http://dickinson.caltech.edu/Research/Grand_Unified_Fly

Contents of the package
=======================

 * README.txt - this file

 * receptor_directions_buchner71.csv - Comma separated value (CSV)
   file which indicates the directions of the ommaditial axes in 3D as
   vectors in a unit sphere. Output by
   precompte_buchner71_optics.py. Note that this includes axes for
   both eyes (1398 ommatidia). To get the axes for a single eye, take
   the first or last 699 rows. The coordinate system is arranged so
   that +X is frontal (rostral), +Y is left, and +Z is dorsal.

 * trace_buchner_1971.py - Python script used to digitize the
   locations of the ommatidial axes on the stereographic projection of
   eye_map.gif.

 * precompute_buchner71_optics.py - Python script used to take the
   output of trace_buchner_1971.py and convert it to a 3D coordinate
   system. Furthermore, a Gaussian spatial weighting map inspired by
   Neumann (2002) [#Neumann]_ is also implemented. These precomputed
   data are then saved for use by other programs as a file called
   precomputed_buchner71.py.

 * util.py - Utility routines used by precompute_buchner71_optics.py.

 * plot_receptors_vtk.py - Python script which is automatically
   inserted into the output of precompute_buchner71_optics.py.

 * make_buchner_interommatidial_distance_figure.py - Plot Buchner's
   data overlaid on a colormap showing mean interommatidial distance.

License
=======

This software was written by Andrew Straw <astraw@caltech.edu>, is
copyright by the California Institute of Technology, and is licensed
under the BSD license. See the LICENSE.txt file for details.

Related software
================

`ArthroVision by the Invariant Corporation`_ is an insect optics
simulation package.

.. _ArthroVision by the Invariant Corporation: http://www.invariant-corp.com/news.html#eglin

(See also the `History`_ section, above, for a description of Andrew
Straw's fsee software package.)

References
==========

.. [#Buchner] Buchner, E. (1971) `Dunkelanregung des stationaeren Flugs der Fruchtfliege Drosophila.` Dipl Thesis, Univ Tuebingen.

.. [#Heisenberg] Heisenberg, M. and Wolf, R., (1984) `Vision in Drosophila: Genetics Microbehavior (Studies of Brain Function).` Springer Verlag.

.. [#Dickson] Dickson, W.B., Straw, A.D., and Dickinson, M.H. (2008) "Integrative Model of Drosophila Flight." `AIAA Journal`, 46(9).  doi: `10.2514/1.29862`_

.. _10.2514/1.29862: http://dx.doi.org/10.2514/1.29862

.. [#Neumann] Neumann, T. (2002) "Modeling Insect Compound Eyes: Space-Variant Spherical Vision." `Biologically Motivated Computer Vision, Proceedings`. Springer Verlag. Vol 2525, pp. 360-367. doi: `10.1007/3-540-36181-2_36`_

.. _10.1007/3-540-36181-2_36: http://dx.doi.org/10.1007/3-540-36181-2_36
