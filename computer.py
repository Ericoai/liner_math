#-*-coding:utf-8 -*-
from math import sqrt,acos,pi
from decimal import Decimal,getcontext

getcontext().prec = 30


class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel componen'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'need more input'
    def __init__(self,coordinates):
        try:
            if not coordinates:
                raise valueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

        #zip函数可以将两个列表合为元组×则相反操作
    def plus(self,v):
        new_coordinates = [x + y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def minus(self,v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self,c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def __str__(self):
        return 'Vector:{}'.format(self.coordinates)

    def __eq__(self,v):
        return self.coordinates == v.coorinates

    def magnitude(self):
        new_coordinates = [x * x for x in self.coordinates]
        return sqrt(sum(new_coordinates))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception('Cannot normailize the zero vector')

    def dot(self,v):
        new_coordinates = [x * y for x, y in zip(self.coordinates, v.coordinates)]
        return sum(new_coordinates)

    def angle_with(self,v,in_degrees = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
    def is_zero(self,tolerance = 1e-10):
        return self.magnitude() < tolerance


    def is_parallel_to(self,v):

        return self.is_zero() or v.is_zero() or self.angle_with(v) == pi or self.angle_with(v) == 0


    def is_orthogonal_to(self,v,tolerance = 1e-10):
        return abs(self.dot(v))< tolerance

    def component_orthogonal_to(self,basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self,basis):
        try:
            u  = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self,v):
        try:
            x_1,y_1,z_1 = self.coordinates
            x_2,y_2,z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - y_2*z_1,-(x_1*z_2 - x_2*z_1),x_1*y_2-x_2*y_1]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates+('0',))
                v_embedded_in_R3 = Vector(v.coordinates+('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif(msg == 'too many values to unpanck'or msg == 'need more than 1 vaule to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_parallelogram_with(self,v):
        cross_product = self.cross(v)
        return cross_product.magnitude()



    def area_of_triangle_with(self,v):
        return self.area_of_parallelogram_with(v)/2.0



v = Vector(['-7.22','-3.21','-2.4'])
m = Vector(['1.2','3.4','3.1'])

print (v.is_parallel_to(m))
print (v.is_orthogonal_to(m))
print(v.component_orthogonal_to(m))
print (v.component_parallel_to(m))
print(v.area_of_parallelogram_with(m))
print (v.area_of_triangle_with(m))