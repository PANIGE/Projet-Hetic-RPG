from framework.data.data import *
from framework import  glob
from framework.graphics.pSprite import pSprite
import time
from framework.data.data import *
from framework.data import helper
import pygame


class cursor:
    def __init__(self):
        self.sprite = pSprite("cursor.png", vector2(0, 0), SkinSource.local, Positions.topLeft, Positions.topLeft)
        self.sprite.VectorScale(vector2(0.2,0.2))



    def draw(self):
        self.sprite.draw()


    def onClick(self):
        self.sprite.ScaleTo(1.2, 100)
        glob.LastActive = time.time()*1000
        isClicked = False
        for sprite in glob.overlaySprites.sprites:
            if sprite.isonHover:
                isClicked = True
                sprite.__onClick__()

        if not isClicked:
            for sprite in glob.foregroundSprites.sprites:
                if sprite.isonHover:
                    sprite.__onClick__()

    def onRelease(self):
        self.sprite.ScaleTo(1, 100)

    def updateCursorPos(self):
        x, y = pygame.mouse.get_pos()
        self.sprite.position = vector2(x / glob.windowManager.getPixelSize(), y / glob.windowManager.getPixelSize())
        glob.cursorPos = vector2(x, y)
        if (time.time()*1000)-glob.LastActive > 3000 and not glob.Afk:
            glob.Afk = True
            self.sprite.FadeTo(0, 300)
        elif glob.Afk and (time.time()*1000)-glob.LastActive < 3000:
            glob.Afk = False
            self.sprite.FadeTo(1, 100)