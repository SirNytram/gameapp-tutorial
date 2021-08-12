from gameapp import GameApp, GameSection, GameImage, kb, GameAudio, GameText, GameFont, Rect, Point, Color, GameTimer, GameShapeRect, GameShapeCircle
from typing import List
from random import randint

class Flappy():
    def __init__(self):
        self.imgs:List[GameImage] = []
        self.imgs.append(GameImage('flappy1.png'))
        self.imgs.append(GameImage('flappy2.png'))
        self.imgs.append(GameImage('flappy3.png'))
        self.imgs.append(GameImage('flappy2.png'))
        self.curimgno = 0
        self.position = Point(50,300)
        self.scale = 1.0
    
    def get_curimg(self)->GameImage:
        return self.imgs[self.curimgno % len(self.imgs)]

    def render(self):
        imgToRender = self.get_curimg()
        imgToRender.position = self.position
        imgToRender.render()
        
    def move(self, pressedKeys):
        if kb.K_DOWN in pressedKeys:
            self.position.y += 5
        if kb.K_UP in pressedKeys:
            self.position.y -= 5
        if kb.K_LEFT in pressedKeys:
            self.position.x -= 5
        if kb.K_RIGHT in pressedKeys:
            self.position.x += 5

    def animate(self):
        self.curimgno += 1        

class Pipe():
    def __init__(self, number, hole_y):
        self.position = Point(600 + (250 * number), hole_y)
        self.bottom_pipe = GameImage('pipe_long.png')
        self.bottom_pipe.rect.top = self.position.y + 50
        

        self.top_pipe = GameImage('pipe_long.png').rotate(180)
        self.top_pipe.rect.bottom = self.position.y - 50

        self.pipe_parts:List[GameImage] = []

        # master_pipe_part = GameImage('pipe_part.png')
        # last_midbottom = self.bottom_pipe.rect.midbottom
        # while last_midbottom[1] < 600:
        #     pipe_part = GameImage(master_pipe_part)
        #     pipe_part.rect.midtop = last_midbottom
        #     last_midbottom = pipe_part.rect.midbottom
        #     self.pipe_parts.append(pipe_part)

        # master_pipe_part = GameImage('pipe_part.png').rotate(180)
        # last_midtop = self.top_pipe.rect.midtop
        # while last_midtop[1] > 0:
        #     pipe_part = GameImage(master_pipe_part)
        #     pipe_part.rect.midbottom = last_midtop
        #     pipe_part.position.y += 1
        #     last_midtop = pipe_part.rect.midtop
        #     self.pipe_parts.append(pipe_part)

    def move(self):
        self.position.x -= 5
    def render(self):
        self.bottom_pipe.position.x = self.position.x
        self.top_pipe.position.x = self.position.x

        if self.position.x < 700 and self.position.x > -100:
            self.bottom_pipe.render()
            self.top_pipe.render()
            for pipe_part in self.pipe_parts:
                pipe_part.position.x = self.position.x
                pipe_part.render()



    def check_collision(self, flappy:Flappy):
        ret = False
        cur_flappy_img = flappy.get_curimg()
        if cur_flappy_img.rect.right > self.bottom_pipe.rect.left:
            if cur_flappy_img.rect.right < self.bottom_pipe.rect.right:
                if cur_flappy_img.rect.top < self.top_pipe.rect.bottom:
                    ret = True

                if cur_flappy_img.rect.bottom > self.bottom_pipe.rect.top:
                    ret = True
        
        return ret

class FlappyLevel(GameSection):
    def on_start(self):
        self.gameapp.addTimer('flappy', 100)
        self.gameapp.addTimer('pipes', 1000)
        self.bg = GameShapeRect(self.gameapp.rect, color=Color('black'), line_width=0)
        self.flappy = Flappy()
        self.pipes:List[Pipe] = []
        
        for i in range(25):
            self.pipes.append(Pipe(i,randint(100,500)))



    def on_timer(self, timer:GameTimer):
        if timer.name == 'flappy':
            self.flappy.animate()

    def on_key(self, is_down, key, mod):
        if is_down and key == kb.K_ESCAPE:
            self.active = False
            self.gameapp.sections['menu'].active = True
        
    def on_loop(self):
        self.flappy.move(self.gameapp.pressedKeys)
           
        numcollision = 0
        for pipe in self.pipes:
            if pipe.check_collision(self.flappy) == True:
                numcollision += 1
                
        if numcollision == 0:
            for pipe in self.pipes:
                pipe.move()

            

    def on_render(self):
        # if not self.game_over:
            self.bg.render()
            for pipe in self.pipes:
                pipe.render()
            self.flappy.render()

class Menu(GameSection):
    def on_start(self):
        self.text1 = GameText('Press ENTER to start, ESC to quit', color = Color('blue'))
        self.text1.rect.center = self.gameapp.rect.center
        self.text2 = GameText('arrow keys to move', color = Color('blue'))
        self.text2.rect.top = self.text1.rect.bottom + 5
        self.text2.rect.centerx = self.text1.rect.centerx

    def on_render(self):
        self.text1.render()
        self.text2.render()

    def on_key(self, is_down, key, mod):
        if is_down:
            if key in ( kb.K_KP_ENTER, kb.K_RETURN):
                self.active = False
                self.gameapp.sections['flappy'].active = True
            elif key == kb.K_ESCAPE:
                self.gameapp.quit()

game = GameApp(display_number=1, width= 600, height=600)
game.sections['menu'] = Menu(game, True)
game.sections['flappy'] = FlappyLevel(game)
game.start()