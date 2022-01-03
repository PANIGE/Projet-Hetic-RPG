from framework.graphics.pSprite import pSprite
from menus.overlays.pNotification import Notification
from framework.graphics.pText import pText
from menus.Elements.CharacterSprite import CharacterSprite
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
import pygame
from os import path
import  time
import numpy
from random import randint
import math


def first(lis):
    pixel1 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    pixel1.VectorScale(vector2(10,10))
    pixel1.Depth = -5
    pixel1.position = vector2(-260,-20)
    pixel1.angularMove(45, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(pixel1)
    lis.append(pixel1)
    time.sleep(3)

    pixel2 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    pixel2.VectorScale(vector2(10,10))
    pixel2.Depth = -5
    pixel2.position = vector2(260,-20)
    pixel2.angularMove(135, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(pixel2)
    lis.append(pixel2)
    time.sleep(3)

    PlayButton = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    PlayButton.VectorScale(vector2(500,200))
    PlayButton.borderBounds(20)
    PlayButton.onHover(PlayButton.FadeColorTo, color=Color(255,0,0), duration=300)
    PlayButton.onHoverLost(PlayButton.FadeColorTo, color=Color(255,255,255), duration=300)
    PlayButton.onClick("a")
    PlayButton.Depth = 0
    glob.foregroundSprites.add(PlayButton)

    for i in range(4):
        for o in range(3):
            p = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
            p.VectorScale(vector2(10,10))
            p.Depth = -5
            p.position = vector2(0,-30)
            p.angularMove(110 -i*20 + (o*5), 800, 4500, EaseTypes.easeOut)
            glob.foregroundSprites.add(p)
            glob.Scheduler.AddDelayed(7000 - i*1000, p.angularMove, angle=290 - i*20 + (o*5), dis= 1000, duration=2000, easing=EaseTypes.easeInOut)
            glob.Scheduler.AddDelayed(8000 - i*1000, p.FadeTo, value=0, duration=500)
            lis.append(p)
        time.sleep(1)
    time.sleep(5)

    pl = []


    t = (time.time()*1000) + 1500
    for i in range(72):
        angle = i*5
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        centre = vector2(0, 205)
        dist = 300
        pos = vector2(0+(cos*dist), 205+(sin*dist))
        p = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
        
        p.VectorScale(vector2(10,10))
        p.Depth = -5
        p.position = pos
        glob.foregroundSprites.add(p)
        lis.append(p)
        pl.append(p)

        p.transformations["position"]["beginTime"] = t
        p.transformations["position"]["endTime"] = t + 2000
        p.transformations["position"]["beginValue"] = p.position
        p.transformations["position"]["endValue"] = vector2(0,205)
        p.transformations["position"]["easing"] = EaseTypes.linear
        p.transformations["position"]["loop"] = False

        p.transformations["fade"]["beginTime"] = t+499
        p.transformations["fade"]["endTime"] = t+500
        p.transformations["fade"]["beginValue"] = 1
        p.transformations["fade"]["endValue"] = 0
        p.transformations["fade"]["easing"] = EaseTypes.linear
        p.transformations["fade"]["loop"] = False
        time.sleep(0.02)
    time.sleep(0.5)
    for p in pl:
        glob.foregroundSprites.remove(p)
    lis.clear()

class attacks:
    def __init__(self) -> None:
        self.Pv=20
        self.MaxPv=20
        self.PvM=30
        self.MaxPvM=30

    def init(self):
        self.whiteLifeJ=pSprite(glob.PixelWhite,vector2(-250,0),SkinSource.local,Positions.centre,Positions.topRight)
        self.redLifeJ=pSprite(glob.PixelWhite,vector2(-260,10),SkinSource.local,Positions.centre,Positions.topRight,Color(255,0,0))
        self.whiteLifeJ.VectorScale(vector2((self.MaxPv/self.MaxPv)*200+20,50))
        self.redLifeJ.VectorScale(vector2((self.Pv/self.MaxPv)*200,30))
        glob.foregroundSprites.add(self.whiteLifeJ)
        glob.foregroundSprites.add(self.redLifeJ)
        
        self.whiteLifeM=pSprite(glob.PixelWhite,vector2(450,0),SkinSource.local,Positions.centre,Positions.topRight)
        self.redLifeM=pSprite(glob.PixelWhite,vector2(440,10),SkinSource.local,Positions.centre,Positions.topRight,Color(0,0,255))
        self.whiteLifeM.VectorScale(vector2((self.MaxPvM/self.MaxPvM)*200+20,50))
        self.redLifeM.VectorScale(vector2((self.PvM/self.MaxPvM)*200,30))
        glob.foregroundSprites.add(self.whiteLifeM)
        glob.foregroundSprites.add(self.redLifeM)

        glob.Scheduler.AddNow(self.Script)

    def healing (self,quantity):
        self.Pv+=quantity
        self.Pv=min(self.MaxPv, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.Pv/self.MaxPv)*200,30))

    def Take_dommage(self,quantity):
        self.Pv-=quantity
        self.Pv = max(0, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.Pv/self.MaxPv)*200,30))
        if self.Pv <= 0:
            self.hideCombat()
            self.gameOver()
            return False
        return True

    def Take_dommage_M(self,quantity):
        self.PvM-=quantity
        self.PvM= max(0, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.PvM/self.MaxPvM)*200,30))
        if self.PvM <= 0:
            self.hideCombat()

            return False
        return True

 