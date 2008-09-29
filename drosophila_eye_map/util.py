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
import cgtypes # cgkit 1.x
import math
import numpy
import scipy, scipy.io
import sets

cube_order = ['posx','negx','posy','negy','posz','negz']

def mag(vec):
    vec = numpy.asarray(vec)
    assert len(vec.shape)==1
    return math.sqrt(numpy.sum(vec**2.0))

def normalize(vec):
    denom = mag(vec)
    return numpy.asarray(vec)/denom

def get_mean_interommatidial_distance( receptor_dirs, triangles ):
    """returns values in radians"""
    # this is not efficient...
    mean_thetas = []
    for iv,v in enumerate(receptor_dirs):
        neighbors = sets.Set()
        for tri in triangles:
            if iv in tri:
                for it in tri:
                    neighbors.add(it)
        neighbors = list(neighbors)
        neighbors.remove( iv )
        neighbor_dirs = [ receptor_dirs[int(n)] for n in neighbors ]
        cos_theta_neighbors = [numpy.dot(n,v) for n in neighbor_dirs]
        theta_neighbors = [numpy.arccos( c ) for c in cos_theta_neighbors]
        mean_theta = numpy.mean(theta_neighbors)
        mean_thetas.append(mean_theta)
    return mean_thetas

def make_receptor_sensitivities(all_d_q,delta_rho_q=None,res=64):
    """

    all_d_q are visual element directions as a 3-vector
    delta_rho_q (angular sensitivity) is in radians

    """
    if delta_rho_q is None:
        raise ValueError('must specify delta_rho_q (in radians)')

    if isinstance( delta_rho_q, float):
        all_delta_rho_qs = delta_rho_q*numpy.ones( (len(all_d_q),), dtype=numpy.float64)
    else:
        all_delta_rho_qs = numpy.asarray(delta_rho_q)
        if len(all_delta_rho_qs.shape) != 1:
            raise ValueError("delta_rho_q must be scalar or vector")
        if all_delta_rho_qs.shape[0] != len(all_d_q):
            raise ValueError("if delta_rho_q is a vector, "
                             "it must have the same number of "
                             "elements as receptors")

    def G_q(zeta,delta_rho_q):
        # gaussian
        # From Snyder (1979) as cited in Burton & Laughlin (2003)
        return numpy.exp( -4*math.log(2)*abs(zeta)**2 / delta_rho_q**2 )

    half_res = res//2
    vals = (numpy.arange(res)-half_res)/half_res

    weight_maps = []

    # setup vectors for initial face (posx)
    face_vecs = {}
    face_vecs['posx'] = []
    x = 1
    for z in vals:
        this_row_vecs = []
        for y in vals:
            on_cube_3d = (x,y,z)
            #print 'on_cube_3d   %5.2f %5.2f %5.2f'%on_cube_3d
            v3norm = normalize(on_cube_3d) # get direction of each pixel
            p_p = cgtypes.quat(0.0, v3norm[0], v3norm[1], v3norm[2])
            this_row_vecs.append(p_p)
        this_row_vecs.reverse()
        face_vecs['posx'].append( this_row_vecs )

    def rot_face( facedict, facename, rotq):
        facedict[facename] = []
        for row in facedict['posx']:
            this_row_vecs = []
            for col in row:
                this_row_vecs.append( rotq*col*rotq.inverse() )
            facedict[facename].append( this_row_vecs )

    rotq = cgtypes.quat()
    rotq = rotq.fromAngleAxis(math.pi/2.0,cgtypes.vec3(0,0,1))
    rot_face( face_vecs, 'posy', rotq)

    rotq = cgtypes.quat()
    rotq = rotq.fromAngleAxis(math.pi,cgtypes.vec3(0,0,1))
    rot_face( face_vecs, 'negx', rotq)

    rotq = cgtypes.quat()
    rotq = rotq.fromAngleAxis(-math.pi/2.0,cgtypes.vec3(0,0,1))
    rot_face( face_vecs, 'negy', rotq)

    rotq = cgtypes.quat()
    rotq = rotq.fromAngleAxis(math.pi/2.0,cgtypes.vec3(0,-1,0))
    rot_face( face_vecs, 'posz', rotq)

    rotq = cgtypes.quat()
    rotq = rotq.fromAngleAxis(math.pi/2.0,cgtypes.vec3(0,1,0))
    rot_face( face_vecs, 'negz', rotq)

    # convert from quat to vec3
    rfv = {}
    for key, rows in face_vecs.iteritems():
        rfv[key] = []
        for row in rows:
            this_row = [ cgtypes.vec3(col.x, col.y, col.z) for col in row ] # convert to vec3
            rfv[key].append( this_row )

    def get_weight_map(fn, rfv, d_q, delta_rho_q):
        angles = numpy.zeros( (vals.shape[0], vals.shape[0]), dtype=numpy.float64 )
        for i, row_vecs in enumerate(rfv[fn]):
            for j, ovec in enumerate(row_vecs):
                angles[i,j] = d_q.angle(ovec)
        wm = G_q(angles,delta_rho_q)
        return wm

    for dqi,(d_q,this_delta_rho_q) in enumerate(zip(all_d_q,all_delta_rho_qs)):
        weight_maps_d_q = {}
        ssf = 0.0

        for fn in cube_order:
            wm = get_weight_map(fn, rfv, d_q, this_delta_rho_q)
            weight_maps_d_q[fn] = wm
            ssf += numpy.sum( wm.flat )

        # normalize
        for mapname,wm in weight_maps_d_q.iteritems():
            weight_maps_d_q[mapname] = wm/ssf

        # save maps by receptor direction
        weight_maps.append( weight_maps_d_q )
    return weight_maps

def flatten_cubemap( cubemap ):
    rank1 = numpy.concatenate( [ numpy.ravel(cubemap[dir]) for dir in cube_order], axis=0 )
    return rank1

def make_repr_able(x):
    if isinstance(x, cgtypes.vec3):
        return repr_vec3(x)
    elif isinstance(x, cgtypes.quat):
        return repr_quat(x)
    elif isinstance(x, list):
        # recurse into
        y = map( make_repr_able,x)
        return y
    else:
        return x

class repr_vec3(cgtypes.vec3):
    def __repr__(self):
        return 'vec3(%s, %s, %s)'%( repr(self.x),
                                    repr(self.y),
                                    repr(self.z) )

class repr_quat(cgtypes.quat):
    def __repr__(self):
        return 'quat(%s, %s, %s, %s)'%( repr(self.w),
                                        repr(self.x),
                                        repr(self.y),
                                        repr(self.z) )

def test_repr():
    x = repr_vec3(1,2,3.0000001)
    ra = repr(x)
    x2 = eval(ra)
    assert x2.z == x.z

    y = [cgtypes.vec3(1,2,3.0000001)]
    y2 = map(make_repr_able,y)
    assert y[0].z == y2[0].z

    x = repr_quat(0.1,1,2,3.0000001)
    ra = repr(x)
    x2 = eval(ra)
    assert x2.z == x.z

    y = [cgtypes.quat(0.1,1,2,3.0000001)]
    y2 = map(make_repr_able,y)
    assert y[0].z == y2[0].z

    y3 = [y]
    y4 = map(make_repr_able,y3)
    assert y3[0][0].z == y4[0][0].z

def save_as_python( fd, var, varname, fname_extra=None ):
    if fname_extra is None:
        fname_extra = ''
    fname_prefix = varname + fname_extra
    buf = get_code_for_var( varname, fname_prefix, var)
    fd.write(buf)

def get_code_for_var( name, fname_prefix, var):
    if (isinstance(var,numpy.ndarray) or
        scipy.sparse.issparse(var)):

        if 0:
            # save as Matrix Market file
            fname = fname_prefix + '.mtx'
            scipy.io.mmwrite( fname, var )

            result = '%s = scipy.io.mmread(os.path.join(datadir,"%s"))\n'%(name,fname)
        else:
            # save as compressed MATLAB .mat file
            fname = fname_prefix + '.mat'
            fd = open( fname, mode='wb' )
            savedict = {name:var}
            #scipy.io.savemat(fname, savedict, format='5' )
            scipy.io.savemat(fd, savedict)
            result = '%s = scipy.io.loadmat(open(os.path.join(datadir,"%s"),mode="rb"))["%s"]\n'%(name,fname,name)
        return result

    if 1:
        ra = repr(var)
        # now check that conversion worked

        # put these in the namespace
        vec3 = cgtypes.vec3
        quat = cgtypes.quat
        try:
            cmp = eval(ra)
        except Exception, err:
            import traceback
            print 'the following exception will trigger a RuntimeError("eval failed") call:'
            traceback.print_exc()
            raise RuntimeError("eval failed")
        else:
            if cmp==var:
                return '%s = '%(name,)+ra+'\n'
            else:
                if 1:
                    # This is a crazy test because equality testing in
                    # cgkit 1.x doesn't seem to work very well.
                    isseq = False
                    try:
                        len(var)
                        isseq = True
                    except:
                        pass

                    if isseq:
                        assert len(var) == len(cmp)
                        for idx in range(len(var)):
                            if var[idx] != cmp[idx]:
                                if repr(var[idx]) == repr(cmp[idx]):
                                    continue
                                raise RuntimeError("equality failure at idx %d. Original = %s, new = %s"%(
                                    idx,repr(var[idx]),repr(cmp[idx])))
                        # hmm, why weren't these equal? i guess there's more precision than repr() checks?
                        return '%s = '%(name,)+ra+'\n'
                else:
                    raise RuntimeError("failed conversion for %s (type %s)"%(repr(var),str(type(var))))

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
