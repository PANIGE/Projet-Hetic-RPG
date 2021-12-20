from framework.graphics.pSprite import pSprite
from menus.overlays.pNotification import Notification
from framework.graphics.pText import pText
from framework import glob
from framework.data import helper
from framework.data.data import *
from pygame.locals import *
import pygame
from os import path
import  time

class handler:
    def __init__(self):
        #Here is to define variable, that are used anywhere, detached from other init for readability reasons

        self.disposeTime = 400  # Needed everywhere for the game to know how much time the menu will take to dispose before loading new menu
        pass

    def init(self):
        title=pText("Le réglisse de la veriter",135,FontStyle.regular , vector2(0,30), Positions.topCentre, Positions.topCentre, Color(255,255,255))
        glob.foregroundSprites.add(title)

        PlayText = pText("Jouer", 100, FontStyle.bold, vector2(0,-5),Positions.centre, Positions.centre, Color(0,0,0))
        PlayText.Depth = -1
        glob.foregroundSprites.add(PlayText)
        PlayButton = pSprite(glob.PixelWhite, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
        PlayButton.VectorScale(vector2(500,200))
        PlayButton.borderBounds(20)
        PlayButton.onHover(PlayButton.FadeColorTo, color=Color(255,0,0), duration=300)
        PlayButton.onHoverLost(PlayButton.FadeColorTo, color=Color(255,255,255), duration=300)
        PlayButton.onClick(self.play)
        PlayButton.Depth = 0
        glob.foregroundSprites.add(PlayButton)


        QuitText = pText("Quitter", 100, FontStyle.bold, vector2(0,350),Positions.centre, Positions.centre, Color(0,0,0))
        QuitText.Depth = -1
        glob.foregroundSprites.add(QuitText)
        QuitButton = pSprite(glob.PixelWhite, vector2(0,350), SkinSource.local, Positions.centre, Positions.centre)
        QuitButton.VectorScale(vector2(500,200))
        QuitButton.borderBounds(20)
        QuitButton.onHover(QuitButton.FadeColorTo, color=Color(255,0,0), duration=300)
        QuitButton.onHoverLost(QuitButton.FadeColorTo, color=Color(255,255,255), duration=300)
        QuitButton.onClick(helper.Exit)
        QuitButton.Depth = 0
        glob.foregroundSprites.add(QuitButton)


        bg = pSprite("réglisse_bg.png", vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
        bg.Depth = 2
        bg.Fade(0.3)
        bg.Scale(1920/bg.image.get_width())
        glob.foregroundSprites.add(bg)

        #Define all variables and initial process, ran only one time on Menu Change
        
    def play(self):
        glob.MenuManager.ChangeMenu(Menus.Play)
        pass

    def update(self):
        #Update done every frame for repeated actions
        pass

    def dispose(self):
        for e in glob.foregroundSprites.sprites:
            e.FadeTo(0,400)
        pass



    def HandleEvents(self, events):
        #Done each frame just before update
        pass