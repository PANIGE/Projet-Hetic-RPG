from framework import glob
from framework.data import helper
from os import path as osp
import pygame
import  time
from framework.data.data import *
from framework.graphics.pSprite import pSprite

class CharacterSprite:
    def __init__(self, path:str, posi:charPos, emot:'list[str]'):
        self.Depth = 0
        self.sprites:dict[str, pSprite] = {}
        t = [Positions.bottomLeft, Positions.bottomCentre, Positions.bottomRight][posi[0]]
        for i in emot:
            self.sprites[i] = (pSprite(osp.join(path, i), vector2(0,0), SkinSource.local, t, t))
            self.sprites[i].Fade(0)
        self.sprites[emot[0]].Fade(1)

        self.position = vector2(0,0)

    def Move(self, vector:vector2):
        self.position = vector
        for i in self.sprites.values():
            i.position = vector

    def Scale(self, scale:float):
        for i in self.sprites.values():
            i.Scale(scale)

    def setChar(self, string):
        for i in self.sprites.values():
            i.Fade(0)
        self.sprites[string].Fade(1)

    def draw(self):
        for i in self.sprites.values():
            i.draw()

    def isonHover(self):
        return False

    def __onClick__(self):
        return False

    def Move(self, vector:vector2, duration=0, Easing=EaseTypes.linear):
        self.position = vector
        for i in self.sprites.values():
            i.MoveTo(vector.x, vector.y, duration, Easing)

    def HoriFlip(self):
        for i in self.sprites.values():
            i.Horiflip()


    def VertFlip(self):
        for i in self.sprites.values():
            i.Vertflip()