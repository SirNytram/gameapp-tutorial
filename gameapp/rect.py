from os import error
from typing import Tuple, List
import math

class Color():
    def __init__(self, *args, **kwargs): 
        self._r = 0
        self._g = 0
        self._b = 0
        for i, arg in enumerate(args):
            if type(arg) == str:
                self.setColorByName(arg)
            elif type(arg) == int:
                if i == 0:
                    self._r = arg
                if i == 1:
                    self._g = arg
                if i == 2:
                    self._b = arg

        if 'name' in kwargs:
            self.setColorByName(kwargs['name'])
        if 'r' in kwargs:
            self._r = kwargs['r']
        if 'g' in kwargs:
            self._g = kwargs['g']
        if 'b' in kwargs:
            self._b = kwargs['b']

        self._changed = False

    def setColorByName(self, name:str):
        if name == 'red':
            self._r = 255
            self._g = 0
            self._b = 0
        elif name == 'green':
            self._r = 0
            self._g = 255
            self._b = 0
        elif name == 'blue':
            self._r = 0
            self._g = 0
            self._b = 255
        elif name == 'black':
            self._r = 0
            self._g = 0
            self._b = 0
        elif name == 'white':
            self._r = 255
            self._g = 255
            self._b = 255
        elif name == 'yellow':
            self._r = 255
            self._g = 255
            self._b = 0
        elif name == 'cyan':
            self._r = 0
            self._g = 255
            self._b = 255
        elif name == 'purple':
            self._r = 255
            self._g = 0
            self._b = 255
        elif name == 'gray':
            self._r = 128
            self._g = 128
            self._b = 128

    @property
    def rgb(self)->Tuple[int,int,int]:  
        return (self._r, self._g, self._b)

    @rgb.setter
    def rgb(self, value: Tuple[int,int,int]):
        self._r = value[0]
        self._g = value[1]
        self._b = value[2]
        self._changed = True
    
    @property
    def r(self)->int:  
        return self._r

    @r.setter
    def r(self, value: int):
        self._r = value
        self._changed = True
        
    @property
    def g(self)->int:  
        return self._g

    @g.setter
    def g(self, value: int):
        self._g = value
        self._changed = True

    @property
    def b(self)->int:  
        return self._b

    @b.setter
    def b(self, value: int):
        self._b = value
        self._changed = True

    ################ 

    def __getitem__(self, i):
        if i < 0 or i > 2:
            raise Exception('value must be 0,1,2 (rgb)')
        if i == 0:
            return self._r
        elif i == 1:
            return self._g
        elif i == 2:
            return self._b
        else:
            return 0

    def __copy__(self):
        return Color(self._r, self._g, self._b)

    def __deepcopy__(self):
        return Color(self._r, self._g, self._b)

    def copy(self):
        return self.__copy__()

class Point():
    # left: float
    # top: float
    # x: float
    # y: float
    # point: Tuple[float, float]

    def __init__(self, left: float = 0.0, top: float = 0.0): 
        self._left = float(left)
        self._top = float(top)
        self._changed = False

    @property
    def left(self)->float:  
        return self._left

    @left.setter
    def left(self, value: float):
        self._left = float(value)
        self._changed = True

    @property
    def top(self)->float: 
        return self._top

    @top.setter
    def top(self, value: float):
        self._top = float(value)
        self._changed = True

    @property
    def x(self)->float: 
        return self._left

    @x.setter
    def x(self, value: float):
        self._left = value
        self._changed = True

    @property
    def y(self)->float: 
        return self._top

    @y.setter
    def y(self, value: float):
        self._top = value
        self._changed = True

    @property
    def point(self)->Tuple[float,float]:
        return (self._left, self._top)

    @point.setter
    def point(self, value:Tuple[float,float]):
        self._left = value[0]
        self._top = value[1]
        self._changed = True

    @property
    def topleft(self)->Tuple[float,float]:
        return (self._left, self._top)

    @topleft.setter
    def topleft(self, value:Tuple[float,float]):
        self._left = value[0]
        self._top = value[1]
        self._changed = True
    ######################

    def __getitem__(self, i):
        if i == 0:
            return self._left
        elif i == 1:
            return self._top
        else:
            raise Exception('value must be 0 or 1')

    def __copy__(self):
        return Point(self._left, self._top)

    def copy(self):
        return self.__copy__()

    def __deepcopy__(self):
        return Point(self._left, self._top)

    def __repr__(self) -> str:
        return f'Point({self._left},{self._top})'
    ###############
    def distanceTo(self, point)->float:
        if type(point) != Point:
            point = Point(point[0], point[1])

        dx = self._left - point._left
        dy = self._top - point._top
        return math.sqrt((dx*dx)+(dy*dy))

    def rotateAround(self, angle, point):
        if type(point) != Point:
            point = Point(point[0], point[1])

        ang = math.radians(angle)
        c = math.cos(ang)
        s = math.sin(ang)
        px = self._left - point._left
        py = self._top - point._top

        xnew = px * c - py * s
        ynew = px * s + py * c

        self.x = xnew + point._left
        self.y = ynew + point._top


class Rect():
    # x: float
    # y: float
    # top: float
    # left: float
    # bottom: float
    # right: float
    # topleft: Tuple[float, float]
    # bottomleft: Tuple[float, float]
    # topright: Tuple[float, float]
    # bottomright: Tuple[float, float]
    # size: Tuple[float, float]

    # midtop: Tuple[float, float]
    # midleft: Tuple[float, float]
    # midbottom: Tuple[float, float]
    # midright: Tuple[float, float]
    # center: Tuple[float, float]
    # centerx: float
    # centery: float

    # width: float
    # height: float
    # w: float
    # h: float

    # noqa
    def __init__(self, left: float = 0.0, top: float = 0.0, width: float = 0.0, height: float = 0.0): # noqa
        self._left = float(left)
        self._top = float(top)
        self._width = float(width)
        self._height = float(height)
        self._changed = False

    @property
    def left(self)->float:  
        return self._left

    @left.setter
    def left(self, value: float):
        self._left = float(value)
        self._changed = True

    @property
    def top(self)->float: 
        return self._top

    @top.setter
    def top(self, value: float):
        self._top = float(value)
        self._changed = True

    @property
    def width(self)->float: 
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = float(value)
        self._changed = True

    @property
    def height(self)->float: 
        return self._height
        self._changed = True

    @height.setter
    def height(self, value: float):
        self._height = float(value)
        self._changed = True


    #####################################


    @property
    def w(self)->float: 
        return self._width

    @w.setter
    def w(self, value: float):
        self._width = value
        self._changed = True

    @property
    def h(self)->float: 
        return self._height

    @h.setter
    def h(self, value: float):
        self._height = value
        self._changed = True

    @property
    def x(self)->float: 
        return self._left

    @x.setter
    def x(self, value: float):
        self._left = value
        self._changed = True

    @property
    def y(self)->float: 
        return self._top

    @y.setter
    def y(self, value: float):
        self._top = value
        self._changed = True

    @property
    def right(self)->float: 
        return self._left + self._width

    @right.setter
    def right(self, value: float):
        self._left = value - self._width
        self._changed = True

    @property
    def bottom(self)->float: 
        return self._top + self._height

    @bottom.setter
    def bottom(self, value: float):
        self._top = value - self._height
        self._changed = True

    #######################

    @property
    def topleft(self)->Tuple[float,float]:
        return (self._left, self._top)

    @topleft.setter
    def topleft(self, value:Tuple[float,float]):
        self._left = value[0]
        self._top = value[1]
        self._changed = True
        # print(self._changed)

    @property
    def bottomleft(self)->Tuple[float,float]:
        return (self.left, self.bottom)

    @bottomleft.setter
    def bottomleft(self, value:Tuple[float,float]):
        self.left = value[0]
        self.bottom = value[1]

    @property
    def topright(self)->Tuple[float,float]:
        return (self.right, self.top)

    @topright.setter
    def topright(self, value:Tuple[float,float]):
        self.right = value[0]
        self.top = value[1]

    @property
    def bottomright(self)->Tuple[float,float]:
        return (self.right, self.bottom)

    @bottomright.setter
    def bottomright(self, value:Tuple[float,float]):
        self.right = value[0]
        self.bottom = value[1]

    @property
    def size(self)->Tuple[float,float]:
        return (self._width, self._height)

    @size.setter
    def size(self, value:Tuple[float,float]):
        self._width = value[0]
        self._height = value[1]
        self._changed = True

    ##### 

    @property
    def center(self)->Tuple[float,float]:
        return (self._left + (self._width / 2), self._top + (self._height / 2))

    @center.setter
    def center(self, value:Tuple[float,float]):
        self._left = value[0] - (self._width / 2)
        self._top = value[1] - (self._height / 2)
        self._changed = True

    @property
    def centerx(self)->float:
        return self.center[0]

    @centerx.setter
    def centerx(self, value:float):
        self.center = (value, self.center[1])

    @property
    def centery(self)->float:
        return self.center[1]

    @centery.setter
    def centery(self, value:float):
        self.center = (self.center[0], value)


    @property
    def midtop(self)->Tuple[float,float]:
        return (self._left + (self._width / 2), self._top)

    @midtop.setter
    def midtop(self, value:Tuple[float,float]):
        self._left = value[0] - (self._width / 2)
        self._top = value[1]
        self._changed = True

    @property
    def midbottom(self)->Tuple[float,float]:
        return (self._left + (self._width / 2), self._top + self._height)

    @midbottom.setter
    def midbottom(self, value:Tuple[float,float]):
        self._left = value[0] - (self._width / 2)
        self._top = value[1] - self._height
        self._changed = True

    @property
    def midleft(self)->Tuple[float,float]:
        return (self._left, self._top + (self._height / 2))

    @midleft.setter
    def midleft(self, value:Tuple[float,float]):
        self._left = value[0]
        self._top = value[1] - (self._height / 2)
        self._changed = True

    @property
    def midright(self)->Tuple[float,float]:
        return (self._left + self._width, self._top + (self._height / 2))

    @midright.setter
    def midright(self, value:Tuple[float,float]):
        self._left = value[0] - self._width
        self._top = value[1] - (self._height / 2)
        self._changed = True

    #######
    def __getitem__(self, i):
        if i == 0:
            return self._left
        elif i == 1:
            return self._top
        elif i == 2:
            return self._width
        elif i == 3:
            return self._height
        else:
            raise Exception('value must be 0,1,2,3')

    def __copy__(self):
        return Rect(self._left, self._top, self._width, self._height)

    def copy(self):
        return self.__copy__()

    def __deepcopy__(self):
        return Rect(self._left, self._top, self._width, self._height)

    def __repr__(self) -> str:
        return f'Rect({self._left},{self._top},{self._width},{self._height})'

    #######

    def collides(self, object)->bool:
        ret = False

        if type(object) == Rect:
            if self.left < object.right and \
                self.right > object.left and \
                self.top < object.bottom and \
                self.bottom > object.top :
                    ret = True
        elif type(object) == Point:
            if self.left < object.x and \
                self.right > object.x and \
                self.top < object.y and \
                self.bottom  > object.y :
                    ret = True
        return ret


    def collidesList(self, list)->int:
        ret = -1
        for i, object in enumerate(list):
            if self.collides(object):
                return i

        return ret

    def contains(self, object)->bool:
        ret = False

        if type(object) == Rect:
            if self.left < object.left and \
                self.right > object.right and \
                self.top < object.top and \
                self.bottom > object.bottom :
                    ret = True
        elif type(object) == Point:
            if self.left < object.x and \
                self.right > object.x and \
                self.top < object.y and \
                self.bottom  > object.y :
                    ret = True

        return ret
        
    def containsList(self, list):
        ret = -1
        for i, rect in enumerate(list):
            if self.contains(rect):
                return i

        return ret

