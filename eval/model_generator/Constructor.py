#!/usr/bin/env python3

import sys
from pivy import coin
sys.path.append("/usr/lib/freecad/lib")
import FreeCAD as App
import ObjectsFem
import Part
import ImportGui
import Mesh
import subprocess
import tempfile
import Fem
import FemGui
from femtools import ccxtools
from math import sqrt, pow

gmsh_bin = "/usr/bin/gmsh"
dir = '/home/blaise/code/gpec/eval/model_generator/tmp/stls/'
name = '2019_4_8_18_55_3.stl'
doc = App.ActiveDocument

print('cookies')

def importMesh(dir, name, document):
    Mesh.insert(dir + name, 'free_cad_test')
    mesh = doc.findObjects('Mesh::Feature')[0]
    return mesh


def shapeFromMesh(mesh):
    shape = doc.addObject('Part::Feature', 'shape')
    __shape__ = Part.Shape()
    __shape__.makeShapeFromMesh(mesh.Mesh.Topology, 0.1)
    shape.Shape = __shape__
    shape.purgeTouched()
    del __shape__
    return shape


def solidFromShape(shape):
    solid = Part.Solid(shape.Shape)
    model = doc.addObject('Part::Feature', 'solid')
    model.Shape = solid
    del solid
    return model


def setAnalysis_setSolver(doc):
    analysis_object = ObjectsFem.makeAnalysis(doc, "Analysis")
    solver_object = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX")
    solver_object.GeometricalNonlinearity = 'linear'
    solver_object.ThermoMechSteadyState = True
    solver_object.MatrixSolverType = 'default'
    solver_object.IterationsControlParameterTimeUse = False
    analysis_object.addObject(solver_object)
    return analysis_object, solver_object


def addMaterialABS(doc):
    material = ObjectsFem.makeMaterialSolid(doc, "SolidMaterial")
    mat = material.Material
    mat['Name'] = "ABS-Generic"
    mat['YoungsModulus'] = "2300.00 MPa"
    mat['PoissonRatio'] = "0.370"
    mat['Density'] = "1060.00 kg/m^3"
    material.Material = mat
    return material


def makeConstraintFixed(doc, model, fixed_references):
    stringified_fixed_references = ['Face' + str(ref + 1) for ref in fixed_references]
    fixed_constraint = ObjectsFem.makeConstraintFixed(doc, "FemConstraintFixed")
    fixed_constraint.References = [(model, stringified_fixed_references)]
    return fixed_constraint


def makeConstraintForce(doc, model, direction):
    force_references = ['Vertex' + str(ref + 1) for ref in findForceReferences(model)]
    force_constraint = ObjectsFem.makeConstraintForce(doc, "FemConstraintForce")
    force_constraint.References = (model, force_references)
    force_constraint.Force = 1.0
    force_constraint.Direction = (model, ['Face' + str(direction + 1)])
    force_constraint.Reversed = True
    return force_constraint


def generateFmesh():
    # Export a part in step format
    temp_file = tempfile.mkstemp(suffix='.step')[1]
    ImportGui.export([model], temp_file)
    selection_name = model.Name

    # Mesh temporaly file
    file_format = 'unv'
    temp_mesh_file = tempfile.tempdir + '/' + selection_name + '_Mesh.' + file_format

    # run gmsh
    options = ' -algo ' + 'netgen' + ' -clmax ' + '5.00' + ' -optimize ' + ' -order ' + '2'
    dim = ' -3 '
    command = gmsh_bin + ' ' + temp_file + dim + '-format ' + file_format + ' -o ' + temp_mesh_file + '' + options
    FreeCAD.Console.PrintMessage("Running: {}".format(command))

    try:
        output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT, )
        FreeCAD.Console.PrintMessage(output)
        Fem.insert(temp_mesh_file, FreeCAD.ActiveDocument.Name)

        FMesh = App.activeDocument().ActiveObject
        FemGui.setActiveAnalysis(App.activeDocument().Analysis)
        App.activeDocument().Analysis.addObject(FMesh)
    except:
        FreeCAD.Console.PrintError("Unexpected error in GMSHMesh macro: {}".format(sys.exc_info()[0]))
    finally:
        try:
            del temp_file
        except:
            pass
        try:
            del temp_mesh_file
        except:
            pass

    return FMesh


def segregateFaces(model):
    facesX = []
    facesY = []
    facesZ = []

    for index, face in enumerate(model.Shape.Faces):
        Xs = [vertex.X for vertex in face.Vertexes]
        Ys = [vertex.Y for vertex in face.Vertexes]
        Zs = [vertex.Z for vertex in face.Vertexes]
        if Xs[0] == Xs[1] == Xs[2]:
            facesX.append(index)
        elif Ys[0] == Ys[1] == Ys[2]:
            facesY.append(index)
        else:
            facesZ.append(index)
    return facesX, facesY, facesZ


def findFixReferences(model, faces):
    max_x = None
    best_indexes = []

    for face_index in faces:
        X = model.Shape.Faces[face_index].Vertexes[0].X
        if not max_x:
            max_x = X
            best_indexes.append(face_index)
        else:
            if max_x < X:
                max_x = X
                best_indexes = [face_index]
            if max_x == X:
                best_indexes.append(face_index)

    return best_indexes


def findForceReferences(model):
    min_indexes = []
    min_x = None

    vertexes = model.Shape.Vertexes
    for index, vertex in enumerate(vertexes):
        print(vertex.X)
        if not min_x:
            min_x = vertex.X
            min_indexes = [index]
        elif vertex.X < min_x:
            min_x = vertex.X
            min_indexes = [index]
        elif vertex.X == min_x:
            min_indexes.append(index)

    # leave out those with largest Z
    max_z = None
    references = []

    for index in min_indexes:
        vertex = vertexes[index]
        if not max_z:
            max_z = vertex.Z
            references = [index]
        elif vertex.Z > max_z:
            max_z = vertex.Z
            references = [index]
        elif vertex.Z == max_z:
            references.append(index)

    return references


def findTopFace(model, facesZ):
    max_z = None
    max_idx = None

    for idx in facesZ:
        z = model.Shape.Faces[idx].Vertexes[0].Z
        if not max_z or max_z < z:
            max_z = z
            max_idx = idx

    return max_idx


def meanFixedVertex(model, fixed_references):
    fixed_faces = [face for index, face in enumerate(model.Shape.Faces) if index in fixed_references]
    cum_X = cum_Y = cum_Z = counter = 0
    for face in fixed_faces:
        for vertex in face.Vertexes:
            counter += 1
            cum_X += vertex.X
            cum_Y += vertex.Y
            cum_Z += vertex.Z
    return Part.Vertex(cum_X / counter, cum_Y / counter, cum_Z / counter)


def meanForceVertex(model, force_references):
    forces_vertexes = [vertex for index, vertex in enumerate(model.Shape.Vertexes) if index in force_references]
    cum_X = cum_Y = cum_Z = counter = 0
    for vertex in forces_vertexes:
        counter += 1
        cum_X += vertex.X
        cum_Y += vertex.Y
        cum_Z += vertex.Z
    return Part.Vertex(cum_X / counter, cum_Y / counter, cum_Z / counter)


def calculateDistance(v1, v2):
    return sqrt(pow(v2.X - v1.X, 2) + pow(v2.Y - v1.Y, 2) + pow(v2.Z - v1.Z, 2))


# model
mesh = importMesh(dir, name, doc)
shape = shapeFromMesh(mesh)
model = solidFromShape(shape)

# analysis and solver
analysis, solver = setAnalysis_setSolver(doc)

# model
analysis.addObject(addMaterialABS(doc))

# contraints
facesX, facesY, facesZ = segregateFaces(model)
# fixed
fixed_references = findFixReferences(model, facesX)
fixed_constraint = makeConstraintFixed(doc, model, fixed_references)
analysis.addObject(fixed_constraint)
# force
force_direction = findTopFace(model, facesZ)
force_references = findForceReferences(model)
force_constraint = makeConstraintForce(doc, model, force_direction)
analysis.addObject(force_constraint)

# fmesh
fmesh = generateFmesh()

doc.recompute()
fea = ccxtools.FemToolsCcx()
fea.purge_results()
fea.run()

# fitness = 1/(1+arc)
fixed_vertex = meanFixedVertex(model, fixed_references)
force_vertex = meanForceVertex(model, force_references)
beam_length = calculateDistance(fixed_vertex, force_vertex)
max_displacement = max(App.ActiveDocument.getObject("CalculiX_static_results").DisplacementLengths)
print('length', beam_length, 'max displacement', max_displacement)
print('fitness', 1 / (1 + max_displacement / beam_length))
