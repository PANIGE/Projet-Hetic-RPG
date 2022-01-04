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


def Attack_basic_1(lis):
    pixel1 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    pixel1.VectorScale(vector2(10,10))
    pixel1.Depth = -5
    pixel1.position = vector2(-260,-20)
    pixel1.angularMove(45, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(pixel1)
    lis.append(pixel1)
    time.sleep(3)

def Attack_basic_2(lis):
    pixel2 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    pixel2.VectorScale(vector2(10,10))
    pixel2.Depth = -5
    pixel2.position = vector2(260,-20)
    pixel2.angularMove(135, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(pixel2)
    lis.append(pixel2)
    time.sleep(3)
    lis.clear()
    lis.clear()

def attack_retour(lis):
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
    lis.clear()


def attack_cercle(lis):
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

def attack_m2_croix(lis):
     pixel3= pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
     pixel3.VectorScale(vector2(20,10))
     pixel3.Depth = -5
     pixel3.position = vector2(0,-20)
     pixel3.angularMove(90,850,2000,EaseTypes.easeOut)
     glob.foregroundSprites.add(pixel3)
     lis.append(pixel3)

     pixel4= pSprite(glob.PixelWhite, vector2(200,0), SkinSource.local, Positions.centre, Positions.centre)
     pixel4.VectorScale(vector2(20,10))
     pixel4.Depth = -5
     pixel4.position = vector2(0,200)
     pixel4.angularMove(180,1500,2000,EaseTypes.easeOut)
     glob.foregroundSprites.add(pixel4)
     lis.append(pixel4)
     
def attack_m2_droite(lis):
        pixel5= pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
        pixel5.VectorScale(vector2(10,20))
        pixel5.Depth = -5
        pixel5.position = vector2(0,200)
        pixel5.angularMove(90,1500,8000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel5)
        lis.append(pixel5)

        pixel5= pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
        pixel5.VectorScale(vector2(10,20))
        pixel5.Depth = -5
        pixel5.position = vector2(0,200)
        pixel5.angularMove(-90,1500,8000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel5)
        lis.append(pixel5)
        time.sleep(500)

def attack_m2_verical(lis):
        pixel6= pSprite(glob.PixelWhite, vector2(100,-200), SkinSource.local, Positions.centre, Positions.centre)
        pixel6.VectorScale(vector2(20,10))
        pixel6.Depth = -5
        pixel6.position = vector2(0,100)
        pixel6.angularMove(90,1500,8000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel6)
        lis.append(pixel6)

        pixel7= pSprite(glob.PixelWhite, vector2(-100,200), SkinSource.local, Positions.centre, Positions.centre)
        pixel7.VectorScale(vector2(20,10))
        pixel7.Depth = -5
        pixel7.position = vector2(0,100)
        pixel7.angularMove(-90,1500,8000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel7)
        lis.append(pixel7)

def attack_m2_horizontal(lis):
        pixel6= pSprite(glob.PixelWhite, vector2(200,-200), SkinSource.local, Positions.centre, Positions.centre)
        pixel6.VectorScale(vector2(20,10))
        pixel6.Depth = -5
        pixel6.position = vector2(0,330)
        pixel6.angularMove(180,1500,5000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel6)
        lis.append(pixel6)

        pixel7= pSprite(glob.PixelWhite, vector2(-600,300), SkinSource.local, Positions.centre, Positions.centre)
        pixel7.VectorScale(vector2(20,10))
        pixel7.Depth = -5
        pixel7.position = vector2(300,-25)
        pixel7.angularMove(-360,1500,5000,EaseTypes.easeOut)
        glob.foregroundSprites.add(pixel7)
        lis.append(pixel7)

def attack_m2(lis):
        pixel7= pSprite(glob.PixelWhite, vector2(200,-200), SkinSource.local, Positions.centre, Positions.centre)
        pixel7.VectorScale(vector2(20,10))
        pixel7.Depth = -5
        pixel7.position = vector2(0,330)
        pixel7.angularMove(180,400,5000,EaseTypes.easeOut)
        glob.Scheduler.AddDelayed( 8000 - 1000, pixel7.angularMove, angle=-90, dis= 500, duration=2000, easing=EaseTypes.easeInOut)
        time.sleep(0.05)
        glob.Scheduler.AddDelayed( 8000 - 1000, pixel7.angularMove, angle=90, dis= 500, duration=2000, easing=EaseTypes.easeInOut)
        time.sleep(0.05)
        glob.Scheduler.AddDelayed(7000 - 1000, pixel7.angularMove, angle=15, dis= 5500, duration=5000, easing=EaseTypes.easeInOut)
        time.sleep(0.05)
        glob.foregroundSprites.add(pixel7)
        lis.append(pixel7)

        pixel8= pSprite(glob.PixelWhite, vector2(-600,300), SkinSource.local, Positions.centre, Positions.centre)
        pixel8.VectorScale(vector2(20,10))
        pixel8.Depth = -5
        pixel8.position = vector2(303,-25)
        pixel8.angularMove(-360,500,5000,EaseTypes.easeOut)
        glob.Scheduler.AddDelayed( 8000 - 1000, pixel8.angularMove, angle=90, dis= 500, duration=2000, easing=EaseTypes.easeInOut)
        time.sleep(0.05)
        glob.Scheduler.AddDelayed(7000 - 1000, pixel8.angularMove, angle=215, dis= 5500, duration=5000, easing=EaseTypes.easeInOut)
        time.sleep(0.05)
        glob.foregroundSprites.add(pixel8)
        lis.append(pixel8)


        