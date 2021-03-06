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
from tools import Attacks


class handler:

    isInCombat = False

    def __init__(self) -> None:
        #Here is to define variable, that are used anywhere, detached from other init for readability reasons

        self.disposeTime = 400  # Needed everywhere for the game to know how much time the menu will take to dispose before loading new m
        
        #Outside Dialogs
        self.Dialog = None
        self.bgDialog = None

        self.DialogTitle = None
        self.bgDialogTitle = None
        self.Messages = []
        self.AcceptInput = False
        self.cmd = ""
        self.Title = None
        self.AwaitSymbol = None

        self.whiteLifeJ = None
        self.redLifeJ = None

        self.BattleDialog = None
        self.bgBattleDialog = None

        self.isAwaiting = False

        self.isInCombat = False
        self.heart = None
        self.heartHurted = None
        self.canTakeDamage = True
        self.Pv=20
        self.MaxPv=20
        self.PvM=30
        self.MaxPvM=30
        

        self.AttackSprites = []

        self.Characters = {}

    def load(self):
        #Define all variables and initial process, ran only one time on Menu Change

        self.Dialog = pSprite(glob.PixelWhite, vector2(0, -40), SkinSource.local, Positions.bottomCentre, Positions.bottomCentre, Color(0,0,0))
        self.bgDialog = pSprite(glob.PixelWhite, vector2(0, -30), SkinSource.local, Positions.bottomCentre, Positions.bottomCentre)
        self.Dialog.Depth = -1
        self.bgDialog.Depth = -0.9

        self.Dialog.VectorScale(vector2(1500,300))
        self.bgDialog.VectorScale(vector2(1520,320))
        glob.foregroundSprites.add(self.Dialog)
        glob.foregroundSprites.add(self.bgDialog)

        self.DialogTitle = pSprite(glob.PixelWhite, vector2(-750, -310), SkinSource.local, Positions.bottomCentre, Positions.bottomLeft, Color(0,0,0))
        self.bgDialogTitle = pSprite(glob.PixelWhite, vector2(-760, -300), SkinSource.local, Positions.bottomCentre, Positions.bottomLeft)
        self.DialogTitle.Depth = -0.8
        self.bgDialogTitle.Depth = -0.7

        self.DialogTitle.VectorScale(vector2(400,100))
        self.bgDialogTitle.VectorScale(vector2(420,120))
        glob.foregroundSprites.add(self.DialogTitle)
        glob.foregroundSprites.add(self.bgDialogTitle)
        self.Title = pText("", 40, FontStyle.thin, vector2(-745,-355), Positions.bottomCentre, Positions.bottomLeft)
        self.Title.Depth = -2
        glob.foregroundSprites.add(self.Title)
        self.AwaitSymbol = pText("V", 40, FontStyle.heavy, vector2(0,0), Positions.bottomCentre, Positions.bottomRight)
        self.AwaitSymbol.position = vector2(730, -50)
        self.AwaitSymbol.MoveTo(730, -60, 500, loop=True)
        self.AwaitSymbol.Fade(0)
        self.AwaitSymbol.Depth = -3
        glob.foregroundSprites.add(self.AwaitSymbol)

        self.BattleDialog=pSprite(glob.PixelWhite,vector2(0,10),SkinSource.local, Positions.centre,Positions.topCentre,Color(0,0,0))
        self.bgBattleDialog=pSprite(glob.PixelWhite,vector2(0,0),SkinSource.local, Positions.centre,Positions.topCentre)
        self.BattleDialog.VectorScale(vector2(400,400))
        self.bgBattleDialog.VectorScale(vector2(420,420))
        self.BattleDialog.Depth = -1
        self.bgBattleDialog.Depth = -0.1

        
        glob.foregroundSprites.add(self.BattleDialog)
        glob.foregroundSprites.add(self.bgBattleDialog)
        self.heart=pSprite("heart.png",vector2(0,0),SkinSource.local,Positions.centre,Positions.centre)
        self.heartHurted=pSprite("heart-hurt.png",vector2(0,0),SkinSource.local,Positions.centre,Positions.centre)
        self.heart.Depth = -2
        self.heartHurted.Depth = -2
        glob.foregroundSprites.add(self.heart)
        glob.foregroundSprites.add(self.heartHurted)

        self.heart.Scale(0.2)
        self.heartHurted.Scale(0.2)

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

        self.Text = pText("attaquer", 25, FontStyle.bold, vector2(355,100),Positions.centre, Positions.centre, Color(0,0,0))
        self.Text.Depth = -1
        glob.foregroundSprites.add(self.Text)
        self.AttackButton = pSprite(glob.PixelWhite, vector2(350,100), SkinSource.local, Positions.centre, Positions.centre)
        self.AttackButton.VectorScale(vector2(230,50))
        self.AttackButton.borderBounds(10)
        self.AttackButton.onHover(self.AttackButton.FadeColorTo, color=Color(255,255,0), duration=300)
        self.AttackButton.onHoverLost( self.AttackButton.FadeColorTo, color=Color(255,255,255), duration=300)
        self.AttackButton.onClick(lambda: self.Take_dommage_M(4))
        self.AttackButton.Depth = 0
        glob.foregroundSprites.add(self.AttackButton) 

        #TOUJOURS EN DERNIER
        glob.Scheduler.AddNow(self.Script)





    def SwitchBackground(self, path, duration):
        if len(glob.backgroundSprites.sprites) > 0:
            glob.backgroundSprites.sprites[0].FadeTo(0, duration)
            glob.Scheduler.AddDelayed(duration, lambda:glob.backgroundSprites.remove(glob.backgroundSprites.sprites[0]))
        if path is not None:
            bg = pSprite(path, vector2(0,0), SkinSource.local, Positions.centre, Positions.centre)
            bg.Scale(1920/bg.image.get_width())
            bg.Fade(0)
            bg.FadeTo(1, duration)
            glob.backgroundSprites.add(bg)
                   

    def hideCombat(self):
        self.isInCombat = False
        self.BattleDialog.Fade(0)
        self.bgBattleDialog.Fade(0)
        self.heart.Fade(0)
        self.heartHurted.Fade(0)
        self.whiteLifeJ.Fade(0)
        self.redLifeJ.Fade(0)
        self.whiteLifeM.Fade(0)
        self.redLifeM.Fade(0)

    def showCombat(self):
        self.isInCombat = True
        self.BattleDialog.Fade(1)
        self.bgBattleDialog.Fade(1)
        self.heart.Fade(1)
        self.heartHurted.Fade(0)
        self.whiteLifeJ.Fade(1)
        self.redLifeJ.Fade(1)
        self.whiteLifeM.Fade(1)
        self.redLifeM.Fade(1)
        self.MoveHeart(0,205)
        
    def lose(self):
        self.wait(2000)
        if self.Pv <= 0:
            self.hideCombat()  
            self.RemoveCharacter("Face")
            glob.AudioManager.Stop()
            self.gameOver()
        
    def MoveHeart(self, x, y):
        width = self.heart.srcImg.get_width()
        height = self.heart.srcImg.get_height()
        x = numpy.clip(x, -200 + width*0.1, 200 - width*0.1)
        y = numpy.clip(y, 10 + height*0.1, 410 - height*0.1)
        self.heart.position = vector2(x, y)
        self.heartHurted.position = vector2(x, y)
        
    def healing (self,quantity):
        self.Pv+=quantity
        self.Pv=min(self.MaxPv, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.Pv/self.MaxPv)*200,30))

    def Take_dommage(self,quantity):
        glob.AudioManager.PlaySound("PUNCH 2.mp3")
        self.Pv-=quantity
        self.Pv = max(0, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.Pv/self.MaxPv)*200,30))
        if self.Pv <= 0:
            self.hideCombat()
            # self.gameOver()
            return False
        return True

    def Take_dommage_M(self,quantity):
        glob.AudioManager.PlaySound("DMG.mp3")
        self.PvM-=quantity
        self.PvM = max(0, self.PvM)
        self.redLifeM.VectorScale(vector2((self.PvM/self.MaxPvM)*200,30))
        if self.PvM <= 0:
            self.hideCombat()
            return False
        return True

    def Change_isAwaiting(self):
        self.isAwaiting=False

    def Wait_Button(self):
        self.isAwaiting=True
        self.AttackButton.onClick(self.Change_isAwaiting)
        while self.isAwaiting :
            self.wait(10)

    def getHurt(self):
        if self.canTakeDamage:
            glob.Scheduler.AddNow(lambda: self._getHurt(), killable=False)

    def _getHurt(self):
        self.bgBattleDialog.Color(Color(255,0,0))
        self.canTakeDamage = False
        d = self.Take_dommage(4)
        if d:
            self.heart.Fade(0)
            for _ in range(6):
                self.heartHurted.Fade(1)
                self.wait(100)
                self.heartHurted.Fade(0)
                self.wait(100)
            self.heart.Fade(1)
            self.canTakeDamage = True
            self.bgBattleDialog.Color(Color(255,255,255))

    # permet de sortir un personnage de l'??cran sans lui faire faire de demi-tour.
    def sortie(self,perso):
            self.Characters[perso].MoveTo(vector2(2000,0),2000)
            self.Characters[perso].MoveTo(vector2(2000,2000),200)
            self.Characters[perso].MoveTo(vector2(-2000,2000),200)
            self.Characters[perso].MoveTo(vector2(-2000,0),200)
            
        
    def sortie_anne(self):
        self.Characters["Anne"].setChar("man 2.png")
        self.Characters["Anne"].MoveTo(vector2(2000,300),1000)
        self.Characters["Anne"].setChar("man 1.png")

    def wait(self, duration):
        time.sleep(duration/1000)

    def update(self):
        #Update, what's run each frame, prerequite in menu class
        if self.isInCombat:
            keys=pygame.key.get_pressed()
            y = self.heart.position.y
            x = self.heart.position.x
            if keys[K_UP]:
                y -= 5
            if keys[K_DOWN]:
                y += 5
            if keys[K_RIGHT]:
                x += 5
            if keys[K_LEFT]:
                x -= 5
            self.MoveHeart(x, y)
            t = []
            for sp in self.AttackSprites:
                if self.heart.isColliding(sp):
                    self.getHurt()
                    glob.foregroundSprites.remove(sp)
                    t.append(sp)
            for s in t:
                self.AttackSprites.remove(s)
                    

    def dispose(self):
        #ran before closure
        for s in glob.foregroundSprites.sprites:
            s.FadeTo(0, 400)
        pass


    def ShowMessage(self, nom, text):
        """Show Message, set title, and wait for player to input (blocking)

        Args:
            nom (string): terminal title
            text (string): the message itself
        """
        self.ShowInterface()
        self.Cls()
        self.Title.Text(nom)
        self.AddMessage(text)
        self.wait(500)
        self.waitForEnter()
        glob.AudioManager.PlaySound("advance.wav")
        self.HideInterface()

    def ShowInterface(self):
        """Show in game terminal
        """
        self.Dialog.Fade(1)
        self.bgDialog.Fade(1)
        self.Title.Fade(1)
        self.DialogTitle.Fade(1)
        self.bgDialogTitle.Fade(1)

    def HideInterface(self):
        """Hide in game terminal
        """
        self.Cls()
        self.Dialog.Fade(0)
        self.bgDialog.Fade(0)
        self.Title.Fade(0)
        self.DialogTitle.Fade(0)
        self.bgDialogTitle.Fade(0)

    def go(self):
        self.SwitchBackground("GO.jpg", 2000)
        self.wait(2000)
        # self.GifSprite()
        # self.ShowCharacter("haato",["happy.png","angry.png","reflexion 1.png","reflexion 2.png","reflexion 3.png","reflexion 4.png","reflexion 5.png","reflexion 6.png","sad.png"],scale=1.4)
        # self.Characters["haato"].Move(vector2(0,400))
        # self.wait(500)
        
        # self.Characters["haato"].setChar("reflexion 2.png")
        # self.wait(500)
        # self.Characters["haato"].setChar("reflexion 3.png")
        # self.wait(500)
        # self.Characters["haato"].setChar("reflexion 4.png")
        # self.wait(500)
        # self.Characters["haato"].setChar("reflexion 5.png")
        # self.wait(437)
        # self.Characters["haato"].setChar("reflexion 6.png")
        # self.wait(148)
        # self.Characters["haato"].setChar("reflexion 5.png")
        # self.wait(148)
        # self.Characters["haato"].setChar("reflexion 6.png")
        
        # self.Characters["haato"].VertFlip()
        # self.wait(500)
        # self.Characters["haato"].VertFlip()
        # self.wait(500)
        # self.Characters["haato"].VertFlip()
        # self.wait(2000)
        # self.RemoveCharacter("haato")
        
        glob.MenuManager.ChangeMenu(Menus.MainMenu)
        

    def gameOver(self):
        self.isAwaiting= True 
        self.ShowMessage("Narrateur","franchement bravo")
        self.go()

        
        
    def Cls(self):
        """Clear in game terminal
        """
        for txt in self.Messages:
            glob.foregroundSprites.remove(txt)
        self.Messages = []
        if self.AcceptInput:
            self.AddMessage(">")

    def AddMessage(self, string, color=Color(255,255,255)):
        """Add a message to the in game terminal

        Args:
            string (string): the string to show
            color (Color, optional): Color of the line. Defaults to Color(255,255,255).
        """
        strLim = 50
        if self.AcceptInput and len(self.Messages) != 0:
            return
        if len(string) > strLim:
            self.AddMessage(string[:strLim], color)
            self.AddMessage(string[strLim:], color)
            return
        text = pText(string, 40, FontStyle.thin, vector2(-740, -50), Positions.bottomCentre, Positions.bottomLeft, color)
        if len(self.Messages) >= 9:
            txt = self.Messages.pop(0)
            glob.foregroundSprites.remove(txt)
        for txt in self.Messages:
            txt.position.y -= 40
        self.Messages.append(text)
        text.Depth = -2
        glob.foregroundSprites.add(text)

    def waitForEnter(self):
        """Wait for the player to input Z or Enter (Blocking)
        """
        self.isAwaiting = True
        self.AwaitSymbol.Fade(1)
        while self.isAwaiting:
            self.wait(10)
        self.AwaitSymbol.Fade(0)
        return

    def HandleEvents(self, events):
        #Handle events (prerequite in menu)
        for e in events:
            if e.type is pygame.QUIT:
                glob.Running = False
            if self.isAwaiting:
                if e.type == KEYDOWN:
                    if self.AcceptInput:
                        self.InputCharacter(e)
                    elif e.key == K_RETURN or e.key == K_KP_ENTER or e.key == K_z:
                        self.isAwaiting = False
                if e.type == pygame.MOUSEBUTTONDOWN and not self.AcceptInput:
                    if e.button in (1, 2, 3):
                        self.isAwaiting = False

    def InputCharacter(self, e):
        """Handle input character (Do not call elsewhere than handle)

        Args:
            e (pygame Event): the event
        """
        keyinput = pygame.key.get_pressed()
        keyPress = e.key
        if keyPress == K_BACKSPACE and len(self.cmd) > 0:
            glob.AudioManager.PlaySound("keyDelete.mp3")
            res = self.cmd[0:-1]
            self.cmd = res
            self.Messages[-1].Text("> "+self.cmd)
        elif keyPress == K_RETURN and len(self.cmd) > 0:
            self.isAwaiting = False
            self.AcceptInput = False
        elif keyPress >= 32 and keyPress <= 126:
            # If the user presses the shift key while pressing another character then capitalise it
            if keyinput[K_LSHIFT]:
                keyPress -= 32
            self.cmd += chr(keyPress)
            self.Messages[-1].Text("> "+self.cmd)
            i = randint(1, 4)
            glob.AudioManager.PlaySound(f"keyTick{i}.mp3")

    def getInput(self, text):
        self.ShowInterface()
        self.UnlockInput(text)
        while self.isAwaiting and self.AcceptInput:
            self.wait(50)
        d = self.cmd
        self.cmd = ""
        self.HideInterface()
        return d

    # permet de sortir un personnage de l'??cran sans faire de demi-tour.
    def sortie(self,perso):
        self.Characters[perso].MoveTo(vector2(2000,0),2000)
        self.Characters[perso].MoveTo(vector2(2000,2000),200)
        self.Characters[perso].MoveTo(vector2(-2000,2000),200)
        self.Characters[perso].MoveTo(vector2(-2000,0),200)
        

    def UnlockInput(self, text):
        """Allow inputs from the player to the in game terminal

        Args:
            text (string): label text to show
        """
        self.Title.Text("input")
        self.Cls()
        self.AddMessage(text)
        self.AddMessage(">")
        self.AcceptInput = True
        self.isAwaiting = True

    def ShowCharacter(self, name, emots, combat=False, scale=1):
        """Create a character sprite on the field

        Args:
            name (string): Character folder name
            emots (string list): Emotes list to load
            combat (bool, optional): Show in combat interface instead of VN style. Defaults to False.
            scale (float, optional): scale of the sprite, to fits size. Defaults to 1.
        """
        sprite=CharacterSprite(name, charPos.Center,emots)
        for s in sprite.sprites.values():
            s.Depth = 3
            s.Scale(scale)
            if combat:
                s.field = Positions.centre
                s.origin = Positions.bottomCentre
        self.Characters[name] = sprite
        glob.foregroundSprites.add(sprite)

    def RemoveCharacter(self, key):
        """Remove character from the field

        Args:
            key (string): Character folder name
        """
        sprite = self.Characters[key]
        glob.foregroundSprites.remove(sprite)
        del self.Characters[key]

    def Script(self):
        """
        Main script, run on another thread to avoid blocking
        """
        debug = False
        
        

        if debug:
            self.hideCombat()
            self.SwitchBackground("bg_bar.png",500)
            glob.AudioManager.PlayMusic("tavern.mp3")
            self.ShowCharacter("haato",["happy.png","angry.png","reflexion 1.png","reflexion 2.png","reflexion 3.png","reflexion 4.png","reflexion 5.png","reflexion 6.png","sad.png"],scale=1.4)
            self.Characters["haato"].MoveTo(vector2(-300,400),50)
            self.wait(2000)
            self.ShowMessage("Narrateur", "Pu***n encore")
            self.ShowMessage("Chara Melmou","Caramel mou?")
            self.ShowMessage("Narrateur","...")
            self.ShowMessage("Narrateur","Ooooook attendez")
            glob.AudioManager.PlaySound("clic_souri.mp3")
            glob.AudioManager.PlaySound("clic_souri.mp3")
            glob.AudioManager.PlaySound("machine_effect.mp3")
            self.wait(4200)
            glob.AudioManager.PlaySound("clic_souri.mp3")
            self.wait(1000)
            self.ShowMessage("Narrateur","C'est bon on recommence")
            self.ShowMessage("Chare Melmou","Je suis Chara Melmou ")
            self.ShowMessage("Narrateur","C'est bon on peut commencer")
            self.ShowMessage("Narrateur","Vous ??tes Chara Melmou. Vous ??tes dans une auberge, apr??s avoir bien manger vous d??cidez d'aller acheter du r??glisse")
            self.ShowMessage("Chara Melmou","R??????????????gliiiiiiise")
            self.ShowMessage("Narrateur","Tais-toi j'introduis le sc??nario!!!!!!!!!!!")
            self.ShowMessage("Narrateur","Vous parter donc acheter dans une boutique")
            glob.AudioManager.Stop()
            glob.AudioManager.PlayMusic("DSI.mp3")
            self.SwitchBackground("bg_boutique_inside.jpg",4500)
            glob.AudioManager.PlaySound("bruit_de_pas.mp3")
            self.Characters["haato"].MoveTo(vector2(-600,400),4500)
            self.wait(5500)
            self.Characters["haato"].VertFlip()
            self.ShowCharacter("roberu",["roberu.png", "roberu_happy.png", "roberu_bad.png"],scale=0.6)
            self.Characters["roberu"].Move(vector2(600,0))
            self.ShowMessage("Roberu","Boujour, je peux vous aider ? ")
            self.ShowMessage("Narrateur","Vous demander de la reglisse")
            self.Characters["roberu"].setChar("roberu_bad.png")
            self.ShowMessage("Roberu","D??sol?? on nous a tout vol??!!")
            glob.AudioManager.PlaySound("nani.mp3")
            self.ShowMessage("Chara Melmou","!!!!!")
            self.wait(500)
            self.Characters["roberu"].setChar("roberu_happy.png")
            self.ShowMessage("Roberu","Mais si vous voulez j'ai du caramel mou !")
            self.ShowMessage("Narrateur","Vous demanddez qui a voler la reglisse")
            self.ShowMessage("Roberu","Je sais pas mais cette idiot et partie dans la f??ret")
            self.ShowMessage("Narrateur","Voulez-vous continuer ? (o/n)")
            conteneur=self.getInput("Choissiez-vous de continuer?")
            while conteneur.lower()!="o":
                self.ShowMessage("Narrateur","aucun probleme tu sais je peut parler des ann??e")
                self.ShowMessage("Narrateur","Voulez-vous continuer ? (o/n)")
                conteneur=self.getInput("Choissiez-vous de continuer?")
            self.Characters["roberu"].setChar("roberu_bad.png")
            self.ShowMessage("Roberu","vous allez vraiment y aller")
            self.ShowMessage("Roberu","hmmmmmmm tenez")
            self.ShowMessage("Narrateur","Vous recevez des potion")
            self.ShowMessage("Narrateur","srx le jeu en mode facile ou quoi")
            glob.AudioManager.Stop()
            self.ShowMessage("Narrateur","Vous partez en direction de la foret")
            
                

        if debug:   
            return
        #Intro (Name selection)
        self.AttackButton.Fade(0)
        self.hideCombat()
        self.ShowMessage("Narrateur", "Bonjour testeur, bienvenue dans \"LE REGLISSE DE LA V??RIT??\".")
        self.ShowMessage("Narrateur","Quel est votre nom ?")
        self.getInput("Entrez votre nom")
        test = self.getInput("Etes vous sur de choisir ce noms ? (o/n)")
        if test.lower() =="n":
            self.getInput("Tr??s bien quel et votre nom ?")
            self.getInput("Tr??s bien ??tes vous sur ? (o/n)")
        self.ShowMessage("Narrateur", "Chara Melmou... c'est pas ouf comme nom, mais bon, on ne choisit pas nos parents")
        self.ShowCharacter("flowey", ["idle.png", "sad.png", "smug.png"], True)
        glob.AudioManager.PlayMusic("flowey.mp3")
        self.ShowMessage("Flowey", "Salut !")
        self.ShowMessage("Flowey", "Je suis Flowey !")
        self.Characters["flowey"].setChar("smug.png")
        self.ShowMessage("Flowey", "Flowey la fleur !")
        self.Characters["flowey"].setChar("idle.png")
        self.ShowMessage("Flowey", "Je vais t'apprendre comment on joue ?? ce jeu")
        self.ShowMessage("Flowey", "Utilise les fl??ches directionnel de ton clavier pour esquiver mais attaque")
        self.ShowMessage("Flowey", "la barre rouge qui apparaitra a ta gauche represente tes point de vie (PV)")
        self.ShowMessage("Flowey", "la bleu qui sera a ta droite represente des point de vie du monstre adverse(PVM)")
        self.ShowMessage("Flowey", "Esquive les attaques du mieux que tu peux !")
        
        self.ShowMessage("Flowey", "ATENTION, droite !!")


        # premier combat
        self.ShowMessage("Flowey", "ATENTION, droite !!")
        self.showCombat()
        self.wait(500)
        
        Attacks.Attack_basic_1(self.AttackSprites)
        self.hideCombat()

        self.ShowMessage("Flowey", "ATENTION, gauche !!")
        self.showCombat()
        self.wait(500)
        
        Attacks.Attack_basic_2(self.AttackSprites)
        self.hideCombat()

        self.ShowMessage("Flowey", "Pr??pare toi !")
        self.showCombat()
        self.wait(500)
        
        Attacks.attack_m2(self.AttackSprites)

        self.wait(8000)
        self.hideCombat()
        self.ShowMessage("Flowey", "A toi de m'attaquer")
        
        self.showCombat()
        
        self.AttackButton.Fade(1)
        self.Text.Fade(1)
        self.Wait_Button()
        self.AttackButton.Fade(0)
        self.Text.Fade(0)

        self.ShowMessage("Flowey", "Assez jouer !!")
        Attacks.attack_cercle(self.AttackSprites)
        
        self.hideCombat()
        self.RemoveCharacter("flowey")
        self.ShowMessage("Narrateur", "STOOOP")
        self.ShowMessage("Narrateur", "VOUS ETES SERIEUX, IL Y A DES LIMITE A LA REFERENCE!!!!!!!!!!!")
        self.ShowMessage("Narrateur", "C'est bon tu prends tes clics et tes clacs,et tu sors de l??!!!!")
        
        #  fin de l'intro et du tutoriel
        
        self.SwitchBackground("bg_bar.png",500)
        glob.AudioManager.PlayMusic("tavern.mp3")
        self.ShowCharacter("haato",["happy.png","angry.png","reflexion 1.png","reflexion 2.png","reflexion 3.png","reflexion 4.png","reflexion 5.png","reflexion 6.png","sad.png"],scale=1.4)
        self.Characters["haato"].MoveTo(vector2(600,400))
        self.wait(2000)
        
        self.ShowMessage("Narrateur", "Pu***n encore")
        self.Characters["haato"].setChar("reflexion 1.png")
        self.ShowMessage("Chara Melmou","Caramel mou?")
        self.ShowMessage("Narrateur","...")
        self.ShowMessage("Narrateur","Ooooook attendez")
        
        glob.AudioManager.PlaySound("clic_souri.mp3")
        self.Characters["haato"].setChar("reflexion 4.png")
        glob.AudioManager.PlaySound("clic_souri.mp3")
        glob.AudioManager.PlaySound("machine_effect.mp3")
        
        self.wait(4200)
        glob.AudioManager.PlaySound("clic_souri.mp3")
        self.wait(1000)
        
        self.ShowMessage("Narrateur","C'est bon on recommence")
        self.ShowMessage("Chare Melmou","Je suis Chara Melmou ")
        self.ShowMessage("Narrateur","C'est bon on peut commencer")
        self.Characters["haato"].setChar("happy.png")
        self.ShowMessage("Narrateur","Vous ??tes Chara Melmou. Vous ??tes dans une auberge, apr??s avoir bien manger vous d??cidez d'aller acheter du r??glisse")
        self.ShowMessage("Chara Melmou","R??????????????gliiiiiiise")
        self.ShowMessage("Narrateur","Tais-toi j'introduis le sc??nario!!!!!!!!!!!")
        self.ShowMessage("Narrateur","Vous parter donc en acheter dans une boutique")
        glob.AudioManager.Stop()
        glob.AudioManager.PlayMusic("DSI.mp3")
        self.SwitchBackground("bg_boutique_inside.jpg",4500)
        
        glob.AudioManager.PlaySound("bruit_de_pas.mp3")
        
        self.Characters["haato"].MoveTo(vector2(-600,400),5500)
        self.wait(5500)
        self.Characters["haato"].VertFlip()
        
        self.ShowCharacter("roberu",["roberu.png", "roberu_happy.png", "roberu_bad.png"],scale=0.6)
        self.Characters["roberu"].Move(vector2(600,0))
        self.ShowMessage("Roberu","Boujour je peux vous aider ? ")
        self.ShowMessage("Narrateur","(Vous demandez du reglisse)")
        self.Characters["roberu"].Move(vector2(600,0))
        self.Characters["roberu"].setChar("roberu_bad.png")
        self.Characters["roberu"].Move(vector2(600,0))
        self.ShowMessage("Roberu","D??sol?? on nous a tous vol??!!")
        self.Characters["haato"].setChar("reflexion 1.png")
        glob.AudioManager.PlaySound("nani.mp3")
        self.ShowMessage("Chara Melmou","!!!!!")
        self.Characters["roberu"].setChar("roberu_happy.png")
        self.ShowMessage("Roberu","Mais si vous vouler j'ai du caramel mou")
        self.ShowMessage("Narrateur","Vous demandez qui a vol?? la reglisse")
        self.ShowMessage("Roberu","Je sais pas mais cet idiot est partie dans la f??ret")
        self.ShowMessage("Roberu","Je l'ignore mais, Il est partie en direction d'un donjon")
        self.Characters["haato"].setChar("happy.png")
        self.ShowMessage("Narrateur","Voulez-vous continuer ? (o/n)")
        conteneur=self.getInput("Choissiez-vous de continuer?")
        while conteneur.lower()!="o":
            self.ShowMessage("Narrateur","aucun probleme tu sais je peut parler des ann??es")
            self.ShowMessage("Narrateur","Voulez-vous continuer ? (o/n)")
            conteneur=self.getInput("Choissiez-vous de continuer?")            

        self.ShowMessage("Narrateur","Vous partez en direction de la foret")
        
        self.Characters["roberu"].setChar("roberu_bad.png")
        self.ShowMessage("Roberu","vous allez vraiment y aller ?")
        self.ShowMessage("Roberu","Hmmmmmmm...")
        self.ShowMessage("Roberu","Tenez")
        self.ShowMessage("Narrateur","(Vous recevez des potion)")
        self.ShowMessage("Narrateur","serieux le jeu est en mode facile ?") 
        self.ShowMessage("Narrateur","(Vous partez en direction de la foret)")
        glob.AudioManager.Stop()
        self.RemoveCharacter("haato")
        self.RemoveCharacter("roberu")

        self.SwitchBackground("japan.jpg",100)
        glob.AudioManager.PlayMusic("MexicanMusic.mp3")
        self.ShowCharacter("haato",["happy.png","angry.png","reflexion 1.png","reflexion 2.png","reflexion 3.png","reflexion 4.png","reflexion 5.png","reflexion 6.png","angry.png","sad.png"],scale=1.4)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")  
        self.Characters["haato"].MoveTo(vector2(10000,400),1000)
        self.ShowMessage("Narrateur","DE L'AUTRE COT?? !!!")
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(-10000,400),1000)
        self.wait(3500)
        
        self.SwitchBackground("New_York.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(10000,400),1000)
        self.wait(2500)
        
        self.SwitchBackground("egypt.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(-10000,400),1000)
        self.wait(2500)
        
        self.SwitchBackground("bear.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(10000,400),1000)
        self.wait(2500)
        glob.AudioManager.Stop()

        self.SwitchBackground("forest 2.png",100)
        glob.AudioManager.PlayMusic("Forest.mp3")
        self.wait(2000)
        
        self.ShowMessage("Narrateur","STOP!!!")
        self.ShowMessage("Chara Melmou","?!!")
        glob.AudioManager.PlaySound("Crissement de pneus 1.mp3")
        self.Characters["haato"].MoveTo(vector2(0,400),1000)       
        glob.AudioManager.Stop()
        self.wait(2000)
        
        glob.AudioManager.PlayMusic("DIO.mp3")
        
        self.ShowMessage("???","*Bruit de pas*")
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].VertFlip() 
        self.wait(1000)
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].MoveTo(vector2(-600,400),1000)
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Qui... est L?? !?")  
        self.SwitchBackground("forest 1.jpg",4500)
        self.wait(4500)
        self.ShowCharacter("Anne",["man 1.png", "man 2.png", "ane.png"],scale=2)
        self.Characters["Anne"].MoveTo(vector2(600,300),1000)
        self.ShowMessage("???","Je suis personnage secondaire et mon but est de faire avancer le sc??nario")
        self.ShowMessage("personnage secondaire"," Je peux t'aider ?? obtenir ce que tu cherche. Tu peux me fare confiance, suis moi !")
        self.ShowMessage("Narrateur","Chara Melmou ne pouvais LOGIQUEMENT pas lui faire confiance")
        
        self.wait(1000)
        
        self.ShowMessage("Chara Melmou","Hhhmmmm...")
        
        glob.AudioManager.PlaySound("reflexion.mp3")
        
        self.wait(874)
        self.Characters["haato"].setChar("reflexion 2.png")
        self.wait(3550)
        self.Characters["haato"].setChar("reflexion 3.png")
        self.wait(624)
        self.Characters["haato"].setChar("reflexion 4.png")
        self.wait(791)
        self.Characters["haato"].setChar("reflexion 5.png")
        self.wait(437)
        self.Characters["haato"].setChar("reflexion 6.png")
        self.wait(148)
        self.Characters["haato"].setChar("reflexion 5.png")
        self.wait(376)
        self.Characters["haato"].setChar("angry.png")
        
        
        self.wait(2000)
        
        self.ShowMessage("personnage secondaire"," Je te propose de faire un march??, tu ??limine quelqu'un pour moi et en ??change je te donnerais de quoi t'aider ?? obtennir le r??glisse que tu convoite")
        self.wait(2000)
        
        glob.AudioManager.Stop()
        glob.AudioManager.PlayMusic("Forest.mp3")
        
        # nouvel alli?? 
        
        self.Characters["haato"].setChar("happy.png")
        self.ShowMessage("Chara Melmou","OK !")
        self.ShowMessage("Narrateur","Quel abruti...")
        self.ShowMessage("personajsegond??r"," ravi de l'entendre, en passant tu peux m'appeler Anne, c'est comme cela que les amis que je n'ai pas m'appellent !")
        self.ShowMessage("Anne","Bon pour commencer la personne que tu cherche se trouve *au sommet de la montagne*, mais pour y acc??der tu devras passer dans son donjon")
        self.ShowMessage("Anne","le donjon est interminable, et de ce fait je vais de donner un raccourci")
        self.ShowMessage("Anne","tu aurras 2 ennemis ?? battre dont...")
        
        self.wait(2000)
        
        self.ShowMessage("Narrateur","r??veille TOI !!!")
        
        self.wait(500)
        
        glob.AudioManager.PlaySound("gifle.mp3")
        
        self.wait(1000)
        
        self.ShowMessage("Chara Melmou","A??e !!")
        self.ShowMessage("Chara Melmou","pourquoi tu m'a frapp?? !!? je ne dormais pas c'est mes yeux qui sont comme ??a")
        self.ShowMessage("Narrateur","oui. je sais.")
        self.ShowMessage("Chara Melmou","?..")
        self.ShowMessage("Anne","Bon je t'expliquerais en chemain allons-y")
        self.sortie("haato")
        self.sortie_anne()
        
        # glob.AudioManager.Stop()
        
        self.ShowMessage("Narrateur","(rigole) Chara Melmou et Anne arriv??rent devans la porte du donjon")
        
        self.SwitchBackground("dungeon.jpg",4500)
        
        self.wait(4500)
        
        
        self.Characters["haato"].MoveTo(vector2(-600,400),2000)
        self.ShowMessage("Anne","Je t'ai tout dit maintenant tu est pr??t.")
        # "explication de l'inventaire + potions
        self.wait(2000)
        
        self.ShowMessage("Chara Melmou","Allons y !!")
        self.sortie("haato")
        
        self.SwitchBackground("1h.jpg",100)
        glob.AudioManager.PlaySound("1h.mp3")
        self.wait(4000)
        
        
        # ""COMBAT 1 
        
        
        self.SwitchBackground("room 1.jpg",2000)
        self.wait(2000)
        self.Characters["haato"].MoveTo(vector2(-600,400),2000)
        self.ShowMessage("Chara Melmou","je suis fatigu?? on peut faire une pose ?")
        self.Characters["Anne"].MoveTo(vector2(600,300),1000)
        self.ShowMessage("Anne","NON.")
        self.ShowMessage("Narrateur","Dans tes r??ves.")
        self.sortie_anne()
        self.ShowMessage("Narrateur","vous rencontrez un ennemie")
        self.ShowMessage("Narrateur","j'esp??re que tu vas y passer..")
        self.wait(4500)
        
        self.ShowCharacter("Mr dragon",["dragon_1.png", "dragon_2.png", "dragon_3.png","walter.png"],scale=0.5)
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),200)
        self.wait(1500)
        self.Characters["Mr dragon"].setChar("dragon_2.png")
        
        self.ShowMessage("???","Vous n'avez rien ?? faire ici, partez !!! ou vous p??rirez..")
        self.ShowMessage("Chara Melmou","Vous vous appelez comment ?")
        self.ShowMessage("???","pour toi humain ce sera Mr dragon")
        self.ShowMessage("Mr dragon","vous ??tes ici pour nous nuire ?? moi et mon ma??tre ?!")
        self.ShowMessage("Chara Melmou","NON ! pas du t..")
        self.ShowMessage("Narrateur","Si. exactemet")
        self.Characters["Mr dragon"].setChar("dragon_3.png")
        self.ShowMessage("Mr dragon","vous ne me laissez plus le choix!")
        self.Characters["haato"].MoveTo(vector2(-2000,400),1000)
        self.Characters["Mr dragon"].MoveTo(vector2(2000,0),1000)
        self.RemoveCharacter("Mr dragon")
        
        """ Les pv du joeur seront augment?? en fonction de la difficult?? de l'ennemi, pour facilit?? le test. """
        
        self.showCombat()
        
        self.healing(90)
        self.Pv= 40
        self.MaxPv= 40
        self.PvM=30
        self.MaxPvM=30

        
        glob.AudioManager.PlayMusic("DIO.mp3")
        
        self.ShowCharacter("Face", ["Dface.png"], True)
        
        while self.PvM > 0 or self.Pv > 0:
            self.wait(500)

            self.hideCombat()
            
            self.lose()
                
            self.ShowMessage("Mr dragon","ne r??siste pas, HUMAIN !!")
            self.showCombat()
            self.wait(500)
            
            Attacks.Attack_basic_2(self.AttackSprites)
            
            self.lose()
        
            Attacks.attack_retour(self.AttackSprites)
            self.wait(500)
            
            self.lose()
            
            Attacks.attack_m2_horizontal(self.AttackSprites)
            self.wait(5000)
                
            self.hideCombat()  
            
            self.lose()
                
            self.ShowMessage("Narrateur","A ton tour.")
            self.ShowMessage("Mr dragon","Tu manques de FORCE !!")  
            self.showCombat()
            self.wait(500)
            
            self.AttackButton.Fade(1)
            self.Text.Fade(1)
            self.Wait_Button()
            self.AttackButton.Fade(0)
            self.Text.Fade(0)
            
            if self.PvM <= 0:
                break
            
            self.hideCombat()
            self.ShowMessage("Mr dragon","A mon tour.")
            self.showCombat()
            self.wait(500)
            
            Attacks.Attack_basic_2(self.AttackSprites)
            
            self.lose()
            
            Attacks.attack_m2_verical(self.AttackSprites)
            
            self.lose()
            
            Attacks.Attack_basic_2(self.AttackSprites)
        
        self.RemoveCharacter("Face")
        
        self.AttackButton.Fade(0)
        
        self.hideCombat()
        
        # victoire du combat, + nouveau compagnon
        
        
        self.Characters["haato"].MoveTo(vector2(-600,400),1000)
        self.ShowCharacter("Mr dragon",["walter.png"],scale=0.8)
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),1000)
        self.ShowMessage("Narrateur","c'est quoi ce bordel pourquoi les ennemies sont si nul..")
        self.Characters["Mr dragon"].setChar("walter.png")
        self.ShowMessage("Mr dragon","Je vous remercie de m'avoir d??livrer du sort que l'on m'a jet??, pour me racheter je vous accompagne dans votre qu??te")
        self.ShowMessage("Walter","Je m'appelle Walter je t'aiderais ?? accomplir ton but")
        self.Characters["Mr dragon"].MoveTo(vector2(2000,0),1000)
        self.ShowMessage("Chara Melmou","Victoire !!")
        self.ShowMessage("Anne","je savais que tu en serais capable.")
        self.ShowMessage("Anne","Maintenant, avan??ons !")
        self.Characters["Anne"].MoveTo(vector2(2000,300),1000)
        self.Characters["haato"].MoveTo(vector2(-2000,400),1000)
        self.Characters["Mr dragon"].MoveTo(vector2(2000,0),1000)
        self.wait(4500)
        
        # COMBAT 2
        
        self.SwitchBackground("eternity.jpg",100)
        glob.AudioManager.PlaySound("eternity.mp3")
        self.wait(4000)
        glob.AudioManager.Stop()
        
        self.SwitchBackground("room 2.jpg",4000)
        self.wait(4000)
        
        self.Characters["haato"].MoveTo(vector2(-600,400),2000)
        
        self.ShowMessage("Narrateur","vous rencontrez un ennemie")
        self.ShowCharacter("shrek",["shrek 1.png", "shrek 2.png", "shrek 3.png"],scale=1)
        
        self.Characters["shrek"].MoveTo(vector2(600,700),1000)
        self.ShowMessage("???","l'ane qu'est ce que tu fais i??i !?")
        self.Characters["shrek"].MoveTo(vector2(2000,700),1000)
        
        self.Characters["Anne"].MoveTo(vector2(600,300),1000) 
        self.ShowMessage("Anne","Voici la personne que je voulais que tu ??limine, fais attention il est dangereux !!")
        self.Characters["Anne"].MoveTo(vector2(2000,300),1000)
       
        self.Characters["shrek"].MoveTo(vector2(600,700),1000)
        self.Characters["shrek"].setChar("shrek 2.png")
        self.ShowMessage("???","l'aaaane...? c'est de moi que tu parles !?")
        self.Characters["shrek"].MoveTo(vector2(2000,500),1000)
        
        
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),1000)
        self.ShowMessage("Walter","Evitez de l'??nerver !!")
        self.Characters["Mr dragon"].MoveTo(vector2(2000,0),1000)
        
        self.Characters["Anne"].MoveTo(vector2(600,300),1000)
        self.ShowMessage("Anne","NON. je parle ?? une pomme")
        self.Characters["Anne"].MoveTo(vector2(2000,300),1000)
        
        self.Characters["shrek"].MoveTo(vector2(600,700),1000)
        
        
        self.wait(2000)
        self.Characters["shrek"].setChar("shrek 3.png")
        self.ShowMessage("shrek","je ne laisserais  AUCUN d'entre vous sortir d'ici vivant!!!")
        self.Characters["haato"].MoveTo(vector2(-2000,400),1000)
        self.Characters["shrek"].MoveTo(vector2(2000,500),1000)
        
        # phase combat
        
        self.showCombat()
        
        glob.AudioManager.PlayMusic("koopas.mp3")
        
        self.ShowCharacter("Face", ["Sface.png"], True,scale=0.6)
    
        self.PvM = 10
        self.MaxPvM= 10
        self.Pv = 40
        self.MaxPv= 40
        
        while self.PvM > 0:
            self.wait(500)

            self.hideCombat()
            self.ShowMessage("shrek","AhAhahahah !!")
            self.showCombat()
            self.wait(500)
            
            Attacks.Attack_basic_2(self.AttackSprites)
            self.lose()
            
            Attacks.attack_retour(self.AttackSprites)
            self.lose()
            
            self.wait(500)
            
            Attacks.attack_m2_horizontal(self.AttackSprites)
            self.lose()
            
            self.wait(5000)
            
            self.hideCombat()
                
            self.ShowMessage("Narrateur","A ton tour.")
            self.ShowMessage("shrek","Abandonne !!")  
            
            self.showCombat()
            
            self.wait(500)
            
            self.AttackButton.Fade(1)
            self.Text.Fade(1)
            self.Wait_Button()
            
            if self.PvM <= 0:
                break
            
            self.AttackButton.Fade(0)
            self.Text.Fade(0)

            self.hideCombat()
            self.ShowMessage("shrek","Tu vas voir")
            self.showCombat()
            self.wait(500)
            
            Attacks.attack_m2_croix(self.AttackSprites)
            self.lose()
            
            Attacks.attack_m2_verical(self.AttackSprites)
            self.lose()
            
            Attacks.attack_m2_croix(self.AttackSprites)
            self.lose()
            
        self.RemoveCharacter("Face")
        
        glob.AudioManager.Stop()
        
        self.hideCombat()
        
        
        self.Characters["haato"].MoveTo(vector2(-600,400),2000)
        self.Characters["Anne"].MoveTo(vector2(600,400),2000)
        
        self.ShowMessage("Anne","Chara Melmou, je voulais te remercier de m'avoir permis de me venger, il a bouffer toute ma famille le fumier, sans toi rien n'aurais ??t?? possible.")
        self.ShowMessage("Chara Melmou","(ne l'??coute pas), il est o?? le r??glisse ?")
        self.ShowMessage("Anne","...")
        self.ShowMessage("Anne","sur ce Chara Melmou, je vais devoir m'en aller et merci encore")
        self.ShowMessage("Chara Melmou","Au revoir..")
        
        self.Characters["Anne"].MoveTo(vector2(2000,400),2000)
        self.Characters["haato"].MoveTo(vector2(-2000,400),2000)
        
        # Sortie du donjon
        
        self.wait(2000)
        
        self.SwitchBackground("dark forest.jpg",4500)
        self.ShowMessage("Narrateur","Chara Melmou et Walter sortent du donjon et retournent dans la for??t en qu??te du reglisse")
        self.wait(1000)
        
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),1000)
        self.ShowMessage("Walter","T'es vraiment s??r de vouloir continuer juste pour du reglisse l?? ??")
        self.Characters["haato"].MoveTo(vector2(-600,400),2500)
        
        self.ShowMessage("Chara Melmou","JUSTE de la reglisse ? Non.. Non... T??che d'??xecuter mes requetes sans discuter Walter")
        self.ShowMessage("Walter","Excusez moi Chara, suis moi!")
        self.ShowMessage("Walter","Si je me souviens bien c'est quelque part par la")
        
        self.Characters["Mr dragon"].MoveTo(vector2(6000,0),3500)
        self.ShowMessage("Chara Melmou","J'arrive!")
        self.Characters["haato"].MoveTo(vector2(6000,400),3500)
        self.wait(1500)


        # Aper??u du ch??teu

        self.SwitchBackground("chateau.png",4500)
        glob.AudioManager.PlayMusic("chateau.mp3")
        self.wait(1500)
        self.ShowMessage("Narrateur","Chara Melmou et Walter continuent leurs p??riple dans la for??t jusqu'a atteindre un mysterieux Chateau")
        self.wait(2500)
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),3500)
        self.wait(1500)
        self.ShowMessage("Walter","Ah enfin.. Voila le lieu dont je te parlais")
        self.Characters["haato"].MoveTo(vector2(-600,400),3500)
        self.wait(1500)
        self.ShowMessage("Chara Melmou","Super Walter ! Ce chateau empeste le reglisse, c'est evident que le voleur ce trouve ici")
        self.ShowMessage("Chara Melmou","Depechons-Nous!!")
        self.Characters["haato"].MoveTo(vector2(6000,400),3500)
        self.wait(1000)
        self.Characters["Mr dragon"].MoveTo(vector2(6000,0),3500)

        glob.AudioManager.Stop()
        
        # P??n??tration dans le ch??teau
        
        self.SwitchBackground("couloir.png",4500)
        glob.AudioManager.PlayMusic("couloir.mp3")
        self.wait(2500)

        self.Characters["Mr dragon"].MoveTo(vector2(600,0),1500)
        self.wait(1000)
        self.ShowMessage("Walter","Tu es au courant que ce n'est pas qu'un simple chateau ? Tu as surement plus a perdre qu'a gagner")
        self.Characters["haato"].MoveTo(vector2(-600,400),1500)
        self.ShowMessage("Walter","Sache que si on franchit cette porte il n'y aura plus aucun retour possible ")
        self.wait(1500)
        self.ShowMessage("Chara Melmou","Je donnerai ma vie pour ces reglisses.. FON??ONS")
        self.Characters["Mr dragon"].MoveTo(vector2(2000,500),1000)
        self.Characters["haato"].MoveTo(vector2(6000,400),3500)
        self.SwitchBackground("hall.png",4500)
        self.wait(1000)
        self.Characters["haato"].MoveTo(vector2(-600,400),1500)
        self.Characters["Mr dragon"].MoveTo(vector2(600,0),1500)
        self.wait(2000)
        glob.AudioManager.PlaySound("Mickeyhall.mp3")
        self.wait(4500)
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].VertFlip() 
        self.wait(1000)
        self.ShowMessage("Chara Melmou","c'etait quoi ??a ??")
        self.ShowMessage("Walter","MERDE.. euh je crois bien que c'est lui. Je vais devoir te laisser ciao")
        self.Characters["Mr dragon"].MoveTo(vector2(-6000,0),4500)
        self.wait(1000)
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Mais t'es serieux la?! c'est qui !! Reponds moi")
        self.wait(1000)
        self.Characters["haato"].VertFlip()
        self.wait(1500)
        self.ShowMessage("Chara Melmou","Bon.. Je crois que je vais devoir me debrouiller seul cette fois ci")
        self.ShowCharacter("mickey",["M1.png","M2.png"],scale=0.7)
        self.Characters["mickey"].setChar("M1.png")
        self.Characters["mickey"].MoveTo(vector2(600,0),2500)
        self.wait(1000)
        self.Characters["haato"].VertFlip() 
        self.wait(1000)
        self.ShowMessage("Chara Melmou","T'es qui toi ?")
        self.Characters["mickey"].setChar("M2.png")
        self.ShowMessage("Evil Mickey","alors c'est toi qui tue mes hommes et qui cherche a derober mes reglisses ?")
        self.ShowMessage("Evil Mickey","Laisse moi te montrer ce que ca fait de s'attaquer aux mauvaises personnes")
        glob.AudioManager.Stop()
        self.Characters["mickey"].MoveTo(vector2(6000,0),1500)
        self.Characters["haato"].MoveTo(vector2(-6000,400),1500)
        self.wait(2500)
        
       
        #COMBAT AVEC MICKEY
        self.showCombat()
        
        glob.AudioManager.PlayMusic("epic.mp3")
        
        self.ShowCharacter("Face", ["Mface.png"], True)
    
        self.MaxPvM = 50
        self.PvM = 50
        self.MaxPv = 30
        self.Pv = 30
        
        while self.PvM > 0:
            self.wait(3000)

            self.hideCombat()
            self.ShowMessage("Evil Mickey","C'est pas finit !!")
            self.showCombat()
            self.wait(500)
            
            Attacks.attack_m2_croix(self.AttackSprites)
            self.lose()
            
            Attacks.attack_retour(self.AttackSprites)
            self.lose()
            
            self.wait(500)
            
            Attacks.attack_m2_horizontal(self.AttackSprites)
            self.lose()
            
            Attacks.attack_retour(self.AttackSprites)
            self.lose()
            
            self.wait(5000)
            
            self.hideCombat()  
              
            self.ShowMessage("Narrateur","A ton tour.")
            self.ShowMessage("Evil Mickey","Tu ne fais pas le poids !!")  
            
            self.showCombat()
            
            self.wait(1000)
            
            self.AttackButton.Fade(1)
            self.Text.Fade(1)
            self.Wait_Button()
            
            if self.PvM <= 0:
                break
            
            self.AttackButton.Fade(0)
            self.Text.Fade(0)

            self.hideCombat()
            self.ShowMessage("shrek","Tu vas voir")
            self.showCombat()
            self.wait(5000)
            
            Attacks.attack_m2_croix(self.AttackSprites)
            self.lose()
            
            Attacks.attack_m2_verical(self.AttackSprites)
            self.lose()
            
            Attacks.attack_m2_croix(self.AttackSprites)
            self.lose()
            
        self.RemoveCharacter("Face")
        
        glob.AudioManager.Stop()
        
        self.hideCombat()
        
        glob.AudioManager.PlayMusic("couloir.mp3")
        self.Characters["haato"].MoveTo(vector2(-600,400),1500)
        self.wait(1500)
        self.ShowMessage("Chara Melmou","il etait coriace celui la")
        self.ShowMessage("Chara Melmou","Il est ou maintenant mon putin de reglisse ??")
        self.ShowMessage("Narrateur","Je crois que tu arrives trop tard..")
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].VertFlip() 
        self.wait(1000)
        self.ShowMessage("Chara Melmou","COMMENT CA ?! iLS SONT OU??")
        self.ShowMessage("Narrateur","hmm comment dire..")
        self.ShowMessage("Narrateur","Mickey a bouff?? tout les reglisses")
        self.ShowMessage("Chara Melmou","TU TE FOUS DE MOI ??")
        self.ShowMessage("Chara Melmou","J'ai fait tout ca pour rien???")
        self.ShowMessage("Narrateur","OOOOH CALME TOI !")
        self.ShowMessage("Narrateur","Il y a un moyen pour tu recupere ton precieux reglisse, mais ca ne restera pas sans consequence")
        self.Characters["haato"].MoveTo(vector2(-300,400),1500)
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Serieux?! Explique!")
        self.ShowMessage("Narrateur","Soit tu recupere le reglisse mais le monde sera totalement detruit")
        self.ShowMessage("Narrateur","Soit t'oublie cette histoire de reglisse et tu rentre chez toi sans faire chier le monde")
        self.Characters["haato"].MoveTo(vector2(-2000,400),1000)
        conteneur=self.getInput("Quel Choix voulez vous faire (1/2)")
        if conteneur.lower()=="1":
            
            #Choix1
            self.ShowMessage("Narrateur","Vous venez de choisir le choix 1: Destruction du monde")
            self.ShowMessage("Explosion","Lancement de l'explosion imminente!")
            self.ShowMessage("Chara Melmou","Quoi ?? Attend mais je vais y passer moi aussi!!")
            self.ShowMessage("Chara Melmou","STOOOOOP")
            #Les deux images et le son en dessous sont a ajout??s
            self.SwitchBackground("earth.png",1500)
            self.wait(2000)
            glob.AudioManager.PlaySound("explosion.mp3")
            self.SwitchBackground("earthexplode.png",1500)
            self.wait(2000)
            self.SwitchBackground("reglissespace.png",2500)
            self.Characters["haato"].MoveTo(vector2(0,400),2000)
            self.Characters["haato"].VertFlip()
            self.wait(1000)
            self.Characters["haato"].VertFlip() 
            self.wait(1000)

            self.ShowMessage("Chara Melmou","JE SUIS OU LA ?? C'est quoi ce bordel")
            self.wait(4500)
            self.Characters["haato"].MoveTo(vector2(4000,400),3000)
            self.wait(2500)
            self.ShowMessage("Narrateur","Bien jou?? Chara tu as finis par obtenir ce que tu convoit?? tant !")
            self.ShowMessage("Narrateur","Mais malheuresement pour elle cette offre avait un prix et mena le monde a sa perte..")
            self.ShowMessage("Narrateur","Et c'est ainsi que ce termina le recit de Chara Melmou. Le Reglisse de la v??rit??")
            self.wait(2000)
            self.SwitchBackground("end.png",1500)
            

        else:

            #Choix2
            self.ShowMessage("Narrateur","Vous venez de choisir le choix 2: Tout ca pour rien")
            self.SwitchBackground("Maison.jpg",1500)
            self.Characters["haato"].MoveTo(vector2(-400,400),1000)
            self.Characters["haato"].VertFlip()
            self.wait(1000)
            self.Characters["haato"].VertFlip() 
            self.wait(1000)
            self.ShowMessage("Chara Melmou","Mais je suis de retour chez moi la ??")
            self.ShowCharacter("mere",["mere.png"],scale=2.5)
            self.Characters["mere"].MoveTo(vector2(400,0),1)
            self.ShowMessage("Mere de Chara","MA FILLE !! Tu es enfin rentr??.. Mais tu etais ou pendant tout ce temps??")
            self.ShowMessage("Chara Melmou","Bonjour m??re, j'avais beaucoup plus important a faire que de rester ici")
            self.ShowMessage("Mere de Chara","QUOI ?! mais tu parles maintenant ???")
            self.Characters["haato"].MoveTo(vector2(-6000,400),1000)
            self.Characters["mere"].MoveTo(vector2(6000,400),1000)
            self.ShowMessage("Narrateur","La m??re de Chara retrouva sa fille mais malheuresement celle ci rentra bredouille.")
            self.ShowMessage("Narrateur","Et c'est ainsi que ce termina le recit de Chara Melmou. Le Reglisse de la v??rit??")
            self.wait(2000)
            self.SwitchBackground("end.png",1500)
            #Mere de chara choqu?? car de base chara s'exprime comme groot mais a fini par etre corrig?? pendant son aventure






    # EXEMPLE de ce ?? quoi l'inventaire devais ressembler, ?? cause d'un certains nombre de bugs il n'aura pas ??t?? affich??.

    """class PlayerSYSTEM:
    def __init__(self, force, defense, pv, inventaires):
      self.force = force
      self.defense = defense
      self.pv = pv
      self.inventaires = [[],
                         []]
      
    def ajouter(self, item):
      x = len(item)
      while x > 0:
          if item == "potion de soin":
            self.inventaires[0].append(objet[0])
            return "vous venez d'obtenir une {}".format(x),self.inventaires
            
          if item == "invincibilit??":
            self.inventaires[0].append(objet[1])
            return "vous venez d'obtenir une {}".format(x),self.inventaires

          elif item == "potion de d??fense":
            self.inventaires[1].append(objet[1])
            return "vous venez d'obtenir une {}".format(x),self.inventaires
            
          elif item == "potion myst??rieuse":
            self.inventaires[1].append(objet[2])
            return "vous venez d'obtenir une {}".format(x),self.inventaires

    def utiliser(self, consommable):
       f = len(consommable)
       while f > 0:
          if consommable == "potion de soin":
            self.pv = self.pv + 20
            self.liste_objet = self.inventaires[0].remove(objet[0])
            
          if consommable == "potion de d??fense":
            self.defense = self.defense + 20
            self.inventaires = self.inventaires[1].remove(objet[1])
            
          if consommable == "potion de soin":
            self.pv = self.pv + 20
            self.liste_objet = self.inventaires[0].remove(objet[0])
  
       print ("vous avez utiliser ",consommable)
  
       return player.inventaires

objet_stat = {
          0: {"type":"soin",
              "niveau":"1",
              "durabilit??":"instantan??",
              "description":"procure au joueur un nombre de PV proportionnel au niveau de la potion"},
          1: {"type":"invincibilit??",
              "niveau":"1",
              "durabilit??":"toute la phase combat",
              "description":"permet au joueur d'??tre invincible"},
          2: {"type":"d??fense",
              "niveau":"1",
              "durabilit??":"instantan??",
              "description":"permet au joueur d'optenir une protection supl??mentaire en de ses PV"},
          3: {"type":"poison",
              "niveau":"inconnue",
              "durabilit??":"inconnue",
              "description":"potion aux effet inconnue"}
}
objet = {
          0: {"nom": "potion de soin",
              "r??ference" : objet_stat[0]},
          1: {"nom": "cape d'invisibilit??",
              "r??ference" : objet_stat[1]},
          2: {"nom": "potion de d??fense",
              "r??ference" : objet_stat[2]},
          3: {"nom": "potion myst??rieuse",
              "r??ference" : objet_stat[3]},
}

inventaire_test = [[objet[0],objet[1]],[objet[2],objet[3]]]"""

        
        




