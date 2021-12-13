import math
from framework import  glob
import os, random, json
import time
from menus.overlays.pNotification import NotificationMassive
from framework.graphics.pSprite import pSprite
from framework.data.data import *
from os import path
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.isPlaying = False


    def PlayMusic(self, music, loop=True, force=False):
        if self.isPlaying:
            if force:
                self.Stop()
            else:
                return
        pygame.mixer.music.set_volume(glob.volume)
        songFolder = os.path.join(glob.currentDirectory, "data", "tracks", music)
        pygame.mixer.music.load(songFolder)
        loop = -1 if loop else 0
        pygame.mixer.music.play(loop)
        self.isPlaying = True

    def PlaySound(self, filename):
        src = os.path.join(glob.currentDirectory, "data", "sounds", filename)
        s = pygame.mixer.Sound(src)
        s.set_volume(glob.volume)
        s.play()

    def setVolume(self, x):
        x = round(x,2)
        glob.volume = x
        glob.Config.setValue("volume", x, "float")
        pygame.mixer.music.set_volume(x)


    def Stop(self):
        self.isPlaying = False
        pygame.mixer.music.stop()

    def Pause(self):
        self.isPlaying = False
        pygame.mixer.music.pause()

    def Unpause(self):
        self.isPlaying = True
        pygame.mixer.music.unpause()

