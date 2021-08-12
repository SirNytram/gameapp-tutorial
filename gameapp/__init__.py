import os

# load pythonsta libraries
if os.name == 'posix': 

    import kb
    from .ios_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
    from .rect import Rect, Point
    
#load pygame libraries
elif os.name == 'nt':
    import pygame
    import pygame.constants as kb
    from gameapp.rect import Rect, Point, Color
    from gameapp.win_gameapp import GameApp, GameSection, GameImage, GameText, GameFont, GameAudio, GameTimer, GameShapeRect, GameShapeCircle, GameShapeLine
