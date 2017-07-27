# -*- coding: utf-8 -*-
# Copyright (c) 2005-2008, California Institute of Technology
# Copyright (c) 2017, Albert-Ludwigs-Universität Freiburg
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

# This function copied from util.py.
def get_mean_interommatidial_distance(receptor_dirs, triangles):
    """returns values in radians"""
    # this is not efficient...
    mean_thetas = []
    for iv, v in enumerate(receptor_dirs):
        neighbors = set()
        for tri in triangles:
            if iv in tri:
                for it in tri:
                    neighbors.add(it)
        neighbors = list(neighbors)
        neighbors.remove(iv)
        neighbor_dirs = [receptor_dirs[int(n)] for n in neighbors]
        cos_theta_neighbors = [numpy.dot(n, v) for n in neighbor_dirs]
        theta_neighbors = [numpy.arccos(c) for c in cos_theta_neighbors]
        mean_theta = numpy.mean(theta_neighbors)
        mean_thetas.append(mean_theta)
    return mean_thetas

if __name__ == '__main__':

    if 0:
        v2 = [(v.x, v.y, v.z) for v in receptor_dirs]
        if 0:
            print(repr(v2))
        elif 0:
            import pylab
            xs, ys, zs = zip(*v2)
            pylab.plot(xs, zs)
            pylab.show()
        elif 0:
            # This was piped to qhull "qhull i < receptors.qhull"
            print('3')
            print(len(receptor_dirs))
            for v in receptor_dirs:
                print(' '.join(map(repr, v)))

    if 1:
        import vtk
        from vtk.util.colors import red, purple, banana

        def init_vtk():

            renWin = vtk.vtkRenderWindow()

            renderers = []

            if 1:
                camera = vtk.vtkCamera()
                camera.SetParallelProjection(1)

                camera.SetClippingRange(1e-3, 1e6)

                ren1 = vtk.vtkRenderer()
                lk = vtk.vtkLightKit()
                ren1.SetViewport(0.0, 0, 1.0, 1.0)
                ren1.SetBackground(.6, .6, .75)
                ren1.SetActiveCamera(camera)
                renWin.AddRenderer(ren1)
                renderers.append(ren1)

            renWin.SetSize(1024, 768)
            return renWin, renderers

        def interact_with_renWin(renWin, ren1=None, actor=None):

            iren = vtk.vtkRenderWindowInteractor()
            iren.SetRenderWindow(renWin)

            iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
            iren.Initialize()

            renWin.Render()

            iren.Start()

        renWin, renderers = init_vtk()

        camera = renderers[0].GetActiveCamera()

        camera.SetParallelProjection(1)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetPosition(-7.0408423455838438, 4.8870908878427501, -1.2421278994521863)
        camera.SetViewAngle(30.0)
        camera.SetViewUp(0.57291464566682204, 0.73136940687668806, -0.36995621290269104)
        camera.SetClippingRange(3.6770148314673339, 14.954014556113785)
        camera.SetParallelScale(3.89701935633)

        renderers[0].SetActiveCamera(camera)

        def vtk_label_iod(receptor_dirs, triangles, renderers):
            dists = get_mean_interommatidial_distance(receptor_dirs, triangles)
            pi = 3.1415926535897931
            R2D = 180.0/pi
            for v, dist in zip(receptor_dirs, dists):
                atext = vtk.vtkVectorText()
                atext.SetText("%.1f"%(dist*R2D,))
                textMapper = vtk.vtkPolyDataMapper()
                textMapper.SetInputConnection(atext.GetOutputPort())
                textActor = vtk.vtkFollower()
                textActor.SetMapper(textMapper)
                scale = 0.03
                textActor.SetScale(scale, scale, scale)
                mult = 1.02
                textActor.AddPosition(v.x*mult, v.y*mult, v.z*mult)
                for renderer in renderers:
                    renderer.AddActor(textActor)


        def vtk_draw(receptor_dirs, triangles, hex_faces, renderers):
            tri_points = vtk.vtkPoints()
            tri_cells = vtk.vtkCellArray()

            body_line_points = vtk.vtkPoints()
            body_lines = vtk.vtkCellArray()
            body_point_num = 0

            for v in receptor_dirs:
                #if v.z > 0:
                if 1:
                    tri_points.InsertNextPoint(v.x, v.y, v.z)

            for tri in triangles:
                tri_cells.InsertNextCell(3)
                tri_cells.InsertCellPoint(tri[0])
                tri_cells.InsertCellPoint(tri[1])
                tri_cells.InsertCellPoint(tri[2])

            for face in hex_faces:
                body_lines.InsertNextCell(len(face)+1)
                for v in face:
                    body_line_points.InsertNextPoint(v.x, v.y, v.z)
                    body_lines.InsertCellPoint(body_point_num)
                    body_point_num += 1
                v = face[0] # connect to beginning
                body_line_points.InsertNextPoint(v.x, v.y, v.z)
                body_lines.InsertCellPoint(body_point_num)
                body_point_num += 1

            if 1:
                profileData = vtk.vtkPolyData()
                profileData.SetPoints(tri_points)
                profileData.SetPolys(tri_cells)

                profileMapper = vtk.vtkPolyDataMapper()
                profileMapper.SetInputData(profileData)

                profile = vtk.vtkActor()
                profile.SetMapper(profileMapper)
                profile.GetProperty().SetDiffuseColor(purple)
                profile.GetProperty().SetSpecular(.3)
                profile.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor(profile)
            else:
                points_poly_data = vtk.vtkPolyData()
                points_poly_data.SetPoints(tri_points)

                head = vtk.vtkSphereSource()
                head.SetRadius(.05)
                #head.SetThetaResolution(8)
                #head.SetPhiResolution(8)
                head.SetThetaResolution(15)
                head.SetPhiResolution(15)

                head_glyphs = vtk.vtkGlyph3D()
                head_glyphs.SetInputConnection(points_poly_data)
                head_glyphs.SetSource(head.GetOutputPort())

                head_glyph_mapper = vtk.vtkPolyDataMapper()
                head_glyph_mapper.SetInputConnection(head_glyphs.GetOutputPort())
                headGlyphActor = vtk.vtkActor()
                headGlyphActor.SetMapper(head_glyph_mapper)
                headGlyphActor.GetProperty().SetDiffuseColor(purple)
                headGlyphActor.GetProperty().SetSpecular(.3)
                headGlyphActor.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor(headGlyphActor)

            if 1:
                profileData = vtk.vtkPolyData()

                profileData.SetPoints(body_line_points)
                profileData.SetLines(body_lines)

                # Add thickness to the resulting line.
                profileTubes = vtk.vtkTubeFilter()
                profileTubes.SetNumberOfSides(8)
                profileTubes.SetInputData(profileData)
                profileTubes.SetRadius(.005)
                #profileTubes.SetRadius(.8)

                profileMapper = vtk.vtkPolyDataMapper()
                profileMapper.SetInputConnection(profileTubes.GetOutputPort())

                profile = vtk.vtkActor()
                profile.SetMapper(profileMapper)
                #profile.GetProperty().SetDiffuseColor( 0xd6/255.0, 0xec/255.0, 0x1c/255.0)
                #profile.GetProperty().SetDiffuseColor(cerulean)
                profile.GetProperty().SetDiffuseColor(banana)
                profile.GetProperty().SetSpecular(.3)
                profile.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor(profile)

        try:
            vtk_draw(receptor_dirs, triangles, hex_faces, renderers)
        except NameError as err:
            print('this script is meant to be embedded into precomputed_buchner71.py, not run standalone', file=sys.stderr)
        vtk_label_iod(receptor_dirs, triangles, renderers)
        interact_with_renWin(renWin, renderers)
