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

# This file specifies how to install the drosophila_eye_map package
# for use by other Python programs and libraries.

from setuptools import setup, find_packages
import os

if not os.path.exists(os.path.join('drosophila_eye_map','precomputed_buchner71.py')):
    raise ValueError('precomputed_buchner71.py is missing')

setup(name='drosophila_eye_map',
      description='eye map of Drosophila melanogaster',
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      version='0.3', # keep in sync with upload_stuff.sh and README.txt
      packages = find_packages(),
      package_data = {'drosophila_eye_map':['receptor_weight_matrix_64_buchner71.mat',
                                            #'precomputed_buchner71.py', # automatically installed since it's a Python file
                                            ]},
      )
