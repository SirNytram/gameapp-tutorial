
from gameapp.win_gameapp import GameShapeRect
from gameapp import GameApp, GameSection, GameImage, kb, GameAudio, GameText, GameFont, Rect, Point

import math

class Flappy():
    def __init__(self, gameapp:GameApp) -> None:
        self.gameapp = gameapp
        self.imgs = (GameImage(None, 'flappy1.png', scale=0.5),
            GameImage(None, 'flappy2.png', scale=0.5),
            GameImage(None, 'flappy3.png', scale=0.5),
            GameImage(None, 'flappy2.png', scale=0.5))
        self.curimg = 0
        self.pos = Point()

    def render(self):
        self.imgs[self.curimg % len(self.imgs)].render(self.pos)
        
    def move(self, pressedKeys):

        if kb.K_s in pressedKeys:
            self.pos.y += 5
        if kb.K_w in pressedKeys:
            self.pos.y -= 5
        if kb.K_a in pressedKeys:
            self.pos.x -= 5
        if kb.K_d in pressedKeys:
            self.pos.x += 5

    def animate(self):
        if kb.K_w in self.gameapp.pressedKeys or kb.K_a in self.gameapp.pressedKeys or kb.K_s in self.gameapp.pressedKeys or kb.K_d in self.gameapp.pressedKeys:
                self.curimg += 1        


class MySection(GameSection):
    def __init__(self, gameapp:GameApp):
        self.gameapp = gameapp
        self.img = GameImage(self, 'bluecar.png', position=(200,200), anchor_point=(0.5,0.5), scale=0.5)
        self.img2 = GameImage(self, 'redcar.png', position=(400,200), anchor_point=(0.5,0.5))
        self.img.rotoZoom(90, 1.0)
        self.img2.rotoZoom(90, 1.0)
        self.crash_sound = GameAudio('crash.wav')
        self.text = GameText(self, GameFont(),'', (0,0), (255,0,0))
        self.rect = GameShapeRect(self, Rect(10,10,10,10), color = (255,0,0))
        self.gameapp.addTimer('flappy', 100)
        #  self.addTimerEx('mytimerEx', 5000)
        self.iscolliding1 = False
        self.iscolliding2 = False
        self.flappy = Flappy(self.gameapp)


    def on_timer(self, name):
        if name == 'flappy':
            self.flappy.animate()
            
            # self.img.rotation += 10

        if name == 'mytimerEx':
            self.img2.rotation += 10


    def on_loop(self):





        self.flappy.move(self.gameapp.pressedKeys)


        if kb.K_UP in self.gameapp.pressedKeys:
            if not self.iscolliding1 and not self.iscolliding2:
                self.img.moveAngle(10, self.img.rotation)


        if kb.K_DOWN in self.gameapp.pressedKeys:
            self.img.moveAngle(-10, self.img.rotation)
            # self.img.position.y += 5

        if kb.K_s in self.gameapp.pressedKeys:
            self.img.rotation += 0.5

        if kb.K_RIGHT in self.gameapp.pressedKeys:
            self.img.rotation -= 5
        if kb.K_LEFT in self.gameapp.pressedKeys:
            self.img.rotation += 5

        if kb.K_g in self.gameapp.pressedKeys:
            self.img.moveTo(1, (300,300))


        if self.img.rect.collideRect(self.img2.rect):
            if not self.iscolliding1:
                self.crash_sound.play()
            self.iscolliding1 = True
        else:
            self.iscolliding1 = False

        self.rect.setRect(Rect(200,500,20,20))
        if self.img.rect.containsRect(self.rect.rect) :
            if not self.iscolliding2:
                self.crash_sound.play()

            self.iscolliding2 = True

        else:
            self.iscolliding2 = False


        if kb.K_o in self.gameapp.pressedKeys:
            self.img2.moveTo(1, self.img.position)
        if kb.K_i in self.gameapp.pressedKeys:
            self.img2.rotateAround(1, (300,100))




        self.gameapp.fill()
        self.img.render()
        self.img2.render()
        self.gameapp.drawRect(self.img.rect, (255,0,0), 1)
        self.text.renderText(f'L {self.img.rect.left:.0f} T {self.img.rect.top:.0f}  R {self.img.rect.right:.0f}  B {self.img.rect.bottom:.0f}')
        self.rect.render()
        self.flappy.render()

    # def on_key(self, isDown, key, mod):
    #     if isDown and key == k.K_RIGHT:
    #         self.img.position.x += 5                
    

class MyGame(GameApp):
    def __init__(self):
         super().__init__(displayNumber=1, fps=60, width=600, height=600)
         self.sections['main'] = MySection(self)
         self.currentSectionName = 'main'








MyGame().start()