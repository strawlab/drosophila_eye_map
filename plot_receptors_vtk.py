# The contents of this file get pasted into others
# Copyright (C) 2005-2007 California Institute of Technology, All rights reserved
# Author: Andrew D. Straw
from util import get_mean_interommatidial_distance

if __name__ == '__main__':
    
    if 0:
        v2 = [ (v.x, v.y, v.z) for v in receptor_dirs ]
        if 0:
            print repr(v2)
        elif 0:
            import pylab
            xs, ys, zs = zip(*v2)
            pylab.plot( xs, zs )
            pylab.show()
        elif 0:
            # This was piped to qhull "qhull i < receptors.qhull"
            print '3'
            print len(receptor_dirs)
            for v in receptor_dirs:
                print ' '.join(map(repr,v))

    if 1:
        import vtk
        from vtk.util.colors import red, purple, banana
        
        def init_vtk():

            renWin = vtk.vtkRenderWindow()

            renderers = []

            if 1:
                camera = vtk.vtkCamera()
                camera.SetParallelProjection(1)

                camera.SetClippingRange (1e-3, 1e6)

                ren1 = vtk.vtkRenderer()
                lk = vtk.vtkLightKit()
                ren1.SetViewport(0.0,0,1.0,1.0)
                ren1.SetBackground( .6,.6,.75)
                ren1.SetActiveCamera( camera )
                renWin.AddRenderer( ren1 )
                renderers.append( ren1 )
                
            renWin.SetSize( 1024, 768 )
            return renWin, renderers
    
        def interact_with_renWin(renWin, ren1=None, actor=None):

            iren = vtk.vtkRenderWindowInteractor()
            iren.SetRenderWindow( renWin )

            iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
            iren.Initialize ()

            renWin.Render()

            iren.Start()
            
        renWin, renderers = init_vtk()

        camera = renderers[0].GetActiveCamera()

        camera.SetParallelProjection(1)
        camera.SetFocalPoint (0.0, 0.0, 0.0)
        camera.SetPosition (-7.0408423455838438, 4.8870908878427501, -1.2421278994521863)
        camera.SetViewAngle(30.0)
        camera.SetViewUp (0.57291464566682204, 0.73136940687668806, -0.36995621290269104)
        camera.SetClippingRange (3.6770148314673339, 14.954014556113785)
        camera.SetParallelScale(3.89701935633)

        renderers[0].SetActiveCamera(camera)

        def vtk_label_iod( receptor_dirs, triangles, renderers ):
            dists = get_mean_interommatidial_distance( receptor_dirs, triangles )
            pi = 3.1415926535897931
            R2D = 180.0/pi
            for v,dist in zip(receptor_dirs,dists):
                atext = vtk.vtkVectorText()
                atext.SetText("%.1f"%(dist*R2D,))
                textMapper = vtk.vtkPolyDataMapper()
                textMapper.SetInput(atext.GetOutput())
                textActor = vtk.vtkFollower()
                textActor.SetMapper(textMapper)
                scale = 0.03
                textActor.SetScale(scale, scale, scale)
                mult = 1.02
                textActor.AddPosition(v.x*mult,v.y*mult,v.z*mult)
                for renderer in renderers:
                    renderer.AddActor( textActor )
            
            
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
                body_lines.InsertNextCell( len(face)+1 )
                for v in face:
                    body_line_points.InsertNextPoint(v.x, v.y, v.z)
                    body_lines.InsertCellPoint( body_point_num )
                    body_point_num += 1
                v = face[0] # connect to beginning
                body_line_points.InsertNextPoint(v.x, v.y, v.z)
                body_lines.InsertCellPoint( body_point_num )
                body_point_num += 1

            if 1:
                profileData = vtk.vtkPolyData()
                profileData.SetPoints(tri_points)
                profileData.SetPolys(tri_cells)

                profileMapper = vtk.vtkPolyDataMapper()
                profileMapper.SetInput(profileData)

                profile = vtk.vtkActor()
                profile.SetMapper(profileMapper)
                profile.GetProperty().SetDiffuseColor(purple)
                profile.GetProperty().SetSpecular(.3)
                profile.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor( profile )
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
                head_glyphs.SetInput(points_poly_data)
                head_glyphs.SetSource(head.GetOutput())

                head_glyph_mapper = vtk.vtkPolyDataMapper()
                head_glyph_mapper.SetInput( head_glyphs.GetOutput())
                headGlyphActor = vtk.vtkActor()
                headGlyphActor.SetMapper(head_glyph_mapper)
                headGlyphActor.GetProperty().SetDiffuseColor(purple)
                headGlyphActor.GetProperty().SetSpecular(.3)
                headGlyphActor.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor( headGlyphActor )

            if 1:
                profileData = vtk.vtkPolyData()

                profileData.SetPoints(body_line_points)
                profileData.SetLines(body_lines)

                # Add thickness to the resulting line.
                profileTubes = vtk.vtkTubeFilter()
                profileTubes.SetNumberOfSides(8)
                profileTubes.SetInput(profileData)
                profileTubes.SetRadius(.005)
                #profileTubes.SetRadius(.8)

                profileMapper = vtk.vtkPolyDataMapper()
                profileMapper.SetInput(profileTubes.GetOutput())

                profile = vtk.vtkActor()
                profile.SetMapper(profileMapper)
                #profile.GetProperty().SetDiffuseColor( 0xd6/255.0, 0xec/255.0, 0x1c/255.0)
                #profile.GetProperty().SetDiffuseColor(cerulean)
                profile.GetProperty().SetDiffuseColor(banana)
                profile.GetProperty().SetSpecular(.3)
                profile.GetProperty().SetSpecularPower(30)

                for renderer in renderers:
                    renderer.AddActor( profile )

        vtk_draw( receptor_dirs, triangles, hex_faces, renderers )
        vtk_label_iod( receptor_dirs, triangles, renderers )
        interact_with_renWin(renWin,renderers)
