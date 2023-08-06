from math import radians, cos, sin, sqrt, acos, degrees, pi

class Vector(object):
    def __init__(self, d):
        super(Vector, self).__init__()
        self.__d = d

    def __str__(self):
        i = self.dimensions()
        f = round(self.magnitude(), 3)
        return(str(i) + "D Vector of length " + str(f))

    def __add__(self, other):
        v = []
        try:
            if self.dimensions() >= other.dimensions():
                for i in range(self.dimensions()):
                    try:
                        v.append(self.__d[i] + other.__d[i])
                    except Exception:
                        v.append(self.__d[i])
            else:
                for i in range(other.dimensions()):
                    try:
                        v.append(self.__d[i] + other.__d[i])
                    except Exception:
                        v.append(other.d[i])
        except AttributeError:
            m = self.magnitude() + other
            unit = self.unitVector()
            return unit.scale(m)
        return Vector(v)

    def __sub__(self, other):
        v = []
        try:
            if self.dimensions() >= other.dimensions():
                for i in range(self.dimensions()):
                    try:
                        v.append(self.__d[i] - other.__d[i])
                    except Exception:
                        v.append(self.__d[i])
            else:
                for i in range(other.dimensions()):
                    try:
                        v.append(self.__d[i] - other.__d[i])
                    except Exception:
                        v.append(-other.__d[i])
        except AttributeError:
            m = self.magnitude() - other
            unit = self.unitVector()
            return unit.scale(m)
        return Vector(v)

    def __mul__(self, other):
        return self.scale(other)

    def __truediv__(self, other):
        return self.scale(1 / other)

    def __gt__(self, other):
        if self.magnitude() > other.magnitude():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.magnitude() < other.magnitude():
            return True
        else:
            return False

    def __eq__(self, other):
        if self.magnitude() == other.magnitude():
            return (self.proj(other) == self.magnitude())
        else:
            return False

    def __ne__(self, other):
        return self.magnitude() != other.magnitude() or self.proj(other) != self.magnitude()

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __imul__(self, other):
        return self.scale(other)

    def __idiv__(self, other):
        return self.scale(1 / other)

    def __iter__(self):
        return self.__d.__iter__()

    def x(self):
        """x(), y(), and z() are helper methods to quickly
        get the first three coordinates of a vector"""
        if self.dimensions() < 1:
            return 0
        else:
            return self.__d[0]

    def y(self):
        if self.dimensions() < 2:
            return 0
        else:
            return self.__d[1]

    def z(self):
        if self.dimensions() < 3:
            return 0
        else:
            return self.__d[2]

    def c(self, dim):
        """returns the component of a vector in a given dimension.
        generalization of Vector#x(), y(), and z()"""
        if self.dimensions() < dim + 1:
            return 0
        else:
            return self.__d[dim]

    def magnitude(self):
        sum = 0
        for x in self.__d:
            sum += x**2
        return sqrt(sum)

    def dimensions(self):
        return (len(self.__d))

    def dot(self, other):
        sum = 0
        if self.dimensions() >= other.dimensions():
            for i in range(self.dimensions()):
                try:
                    sum += (self.__d[i] * other.__d[i])
                except Exception:
                    pass
        else:
            for i in range(other.dimensions()):
                try:
                    sum += (self.__d[i] * other.__d[i])
                except Exception:
                    pass
        return sum

    def cross(self, other):
        if self.dimensions() > 3 or other.dimensions() > 3:
            raise ValueError("This function is implemented for <4D vectors!")
        x = self.y() * other.z() - self.z() * other.y()
        y = self.z() * other.x() - self.x() * other.z()
        z = self.x() * other.y() - self.y() * other.x()
        return Vector([x, y, z])

    def proj(self, other):
        return self.magnitude() * cos(self.angleTo(other))

    def angleTo(self, other):
        return acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def toArray(self, rnd=False, r=5):
        if rnd:
            b = []
            for i in self.__d:
                b.append(round(i, r))
            return b
        return self.__d

    def scale(self, mul):
        c = []
        for i in range(self.dimensions()):
            c.append(self.__d[i] * mul)
        return Vector(c)

    def unitVector(self):
        return self.scale(1 / self.magnitude())

    def alphaRad(self, dim):
        """returns the angle between this vector and a given axis in radians"""
        try:
            return acos(self.__d[dim] / self.magnitude())
        except Exception:
            return 0

    def alphaDeg(self, dim):
        """returns the angle between this vector and a given axis in degrees"""
        return degrees(self.alphaRad(dim))

    def sector(self):
        """returns the sector in which this vector lies, in the form
        [-1, 1] (for a 2D vector in quadrant II)"""
        sector = []
        for i in range(self.dimensions()):
            if self.__d[i] != 0:
                sector.append(abs(self.__d[i]) / self.__d[i])
            else:
                sector.append(0)
        return sector

    def __fromMagnitudeRad(m, alphas):
        v = []
        try:
            for i in alphas:
                v.append(m * cos(i))
            print(Vector(v).toMagnitudeAngle())

            if Vector(v).toMagnitudeAngle() == [m, alphas]:
                return Vector(v)
            else:
                raise ValueError("The given angles are not geometrically possible (something is wrong)!")
        except TypeError:
            try:
                return Vector([m * cos(i), m * sin(i)])
            except Exception as e:
                raise e

    def fromTwoPoints(a, b, m=0):
        """generates a vector given two points (direction from a to b)
        m = the length of the vector"""
        c = []
        if len(a) >= len(b):
            for i in range(len(a)):
                c.append(b[i] - a[i])
        else:
            for i in range(len(b)):
                c.append(b[i] - a[i])
        d = Vector(c).toMagnitudeAngle()
        if m != 0:
            d[0] = m
        return Vector.__fromMagnitudeRad(d[0], d[1])

    def fromSpherical(r, theta, phi):
        """returns a 3D vector in spherical coordinates"""
        return Vector.__fromMagnitudeRad(r, [theta, (pi / 2) - theta, phi])

    def toMagnitudeAngle(self):
        alphas = []
        magnitude = self.magnitude()
        for i in self.__d:
            alphas.append(acos(i / magnitude))
        return [magnitude, alphas]

    def toMagnitudeAngleDeg(self):
        alphas = []
        magnitude = self.magnitude()
        for i in self.__d:
            alphas.append(degrees(acos(i / magnitude)))
        return [magnitude, alphas]

    def directionTo(self, other):
        """returns the unit vector in the direction from self to other"""
        return (other - self).unitVector()

    def parallel(self, other, tolerance=0.000000001):
        """true if these vectors are parallel
        within tolerance (default 1e-09rad)"""
        return (abs(self.anglebetween(other)) <= tolerance)

    def perpendicular(self, other, tolerance=0.000000001):
        """true if these vectors are perpendicular
        within tolerance (default 1e-09rad)"""
        return (abs(self.anglebetween(other) - (pi / 2)) <= tolerance)


