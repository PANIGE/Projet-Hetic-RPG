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

def first(lis):
    p1 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    p1.VectorScale(vector2(10,10))
    p1.Depth = -5
    p1.position = vector2(-260,-20)
    p1.angularMove(45, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(p1)
    lis.append(p1)
    time.sleep(3)

    p2 = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
    p2.VectorScale(vector2(10,10))
    p2.Depth = -5
    p2.position = vector2(260,-20)
    p2.angularMove(135, 800, 4500, EaseTypes.easeOut)
    glob.foregroundSprites.add(p2)
    lis.append(p2)
    time.sleep(3)

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
    time.sleep(2)
