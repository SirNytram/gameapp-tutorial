

import pygame
import pygame.constants as kb
from pygame.surface import Surface
from gameapp import Rect, Point, Color
from typing import List, Dict, Tuple
import time
import math

gblScale = 1.0

class GameImage():
    def __init__(self, source = None, position = (0,0), *, anchor_point = (0.5,0.5), rotation:float = 0.0, scale:float = 1.0, show_rect=False):
        self._image = pygame.Surface((0,0))
        self.anchor_point = Point(anchor_point[0],anchor_point[1])
        self.rotation = rotation
        self.scale = scale
        self._position = Point(position[0], position[1])
        self._position._changed = True
        self._rect = Rect(0, 0, 1, 1)
        self.show_rect = show_rect

        self.load(source)  

    ###################### 
    
    @property
    def rect(self)->Rect:
        if self._position._changed:
            self._rect._left = self._position._left - (self._rect._width * self.anchor_point[0])
            self._rect._top = self._position._top - (self._rect._height * self.anchor_point[1])
            self._position._changed = False

        return self._rect

    @rect.setter
    def rect(self, value:Rect):
        self._rect = Rect(value._left, value._top, value._width, value._height)
        self._position._left = self._rect._left + (self._rect._width * self.anchor_point.left)
        self._position._top = self._rect._top + (self._rect._height * self.anchor_point.top)
        self._position._changed = False

    @property
    def position(self)->Point:
        if self._rect._changed:
            self._position._left = self._rect._left + (self._rect._width * self.anchor_point.left)
            self._position._top = self._rect._top + (self._rect._height * self.anchor_point.top)
            self._rect._changed = False

        return self._position

    @position.setter
    def position(self, value:Point):
        self._position = Point(value._left, value._top)
        self._rect._left = self._position._left - (self._rect._width * self.anchor_point[0])
        self._rect._top = self._position._top - (self._rect._height * self.anchor_point[1])
        self._rect._changed = False

    ###################### 


    def load(self, source):
        if source:
            if type(source) == str:
                self._image = pygame.image.load(source).convert_alpha()
            elif type(source) == Surface:
                self._image = source
            elif type(source) == GameImage:
                self._image = source._image

            size = self._image.get_size()
            global gblScale
            newsize = (int(size[0] * gblScale), int(size[1] * gblScale))
            self._image = pygame.transform.scale(self._image, newsize)
            self.updateRect(self._image)


    def updateRect(self, img):
        size = img.get_size()
        self._rect._left = self._position._left-(size[0]*self.anchor_point[0])
        self._rect._top = self._position._top-(size[1]*self.anchor_point[1])
        self._rect._width = size[0]
        self._rect._height = size[1]



    def render(self, position = None):
        if position:
            self.position = Point(position[0], position[1])

        # img = self.image
        if self.rotation == 0.0 and self.scale == 1.0:
            img = self._image
        else:        
            img  = pygame.transform.rotozoom(self._image, self.rotation, self.scale) 
            # self._position._left *= self.scale
            # self._position._top *= self.scale
            self.updateRect(img)


        global gblScale
        scaledposition = Point(self.position.left, self.position.top)
        scaledposition.x *= gblScale        
        scaledposition.y *= gblScale

        pygame.display.get_surface().blit(img, (scaledposition.x-(img.get_size()[0]*self.anchor_point[0]), scaledposition.y-(img.get_size()[1]*self.anchor_point[1])))
        if self.show_rect:
            pygame.draw.rect(pygame.display.get_surface(), (0,255,0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)

    def rotate(self, angle=0):
        self._image = pygame.transform.rotate(self._image, angle)
        self.updateRect(self._image)
        return self

    def resize(self, width, height):
        self._image = pygame.transform.scale(self._image, (width, height))
        self.updateRect(self._image)
        return self

    def rotoZoom(self, angle=0, scale=1.0):
        self._image = pygame.transform.rotozoom(self._image, angle, scale)
        self.updateRect(self._image)
        return self

    def moveAngle(self, dist, angle):
        ang = math.radians(angle)
        dx = dist * math.cos(ang)
        dy = dist * math.sin(ang)
        self.position.x += dx
        self.position.y -= dy
        self.updateRect(self._image)
        return self

    def moveTo(self, dist, position):
        dx = (position[0] - self.position.x)
        dy = -(position[1] - self.position.y)
        
        ang = 0
        if dx > 0:
            ang = math.degrees(math.atan(dy/dx))

        if dx < 0:
            ang += 180

        self.moveAngle(dist, ang)

    def rotateAround(self, angle:float, point):
        ang = math.radians(angle)
        c = math.cos(ang)
        s = math.sin(ang)
        px = self.position.x - point[0]
        py = self.position.y - point[1]
        self.rotation -= angle

        xnew = px * c - py * s
        ynew = px * s + py * c

        self.position.x = xnew + point[0]
        self.position.y = ynew + point[1]
        return self

    def setPixel(self, point = Point(), color = (0,0,0)):
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self._image.set_at((point[0], point[1]), pygame.Color(color.r, color.g, color.b))

    def copy(self):
        gi = GameImage(position = self.position, anchor_point=self.anchor_point, rotation=self.rotation, scale=self.scale, show_rect=self.show_rect)
        gi._image = self._image.copy()
        gi.updateRect(self._image)
        return gi


class GameShapeRect(GameImage):
    def __init__(self, rect = (0,0,0,0), color = (0,0,0), line_width:int = 1, corner_radius:int = 0):
        '''Rectangle Shape'''
        super().__init__()
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        if type(rect) in (tuple, list):
            rect = Rect(rect[0], rect[1], rect[2], rect[3])

        self.rect = rect
        self._image = pygame.Surface((self.rect.width, self.rect.height))

        self.line_width = line_width
        self.corder_radius = corner_radius

    def render(self):
        if self.rect.size != self._image.get_size():
            self._image = pygame.Surface((self.rect.width, self.rect.height))
            self.updateRect(self._image)

        pygame.draw.rect(pygame.display.get_surface(), self.color.rgb, pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height), self.line_width, self.corder_radius)
        
class GameShapeCircle(GameImage):
    def __init__(self, center = (0,0), radius = 0, color = (0,0,0), line_width:int = 1):
        super().__init__(position=center)
        self.radius = radius
        self.line_width = line_width

        self.color = Color(color[0], color[1], color[2])

        self._image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.updateRect(self._image)


    def render(self):
        if self.rect.size != (self.radius * 2, self.radius * 2):
            self._image = pygame.Surface((self.radius * 2, self.radius * 2))
            self.updateRect(self._image)

        pygame.draw.circle(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), (self.position[0], self.position[1]), self.radius, self.line_width)

class GameShapeLine(GameImage):
    def __init__(self, first_point = (0,0), last_point = (0,0), color = (0,0,0), line_width:int = 1):
        super().__init__()
        self.first_point = Point(first_point[0], first_point[1])
        self.last_point = Point(last_point[0], last_point[1])
        self.line_width = line_width

        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color

        self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
        self.updateRect(self._image)


    def render(self):
        if self.rect.size != (self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x):
            self._image = pygame.Surface((self.last_point.x - self.first_point.x, self.last_point.x - self.first_point.x))
            self.updateRect(self._image)
        pygame.draw.line(pygame.display.get_surface(), pygame.Color(self.color.r, self.color.g, self.color.b), self.first_point.point, self.last_point.point, self.line_width)

# class GameShapeTriangle(GameImage):
    # pass


class GameFont():
    def __init__(self, name = 'Verdana', size = 20, is_sys = True):
        self.name = name
        self.size = size
        self.font = None
        self.is_sys = is_sys


    def load(self):
        global gblScale
        if not self.font:
            if self.is_sys:
                self.font = pygame.font.SysFont(self.name, int(self.size * gblScale))
            else:
                self.font = pygame.font.Font(self.name, int(self.size * gblScale))

class GameText(GameImage):
    def __init__(self, text = '', position = (0,0), color = (0,0,0), font = GameFont(), anchor_point = (0.5, 0.5)):
        super().__init__(position=position, anchor_point=anchor_point)
        if type(color) != Color:
            color = Color(color[0], color[1], color[2])
        self.color = color
        self.font = font
        self.text = text

    @property
    def text(self)->str:
        return self._text

    @text.setter
    def text(self, value:str):
        self._text = value
        self.font.load()
        self._image = self.font.font.render(self._text, True, pygame.Color(self.color.r,self.color.g, self.color.b))
        self.updateRect(self._image)

    def renderText(self, text, position = None):
        self.text = str(text)
        self.render(position)


class GameAudio():
    def __init__(self, file_name = None, volume = 1):
        self.mySound:pygame.mixer.Sound = None 
        # self.played = False
        if file_name:
            self.load(file_name)
            self.setVolume(volume)
    
    def load(self, file_name):
        if self.mySound:
            self.mySound.stop()
            
        if '.' not in file_name:
            file_name += '.ogg'

        self.mySound = pygame.mixer.Sound(file_name)

    def play(self, numRepeat = 0):
        # if not self.played:
            self.mySound.play(loops = numRepeat)    
            # self.played = True

    def stop(self):
        self.mySound.stop()
        # self.played = False

    def setVolume(self, volume = 1):
        self.mySound.set_volume(volume)
        
class VirtualKey():
    def __init__(self, parent, label, key, colrow):
        self.parent = parent
        self.label = label
        self.key = key
        self.diameter = 20
        self.spacing = 2.5
        self.distance = (self.diameter*2) + (self.spacing * 2)

        if parent and colrow:
            xpos = self.diameter + self.spacing
            ypos  = self.parent.surface.get_height() - (self.distance * 3) + self.diameter + self.spacing
            self.position = Rect(xpos + (colrow[0]*self.distance), ypos + (colrow[1]*self.distance), 0, 0)
            self.text = GameText(self, GameFont(self, 'Calibri', 20), label, (self.position.x-10, self.position.y-10))
        
        

    def render(self):
        surf = pygame.display.get_surface()
        pygame.draw.circle(surf, (255,255,255), (self.position[0], self.position[1]), self.diameter)
        self.text.render()
        


class GameTimer():
    def __init__(self, name:str, id:int, milliseconds:float, numRepeats:int, delayMS:float=0.0):
        self.active: bool = True
        self.name:str = name
        self.id:int = id
        self.milliseconds:float = milliseconds
        self.numRepeats:int = numRepeats
        self.msAtStart:float = 0.0
        self.numLoopsPerformed:int = 0
        self.delayMS:float = delayMS

    def getNextRunMS(self):
        return self.msAtStart + self.delayMS + ((self.numLoopsPerformed + 1) * self.milliseconds)

class GameSection:
    def __init__(self, gameapp, active:bool = False):
        self.gameapp:GameApp = gameapp
        self.active = active
        self.started_once = False

    def on_start(self):
        pass

    def on_event(self, event_id):
        pass
    
    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_after_render(self):
        pass

    def on_key(self, is_down, key, mod):
        pass

    def on_mouse(self, is_down, key, position = Point()):
        pass

    def on_timer(self, timer: GameTimer):
        pass
        

class GameApp:
    def __init__(self, *, width=640, height=480, display_number = 0, full_screen = False, scale = 1.0, hasVK = False, fps = 60):
        self.hasVK = hasVK
        self.platform = 'win'
        self.isRunning = True
        self._surface = None
        self.rect = Rect(0,0, width, height)
        self._fps = fps
        # self.keysPressed = []
        self.pressedKeys = []
        self.curUserEventId = kb.USEREVENT 

        self._milliseconds_since_start =  time.time() * 1000
        self._milliseconds_since_last_frame = 0.0

        # self.active_section:GameSection = GameSection(self)
        self.sections: Dict[str, GameSection] = {}
        self.virtualKeys: List[VirtualKey] = []
        # self.timersById: Dict[int, GameTimer] = {}
        self.timers: Dict[str, GameTimer] = {}
        # self.timers: List[GameTimer] = []

        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        vkspace = 0
        if hasVK:
            vk = VirtualKey(None, None, None, None)
            vkspace = vk.distance * 3

        global gblScale
        gblScale = scale
        self._surface = pygame.display.set_mode((int(self.rect.width * gblScale), int(self.rect.height * gblScale + vkspace)), display=display_number)
        if full_screen == True:
            pygame.display.toggle_fullscreen()
      
    def getMS(self):
        return self._milliseconds_since_start

    def getLastFrameMS(self):
        return self._milliseconds_since_last_frame 

    def on_start(self):
        for section in self.sections.values():
            if section.active and not section.started_once:
                section.on_start()
                section.started_once = True

    def on_event(self, event_id):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_event(event_id)
    
    def on_loop(self):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_loop()

    def on_render(self):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_render()

    def on_after_render(self):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_after_render()

    def on_key(self, is_down, key, mod):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_key(is_down, key, mod)

    def on_mouse(self, is_down, key, position = Point()):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_mouse(is_down, key, position)

    def on_timer(self, timer:GameTimer):
        for section in self.sections.values():
            if section.active:
                if not section.started_once:
                    section.on_start()
                    section.started_once = True
                    
                section.on_timer(timer)

    def addTimer(self, name, milliseconds:float, numRepeats:int=-1, delayMS=0.0):
        if name not in self.timers:
            self.curUserEventId += 1
            timer = GameTimer(name, self.curUserEventId, milliseconds, numRepeats, delayMS)
            timer.msAtStart = self.getMS()
            self.timers[name]  = timer
        else:
            timer = self.timers[name]
            timer.msAtStart = self.getMS()
            timer.milliseconds = milliseconds
            timer.numRepeats = numRepeats
            timer.numLoopsPerformed = 0
            timer.active = True

    def stopTimer(self, name):
        self.timers[name].active = False




    def start(self):

        if self.hasVK:
            self.virtualKeys.append(VirtualKey(self, 'L', kb.K_LEFT, (5,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', kb.K_RIGHT, (7,1)))
            self.virtualKeys.append(VirtualKey(self, 'U', kb.K_UP, (6,0)))
            self.virtualKeys.append(VirtualKey(self, 'D', kb.K_DOWN, (6,1)))
            self.virtualKeys.append(VirtualKey(self, 'R', kb.K_r, (1,2)))
            self.virtualKeys.append(VirtualKey(self, 'ESC', kb.K_ESCAPE, (1,0)))
            self.virtualKeys.append(VirtualKey(self, 'OK', kb.K_RETURN, (9,2)))


        while( self.isRunning ):

            curTime = time.time() * 1000
            self._milliseconds_since_last_frame = curTime - self._milliseconds_since_start
            self._milliseconds_since_start =  curTime

            # self._milliseconds_since_last_frame = self.clockb.get_time()
            # self._milliseconds_since_start += self._milliseconds_since_last_frame


            # self.keysPressed = pygame.key.get_pressed()
            self.on_start()

            for event in pygame.event.get():
                self.on_event(event.type)

                if event.type == pygame.QUIT:
                    self.isRunning = False

                pos = pygame.mouse.get_pos()
                if event.type == kb.KEYDOWN:
                    self.on_key(True, event.key, event.mod)
                    self.pressedKeys.append(event.key)
                if event.type == kb.KEYUP:
                    self.on_key(False, event.key, event.mod)
                    self.pressedKeys.remove(event.key)

                if event.type in (kb.MOUSEBUTTONDOWN, kb.MOUSEBUTTONUP):
                    for vk in self.virtualKeys:
                        vk: VirtualKey 
                        if pos[0] > vk.position.x - vk.diameter and pos[0] < vk.position.x + vk.diameter and \
                           pos[1] > vk.position.y - vk.diameter and pos[1] < vk.position.y + vk.diameter:
                            self.on_key(event.type == kb.MOUSEBUTTONDOWN, vk.key, None)
                            if event.type == kb.MOUSEBUTTONDOWN:
                                self.pressedKeys.append(vk.key)
                            else:
                                self.pressedKeys.remove(vk.key)

                global gblScale
                if event.type in (kb.MOUSEBUTTONDOWN, kb.MOUSEBUTTONUP):
                    self.on_mouse(event.type == kb.MOUSEBUTTONDOWN, event.button, Point(pos[0] / gblScale, pos[1] / gblScale))


            for timer in self.timers.values():
                if timer.active and self._milliseconds_since_start > timer.getNextRunMS():
                    timer.numLoopsPerformed += 1
                    self.on_timer(timer)
                    #check if last loop
                    #if not infinite timer
                    if timer.numRepeats >= 0 and timer.numLoopsPerformed > timer.numRepeats:
                        timer.active = False


                    
            self.on_loop()
            self.on_render()

            #display virtual keys if we have any
            for vk in self.virtualKeys:
                vk.render()

            pygame.display.flip()

            self.on_after_render()

            self.clock.tick(self._fps)
 
    def quit(self):
        self.isRunning = False


if __name__ == "__main__" :
    
    GameApp().start()
