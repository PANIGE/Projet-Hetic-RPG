import os 
from framework.data.data import *
from framework.graphics.spriteManager import SpriteManager
from menus.menuManager import MenuManager
from framework.audio.audioManager import AudioManager as am

Debug = False

Running = False

currentDirectory = os.getcwd()
surface = None
windowManager:WindowManager = WindowManager()
clock = None
cursorPos:vector2 = vector2(0,0)
cursor = None
MenuManager:MenuManager = None
AudioManager:am = None
UserEvents = {}
PixelWhite = "pixel.png"
Scheduler = None
Background = None
LastActive = None
Afk = False
Logger = None
Config = None
db = None
playing = None
Framerate = 30

volume = 1


#Cache to transit data between menus
cache = None

#SpriteManagers
backgroundSprites:SpriteManager = SpriteManager()
foregroundSprites:SpriteManager = SpriteManager()
overlaySprites:SpriteManager = SpriteManager()


#Windows
WindowLeft = None
WindowCenter = None
WindowRight = None