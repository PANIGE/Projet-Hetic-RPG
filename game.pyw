########################################################
# Main game script, used to be ran within nothing else #
########################################################
import sys
import time
import ctypes
import pygame

from pygame.locals import *

from framework import glob

from framework.data import helper, ErrorHandler
from framework.data.Scheduler import Scheduler
from framework.data.data import *
from framework.data.database import Db
from framework.data.log import log
from framework.graphics.cursor import cursor
from framework.graphics.pSprite import pSprite
from framework.graphics.pText import pText
from framework.serializers.config import Config
from framework.audio.audioManager import AudioManager
from menus.menuManager import MenuManager
import traceback

if __name__ == "__main__": #avoid script to be runned in another script

    #Initialize all global variables
    glob.Config = Config()
    glob.db = Db()

    glob.volume = glob.Config["volume"]
    pygame.init()
    pygame.font.init()

    wd, ht = 1920, 1080

    if pygame.display.Info().current_w == 1920 and pygame.display.Info().current_h == 1080:
        flags = HWSURFACE |  DOUBLEBUF | HWACCEL | NOFRAME
    else:
        flags = HWSURFACE |  DOUBLEBUF | HWACCEL


    glob.windowManager.width = wd
    glob.windowManager.height = ht
    glob.windowManager.heightScaled = ht / glob.windowManager.getPixelSize()
    glob.windowManager.widthScaled = wd / glob.windowManager.getPixelSize()
    glob.Scheduler = Scheduler()

    #Initialize pygame

    glob.surface = pygame.display.set_mode((glob.windowManager.width, glob.windowManager.height), display=0, flags=flags)
    pygame.display.set_caption("DDFramework - RPG Game")


    glob.Logger = log()

    glob.AudioManager = AudioManager()
    glob.MenuManager = MenuManager()



    cursor = cursor()
    glob.cursor = cursor


    glob.clock = pygame.time.Clock()
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #Transparent cursor to let in game cursor do his work


    #Get the main menu and playing the main audio
    glob.MenuManager.ChangeMenu(Menus.MainMenu)

    #setting afk time to now
    glob.LastActive = time.time()*1000


    glob.Running = True
    glob.Logger.write("Initialised")
    try:
        while glob.Running: #Main Loop

            #Update frame behind background
            glob.surface.fill((0, 0, 0))

            glob.clock.tick(50)

            cursor.updateCursorPos()



            events =pygame.event.get()
            glob.MenuManager.HandleEvents(events)
            for event in events:
                if event.type == pygame.QUIT:
                    glob.Running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1,2,3):
                        cursor.onClick()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in (1, 2,3):
                        cursor.onRelease()
                if event.type == pygame.MOUSEMOTION:
                    glob.LastActive = time.time()*1000


            glob.MenuManager.activeMenu.update()


            glob.backgroundSprites.draw()
            glob.foregroundSprites.draw()
            glob.overlaySprites.draw()
            cursor.draw()


            pygame.display.flip()
    except Exception as e:
        ErrorHandler.raiseError(e)
        pygame.quit()
        if not glob.Debug:
            ctypes.windll.user32.MessageBoxW(0, "this game encountered an Error and couldn't continue Working\n\n"+traceback.format_exc()+"\n\nSee logs for further informations", "Delta Dash - Crash", 0)

    pygame.quit()
    sys.exit(0)
