from math import pow, sqrt
import sys


class SurfaceVolumeRatio:
    def calculate_volume_surface_ratio(self, path_stl):
        try:
            triangles = self.get_triangles_from_stl(path_stl)
            volume = self.calculate_volume(triangles)
            surface = self.calculate_surface(triangles)
            ratio_fitness = 1 / (1 + pow(surface, 1/2) / pow(volume, 1/3))
            return ratio_fitness
        except:
            return 0

    # http://chenlab.ece.cornell.edu/Publication/Cha/icip01_Cha.pdf
    def calculate_volume(self, triangles):
        volume = 0
        for triangle in triangles:
            volume += self.signed_triangle_volume(triangle[0], triangle[1], triangle[2])
        return volume

    # https://math.stackexchange.com/questions/128991/how-to-calculate-area-of-3d-triangle#128999
    def calculate_surface(self, triangles):
        surface = 0
        for triangle in triangles:
            A, B, C = triangle
            AB = self.vector_subtraction(A, B)
            AC = self.vector_subtraction(A, C)
            surface += self.triangle_surface(AB, AC)
        return surface

    @staticmethod
    def get_triangles_from_stl(path_stl):
        triangles = []
        triangle = []
        stl = open(path_stl)
        for line in stl:
            if line.find('vertex') == 6:
                point = [float(coordinate) for coordinate in line[13:-1].split(' ')]
                triangle.append(point)
                if len(triangle) == 3:
                    triangles.append(triangle)
                    triangle = []
        stl.close()
        return triangles

    @staticmethod
    def signed_triangle_volume(p1, p2, p3):
        v321 = p3[0] * p2[1] * p1[2]
        v231 = p2[0] * p3[1] * p1[2]
        v312 = p3[0] * p1[1] * p2[2]
        v132 = p1[0] * p3[1] * p2[2]
        v123 = p1[0] * p2[1] * p3[2]
        v213 = p2[0] * p1[1] * p3[2]
        return (-v321 + v231 + v312 - v132 - v213 + v123) / 6

    @staticmethod
    def vector_subtraction(A, B):
        return [B[0] - A[0], B[1] - A[1], B[2] - A[2]]

    @staticmethod
    def vector_length(x, y, z):
        return sqrt(x ^ 2 + y ^ 2 + z ^ 2)

    @staticmethod
    def triangle_surface(A, B):
        return (sqrt(pow(A[1] * B[2] - A[2] * B[1], 2) +
                     pow(A[2] * B[0] - A[0] * B[2], 2) +
                     pow(A[0] * B[1] - A[1] * B[0], 2))) / 2


if __name__ == '__main__':
    sv = SurfaceVolumeRatio()
    fitness = sv.calculate_volume_surface_ratio(sys.argv[1])
    print(fitness)
