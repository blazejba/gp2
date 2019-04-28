#!/usr/bin/env python3

import os
import sys
import FreeCAD as App
import ObjectsFem
import Part
import Mesh
import subprocess
import tempfile
import Fem
from femtools import ccxtools
from math import sqrt, pow


def importMesh(dir, name):
    while True:
        exists = os.path.isfile(dir + name)
        if exists:
            break
    return Mesh.Mesh(dir + name)


def shapeFromMesh(mesh, doc):
    shape = doc.addObject('Part::Feature', 'shape')
    __shape__ = Part.Shape()
    __shape__.makeShapeFromMesh(mesh.Topology, 1)
    shape.Shape = __shape__
    shape.purgeTouched()
    shape.Shape = shape.Shape.removeSplitter()
    del __shape__
    return shape


def solidFromShape(shape, doc):
    solid = Part.Solid(shape.Shape)
    model = doc.addObject('Part::Feature', 'solid')
    model.Shape = solid
    del solid
    return model


def setAnalysis_setSolver(doc):
    analysis_object = ObjectsFem.makeAnalysis(doc, "Analysis")
    solver_object = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculiX")
    solver_object.WorkingDir = '/home/blaise/code/gpec/eval/model_generator/'
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


def makeConstraintForce(doc, model, direction, magnitude, axis):
    force_references = ['Vertex' + str(ref + 1) for ref in findForceReferences(model, axis)]
    force_constraint = ObjectsFem.makeConstraintForce(doc, "FemConstraintForce")
    force_constraint.References = (model, force_references)
    force_constraint.Force = magnitude
    force_constraint.Direction = (model, ['Face' + str(direction + 1)])
    force_constraint.Reversed = True
    return force_constraint


def generateFmesh(doc, model, gmsh_bin):
    # Export a part in step format
    temp_file = tempfile.mkstemp(suffix='.step')[1]
    model.Shape.exportStep(temp_file)
    selection_name = model.Name

    # Mesh temp file
    file_format = 'unv'
    temp_mesh_file = tempfile.tempdir + '/' + selection_name + '_Mesh.' + file_format

    # run gmsh
    options = ' -algo ' + 'netgen' + ' -optimize ' + ' -order ' + '2'
    dim = ' -3 '
    command = gmsh_bin + ' ' + temp_file + dim + '-format ' + file_format + ' -o ' + temp_mesh_file + '' + options

    try:
        output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT, )
        Fem.insert(temp_mesh_file, App.ActiveDocument.Name)
        FMesh = App.activeDocument().ActiveObject
        App.activeDocument().Analysis.addObject(FMesh)
    except:
        App.Console.PrintError("Unexpected error in GMSHMesh macro: {}".format(sys.exc_info()[0]))
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
        if Xs[0] == Xs[1] == Xs[2]:
            facesX.append(index)
        elif Ys[0] == Ys[1] == Ys[2]:
            facesY.append(index)
        else:
            facesZ.append(index)
    return facesX, facesY, facesZ


def modelDimension(model, faces, axis):
    min =  max = None
    for index in faces:
        face = model.Shape.Faces[index]
        if axis == 'x':
            pos = face.Vertexes[0].X
        elif axis == 'y':
            pos = face.Vertexes[0].Y
        else:
            pos = face.Vertexes[0].Z

        if not min and not max:
            min = max = pos
        else:
            if pos > max:
                max = pos
            elif pos < min:
                min = pos
    return max - min


def boundingBox(model, faces):
    dim_X = modelDimension(model, faces[0], 'x')
    dim_Y = modelDimension(model, faces[1], 'y')
    dim_Z = modelDimension(model, faces[2], 'z')
    return [dim_X, dim_Y, dim_Z]


def findFixReferences(model, faces, axis):
    extrema = None
    best_indexes = []

    for face_index in faces[axis]:
        if axis == 0:
            value = model.Shape.Faces[face_index].Vertexes[0].X
        elif axis == 1:
            value = model.Shape.Faces[face_index].Vertexes[0].Y
        else:
            value = model.Shape.Faces[face_index].Vertexes[0].Z

        if not extrema:
            extrema = value
            best_indexes.append(face_index)
        else:
            if extrema < value:
                extrema = value
                best_indexes = [face_index]
            if extrema == value:
                best_indexes.append(face_index)

    return best_indexes


def findForceReferences(model, axis):
    # find min X vertexes
    min_indexes = []
    extrema = None

    vertexes = model.Shape.Vertexes
    for index, vertex in enumerate(vertexes):
        if axis == 0:
            value = vertex.X
        elif axis == 1:
            value = vertex.Y
        else:
            value = vertex.Z

        if not extrema:
            extrema = value
            min_indexes = [index]
        elif value < extrema:
            extrema = value
            min_indexes = [index]
        elif value == extrema:
            min_indexes.append(index)

    # leave out those with largest Z
    extrema = None
    references = []
    print(min_indexes)
    for index in min_indexes:
        vertex = vertexes[index]
        if axis == 0 or axis == 1:
            value = vertex.Z
        else:
            value = vertex.X

        if not extrema:
            extrema = value
            references = [index]
        elif value > extrema:
            extrema = value
            references = [index]
        elif value == extrema:
            references.append(index)
    print(references)
    return references


def findTopFace(model, faces, axis):
    max = None
    max_idx = None

    if axis == 0 or axis == 1:
        top = 2
    else:
        top = 0

    for idx in faces[top]:
        if top == 2:
            value = model.Shape.Faces[idx].Vertexes[0].Z
        else:
            value = model.Shape.Faces[idx].Vertexes[0].X

        if not max or max < value:
            max = value
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


def distil_references(model, fixed_references, force_references):
    fixed_vertex = meanFixedVertex(model, fixed_references)
    force_vertex = meanForceVertex(model, force_references)
    return fixed_vertex, force_vertex


def fitness_1(doc, fixed_vertex, force_vertex):
    beam_length = calculateDistance(fixed_vertex, force_vertex)
    max_displacement = max(doc.getObject("CalculiX_static_results").DisplacementLengths)
    return 1 / (1 + max_displacement / pow(beam_length, 2))


def fitness_2(doc, force, length, E):
    delta_max_0 = simpleBeamMaxDisplacement(force, length, E)
    delta_max_1 = max(doc.getObject("CalculiX_static_results").DisplacementLengths)
    print('displacement 0 and 1:', delta_max_0, delta_max_1)
    return delta_max_0 / (delta_max_1 +  delta_max_0)


def simpleBeamMaxDisplacement(force, length, E):
    print('what is the length unit', length)
    return (4 * force * pow(length, 3))/E


def main():
    # setup
    gmsh_bin = '/usr/bin/gmsh'
    dir_stl = '/home/blaise/code/gpec/eval/model_generator/tmp/stls/'
    dir_fitness = '/home/blaise/code/gpec/eval/model_generator/tmp/results/'
    #name = sys.argv[3]
    name = '0.0250775548917046_15559992097142885.stl'
    doc = App.newDocument('freecad_doc')
    force_magnitude = 98.0665 / 2 # 10 kg worth of force
    youngs_modulus = 2300.00 # MPa

    try:
        # model
        mesh = importMesh(dir_stl, name)
        shape = shapeFromMesh(mesh, doc)
        model = solidFromShape(shape, doc)

        # analysis and solver
        analysis, solver = setAnalysis_setSolver(doc)
        analysis.addObject(addMaterialABS(doc))

        # contraints
        segregated_faces = segregateFaces(model)
        bounding_box = boundingBox(model, segregated_faces)
        prime_axis = bounding_box.index(max(bounding_box))

        # fixed
        fixed_references = findFixReferences(model, segregated_faces, prime_axis)
        fixed_constraint = makeConstraintFixed(doc, model, fixed_references)
        analysis.addObject(fixed_constraint)

        # force
        force_direction = findTopFace(model, segregated_faces, prime_axis)
        force_references = findForceReferences(model, prime_axis)
        force_constraint = makeConstraintForce(doc, model, force_direction, force_magnitude, prime_axis)
        analysis.addObject(force_constraint)

        # fmesh
        fmesh = generateFmesh(doc, model, gmsh_bin)

        # fem
        doc.recompute()
        fea = ccxtools.FemToolsCcx(analysis, solver)
        fea.purge_results()
        fea.run()

        # points for calculting beam length
        fixed_veretex, force_vertex = distil_references(model, fixed_references, force_references)

        # fitness = 1/(1+arc)
        fitness = fitness_1(doc, fixed_veretex, force_vertex)

        # logaritmic equivalence fitness
        fitness2 = fitness_2(doc, force_magnitude, max(bounding_box), youngs_modulus)

    except:
        fitness = 0

    finally:
        print('fitness 1', fitness)
        print('fitness 2', fitness2)
        file = open(dir_fitness + name[:-4], 'w')
        file.write(str(fitness))
        file.close()

main()
sys.exit(1)
