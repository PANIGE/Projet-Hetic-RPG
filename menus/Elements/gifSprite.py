from framework import glob
from framework.data import helper
from os import path as osp
import pygame
import  time
from framework.data.data import *
from framework.graphics.pSprite import pSprite
from PIL import Image

class GifSprite:
    def __init__(self, filename:str, position:vector2, skinSource:SkinSource, field:Positions, origin:Positions, color:Color=Color(255,255,255,255), clock:Clocks=Clocks.game):
        self.Depth = 0
        self.sprites:list[pSprite] = []
        self.position = vector2(0,0)
        self.alpha = 1
        self.current = 0
        self.isPlaying = False
        self.frames = 0
        self.requestStop = False
        
        with Image.open('somegif.gif') as im:
            self.frames = im.n_frames
            for i in range(im.n_frames):
                im.seek(i-1)
                s = pSprite("", position, skinSource, field, origin, color, clock, False)
                
                mode = image.mode
                size = image.size
                data = image.tostring()
                s.changeImageFromString(im.tobytes(), (im.width, im.height))
                self.sprites.append(s)

    def Move(self, vector:vector2):
        self.position = vector
        for i in self.sprites.values():
            i.position = vector

    def PlayGif(self, fps:int):
        glob.Scheduler.AddNow(lambda: self.__playgif__(fps))
        
    def __playgif__(self, fps:int):
        if self.isPlaying:
            self.requestStop = True
            while self.requestStop:
                time.sleep(1/100)
        self.isPlaying = True
        while self.isPlaying and not self.requestStop:
            self.current = self.current + 1 if self.current +1 < self.frames else 0
            self.Seek(self.current)
            time.sleep((1000/fps) / 1000)
        self.isPlaying = False
        self.requestStop = False
            

    def Seek(self, i:int):
        self.current = i
        for s in self.sprites:
            s.Fade(0)
        self.sprites[i].Fade()



    def Scale(self, scale:float):
        for i in self.sprites.values():
            i.Scale(scale)

    def draw(self):
        for i in self.sprites.values():
            i.draw()

    def isonHover(self):
        return False

    def __onClick__(self):
        return False

    def MoveTo(self, vector:vector2, duration=0, Easing=EaseTypes.linear):
        self.position = vector
        for i in self.sprites.values():
            i.MoveTo(vector.x, vector.y, duration, Easing)

    def HoriFlip(self):
        for i in self.sprites.values():
            i.Horiflip()


    def VertFlip(self):
        for i in self.sprites.values():
            i.Vertflip()