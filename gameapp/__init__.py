import os

# load pythonsta libraries
if os.name == 'posix': 

    import gameapp.ios_constants as kb
    from gameapp.ios_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection
    from gameapp.rect import Rect, Position
    
#load pygame libraries
elif os.name == 'nt':
    import pygame
    import pygame.constants as kb
    from gameapp.rect import Rect, Point
    #from pygame import Rect 
    from gameapp.win_gameapp import GameApp, GameText, GameFont, GameImage, GameAudio, GameSection