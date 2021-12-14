from framework.data.data import *
from menus import mainMenu
from menus import Play
from framework import  glob


class MenuManager:
    def __init__(self):
        self.activeMenu = None
        self.MenuType = None

    def ChangeMenu(self, type):
        """Handle menu changing, disposing the actual menu """
        if self.activeMenu != None:
            self.activeMenu.dispose()
            glob.Scheduler.killThreads()
            disposeTime = self.activeMenu.disposeTime
            for sprite in glob.foregroundSprites.sprites:
                glob.Scheduler.AddDelayed(disposeTime, glob.foregroundSprites.remove, sprite=sprite)
        self.MenuType = type
        self.activeMenu = self.getMenuFromType(type)
        self.activeMenu.init()


    def getMenuFromType(self, type):
        if type == Menus.MainMenu:
            return mainMenu.handler()
        if type == Menus.Play:
            return Play.handler()

    def HandleEvents(self, events):
        self.activeMenu.HandleEvents(events)


