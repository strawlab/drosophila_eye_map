`Drosophila eye map`_

.. _drosophila eye map: http://code.astraw.com/projects/drosophila_eye_map

Overview
========

This software package concerns the eye-map of `Drosophila
melanogaster` made by Erich Buchner during his diplom thesis in
1971. This eye map was published in Heisenberg and Wolf (1984). These
data were digitized from a scan of the photo in the book and coverted
to 3D and saved to the included file
receptor_directions_buchner71.csv.

Download
========

To download current and older versions of this package, go to the `download page`_

.. _download page: http://code.astraw.com/projects/drosophila_eye_map/download

History
=======

These programs and files have been extraced from Andrew Straw's
"fsee" `software package`_ for simulating the visual world of
Drosophila described in Dickson, Straw, and Dickinson (in press). At
the 2nd International Conference on Invertebrate Vision in Sweden,
2008, Andrew learned that a digitized form of the Drosophila eye map
would be useful to others, and so he created this package.

This is release 0.1, released August 9, 2008.

.. _software package: http://dickinson.caltech.edu/Research/Grand_Unified_Fly

Contents of the package
=======================

 * README.txt - this file

 * eye_map.gif - a scan of the eye-map as published in Heisenberg and Wolf (1984).

 * receptor_directions_buchner71.csv - Comma separated value (CSV)
   file which indicates the directions of the ommaditial axes in 3D as
   vectors in a unit sphere. Output by
   precompte_buchner71_optics.py. Note that this includes axes for
   both eyes (1398 ommatidia). To get the axes for a single eye, take
   the first or last 699 rows.

 * trace_buchner_1971.py - Python script used to digitize the
   locations of the ommatidial axes on the stereographic projection of
   eye_map.gif.

 * precompute_buchner71_optics.py - Python script used to take the
   output of trace_buchner_1971.py and convert it to a 3D coordinate
   system. Furthermore, a Gaussian spatial weighting map inspired by
   Neumann (2002) is also implemented. These precomputed data are then
   saved for use by other programs as a file called
   precomputed_buchner71.py.

 * util.py - Utility routines used by precompute_buchner71_optics.py.

 * plot_receptors_vtk.py - Python script which is automatically
   inserted into the output of precompute_buchner71_optics.py.

License
=======

This software was written by Andrew Straw <astraw@caltech.edu>, is
copyright by the California Institute of Technology, and is licensed
under the BSD license. The license status of the eye_map.gif file
itself is unclear and should be determined before any attempts at
redistribution.

References
==========

Heisenberg, M. and Wolf, R., (1984) Vision in Drosophila: Genetics
Microbehavior (Studies of Brain Function). Springer Verlag.

Dickson, W.B., Straw, A.D., and Dickinson, M.H. (in press)
"Integrative Model of Drosophila Flight." AIAA Journal.

Neumann, T. (2002) "Modeling Insect Compound Eyes: Space-Variant
Spherical Vision." Biologically Motivated Computer Vision,
Proceedings. Springer Verlag. Vol 2525, pp. 360-367.
