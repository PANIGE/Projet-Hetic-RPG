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


"""
plan:
    - Trouver un PUTAIN de synopsis
        - Evil God Mikey
        - Nom du joueur : Chara Melmou
        - Dieu Maléfique mickey vole du réglisse a Chara Melmou, donc karamelmou va lui botter son derrière
        
    -Tutoriel
        -Déplacement VN sauf en combat
"""

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
        self.redLifeM=pSprite(glob.PixelWhite,vector2(440,10),SkinSource.local,Positions.centre,Positions.topRight,Color(255,255,0))
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
        self.PvM = max(0, self.Pv)
        self.redLifeJ.VectorScale(vector2((self.PvM/self.MaxPvM)*200,30))
        if self.PvM<= 0:
            self.hideCombat()
            return False
        return True

    def wait_button(self):
        self.isAwaiting=True
       # self.AttackButton.OnClick(lambda: self.isAwaiting = False)
        while self.isAwaiting:
            self.wait(10)
        pass
        

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

    def gameOver(self):
        self.isAwaiting= True 
        self.ShowMessage("Narrateur","franchement bravo")
        glob.MenuManager.ChangeMenu(Menus.MainMenu)
        
        
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
        debug = True
        if debug:
            self.hideCombat()
            self.ShowCharacter("flowey", ["idle.png", "sad.png", "smug.png"], True)
            #glob.AudioManager.PlayMusic("flowey.mp3")
            self.ShowMessage("Flowey", "Salut !")
            self.ShowMessage("Flowey", "Je suis Flowey !")
            self.Characters["flowey"].setChar("smug.png")
            self.ShowMessage("Flowey", "Flowey la fleur !")
            self.Characters["flowey"].setChar("idle.png")
            self.ShowMessage("Flowey", "Je vais t'apprendre comment on joue à ce jeu")
            self.ShowMessage("Flowey", "Utilise les flèches directionnel de ton clavier pour esquiver mes attaques")
            self.ShowMessage("Flowey", "La barre rouge qui apparaitra à ta gauche represente tes points de vie (PV)")
            self.ShowMessage("Flowey", "La bleu qui sera a ta droite represente des points de vie du monstre adverse (PVM)")
            self.ShowMessage("Flowey", "Esquive les attaques du mieux que tu peux !")
            self.showCombat()
            Attacks.attack_m2(self.AttackSprites)
            self.wait(6000)
           
                
            return
        #Intro (Name selection)
        self.AttackButton.Fade(0)
        self.hideCombat()
        self.ShowMessage("Narrateur", "Bonjour testeur, bienvenue dans \"LE REGLISSE DE LA VÉRITÉ\".")
        self.ShowMessage("Narrateur","Quel est votre nom ?")
        self.getInput("Entrez votre nom")
        test = self.getInput("Etes vous sur de choisir ce noms ? (o/n)")
        if test.lower() =="n":
            self.getInput("Très bien quel et votre nom ?")
            self.getInput("Très bien êtes vous sur ? (o/n)")
        self.ShowMessage("Narrateur", "Chara Melmou... c'est pas ouf comme nom, mais bon, on ne choisit pas nos parents")
        self.ShowCharacter("flowey", ["idle.png", "sad.png", "smug.png"], True)
        #glob.AudioManager.PlayMusic("flowey.mp3")
        self.ShowMessage("Flowey", "Salut !")
        self.ShowMessage("Flowey", "Je suis Flowey !")
        self.Characters["flowey"].setChar("smug.png")
        self.ShowMessage("Flowey", "Flowey la fleur !")
        self.Characters["flowey"].setChar("idle.png")
        self.ShowMessage("Flowey", "Je vais t'apprendre comment on joue à ce jeu")
        self.ShowMessage("Flowey", "Utilise les fléches directionnel de ton clavier pour esquiver mais attaque")
        self.ShowMessage("Flowey", "la barre rouge qui apparaitra a ta gauche represente tes point de vie (PV)")
        self.ShowMessage("Flowey", "la bleu qui sera a ta droite represente des point de vie du monstre adverse (PVM)")
        self.ShowMessage("Flowey", "Esquive les attaques du mieux que tu peux !")
        self.showCombat()
        Attacks.Attack_basic_1(self.AttackSprites)
        self.ShowMessage("Flowey", "Ok on recommence")
        Attacks.Attack_basic_2(self.AttackSprites)
        self.ShowMessage("Flowey", "bien attaque moi maintenant")
        self.ShowMessage("Flowey", "Tu vois ce bouton a droite il te permet de m'attaquer")
        self.AttackButton.Fade(1)
        Attacks.attack_retour(self.AttackSprites)
        self.ShowMessage("narrateur","ta survécu pas mal")
        self.ShowMessage("narrateur","monton d'un niveaux")
        Attacks.attack_cercle(self.AttackSprites)
        self.hideCombat()
        self.RemoveCharacter("flowey")
        self.ShowMessage("Narrateur", "STOOOP")
        self.ShowMessage("Narrateur", "VOUS ETES SERIEUX, IL Y A DES LIMITE A LA REFERENCE!!!!!!!!!!!")
        self.ShowMessage("Narrateur", "C'est bon tu prends tes clics et tes clacs,et tu sors de là!!!!")
        #fin de l'intro et du tutoriel
        self.SwitchBackground("bg_bar.png",500)
        self.ShowCharacter("haato",["idle.png"],scale=0.6)
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
        self.ShowMessage("Narrateur","Vous êtes Chara Melmou. Vous êtes dans une auberge, après avoir bien manger vous décidez d'aller acheter du réglisse")
        self.ShowMessage("Chara Melmou","Rééééééégliiiiiiise")
        self.ShowMessage("Narrateur","Tais-toi j'introduis le scénario!!!!!!!!!!!")
        self.ShowMessage("Narrateur","Vous parter donc en acheter dans une boutique")
        self.SwitchBackground("bg_boutique_inside.jpg",4500)
        glob.AudioManager.PlaySound("bruit_de_pas.mp3")
        self.Characters["haato"].MoveTo(vector2(-600,0),5500)
        self.wait(5500)
        self.Characters["haato"].VertFlip()
        self.ShowCharacter("roberu",["roberu.png", "roberu_happy.png", "roberu_bad.png"],scale=0.6)
        self.Characters["roberu"].Move(vector2(600,0))
        self.ShowMessage("Roberu","Boujour je peux vous aider ? ")
        self.ShowMessage("Narrateur","(Vous demandez du reglisse)")
        self.Characters["roberu"].Move(vector2(600,0))
        self.Characters["roberu"].setChar("roberu_bad.png")
        self.Characters["roberu"].Move(vector2(600,0))
        self.ShowMessage("Roberu","Désolé on nous a tous volé!!")
        glob.AudioManager.PlaySound("nani.mp3")
        self.ShowMessage("Chara Melmou","!!!!!")
        self.Characters["roberu"].setChar("roberu_happy.png")
        self.ShowMessage("Roberu","Mais si vous voulez j'ai du caramel mou")
        self.ShowMessage("Narrateur","(Vous demandez qui à voler la reglisse)")
        self.ShowMessage("Roberu","Je sais pas mais cet idiot est partie dans la fôret...")
        self.ShowMessage("Roberu","Vers le labyrinthe.")
        self.ShowMessage("Narrateur","Voulez-vous continuer ? (o/n)")
        conteneur=self.getInput("Choissiez-vous de continuer?")
        while conteneur.lower()!="o":
            self.ShowMessage("Narrateur","aucun probleme tu sais je peut parler des années")
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
        self.RemoveCharacter("haato")
        self.RemoveCharacter("roberu")

        self.SwitchBackground("japan.jpg",100)
        self.ShowCharacter("haato",["idle.png"],scale=0.6)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")  
        self.Characters["haato"].MoveTo(vector2(10000,0),1000)
        self.ShowMessage("Narrateur","DE L'AUTRE COTÉ !!!")
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(-10000,0),1000)
        self.wait(2500)
        
        self.SwitchBackground("New_York.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(10000,0),1000)
        self.wait(2500)
        
        self.SwitchBackground("egypt.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(-10000,0),1000)
        self.wait(2500)
        
        self.SwitchBackground("bear.jpg",100)
        glob.AudioManager.PlaySound("fast-car-sound-effect.mp3")
        self.Characters["haato"].MoveTo(vector2(10000,0),1000)
        self.wait(2500)      

        self.SwitchBackground("forest 2.png",100)
        self.wait(2000)
        
        self.ShowMessage("Narrateur","STOP!!!")
        self.ShowMessage("Chara Melmou","?!!")
        glob.AudioManager.PlaySound("Crissement de pneus 1.mp3")
        self.Characters["haato"].MoveTo(vector2(0,0),1000)       
        self.wait(2000)
        glob.AudioManager.PlaySound("DIO.mp3")
        
        self.ShowMessage("???","*Bruit de pas*")
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].VertFlip() 
        self.wait(1000)
        self.Characters["haato"].VertFlip()
        self.wait(1000)
        self.Characters["haato"].MoveTo(vector2(-600,0),1000)
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Qui... est Là !?")  
        self.SwitchBackground("forest 1.jpg",4500)
        self.wait(4500) 
        self.ShowMessage("???","Je suis personnage secondaire et mon but est de faire avancer le scénario")
        self.ShowMessage("personnage secondaire"," Je peux t'aider à obtenir ce que tu cherche. Tu peux me fare confiance, suis moi !")
        self.ShowMessage("Narrateur","Chara Melmou ne pouvais LOGIQUEMENT pas lui faire confiance")
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Hhhmmmm...")
        glob.AudioManager.PlaySound("reflexion.mp3")
        self.wait(12000)
        self.wait(2000)
        self.ShowMessage("personnage secondaire"," Je te propose de faire un marché, tu élimine quelqu'un pour moi et en échange je te donnerais de quoi t'aider à obtennir le réglisse que tu convoite")
        self.wait(2000)
        self.ShowMessage("Chara Melmou","OK !")
        self.ShowMessage("Narrateur","Quel abruti...")
        self.ShowMessage("personajsegondèr"," ravi de l'entendre, en passant tu peux m'appeler Anne, c'est comme cela que les amis que je n'ai pas m'appellent !")
        self.ShowMessage("Anne","Bon pour commencer la personne que tu cherche se trouve *au sommet de la montagne*, mais pour y accéder tu devras passer dans son donjon")
        self.ShowMessage("Anne","le donjon est interminable, et de ce fait je vais de donner un raccourci")
        self.ShowMessage("Anne","tu aurras 3 ennemis à battre dont...")
        self.wait(2000)
        self.ShowMessage("Narrateur","réveille TOI !!!")
        glob.AudioManager.PlaySound("gifle.mp3")
        self.wait(1000)
        self.ShowMessage("Chara Melmou","Aïe !!")
        self.ShowMessage("Chara Melmou","pourquoi tu m'a frappé !!? je ne dormais pas c'est mes yeux qui sont comme ça")
        self.ShowMessage("Narrateur","oui. je sais.")
        self.ShowMessage("Chara Melmou","?..")
        self.ShowMessage("Anne","Bon je t'espliquerais en chemain allons-y")
        self.Characters["haato"].MoveTo(vector2(2000,0),2000)
        self.RemoveCharacter("haato")
        
        self.ShowMessage("Narrateur","(rigole) Chara Melmou et Anne arrivèrent devans la porte du donjon")
        self.SwitchBackground("dungeon.jpg",4500)
        self.wait(2000)
        
        self.ShowMessage("Anne","Je t'ai tout dit maintenant tu est prêt.")
        """explication de l'inventaire + potions"""
        
        self.ShowMessage("Chara Melmou","Allons y !!")
        """self.SwitchBackground("une heure plus tard",100)"""
        """glob.AudioManager.PlaySound("one hour later.mp3")"""
        
        
        
        """ COMBAT 1 """
        
        
        """self.SwitchBackground("étage donjon 1",100)"""
        self.ShowMessage("Narrateur","vous rencontrez un ennemie")
        self.ShowMessage("Narrateur","j'espère que tu vas y passer...")
        self.wait(4500)
        
        """introduction de l'ennemie ("rick astley" (meme))"""
        """phase combat"""
        
        self.ShowMessage("Narrateur","c'est quoi ce bordel pourquoi les ennemies sont si nul...")
        self.ShowMessage("Chara Melmou","Victoire !!")
        self.ShowMessage("Anne","je savais que tu en serais capable.")
        self.ShowMessage("Anne","Maintenant, avançons !")
        self.wait(4500)
        
        
        """ COMBAT 2 """
        
        
        """self.SwitchBackground("deux heures plus tard",100)"""
        """glob.AudioManager.PlaySound("two hours later.mp3")"""
        
        """self.SwitchBackground("étage donjon 2",100)"""
        self.ShowMessage("Narrateur","vous rencontrez un ennemie")
        self.ShowMessage("Narrateur","j'espère vraiment que tu vas y passer cette fois ci...")
        self.wait(4500)
        
        self.ShowMessage("Narrateur","Non mais serieusement c'est quoi ce truc...")
        
        """introduction de l'ennemie ("freddie mercury" (meme))"""
        """phase combat"""
        
        glob.AudioManager.PlaySound("mama.mp3")
        self.ShowMessage("Narrateur","mais c'est qu'il va la fermer !!!")
        glob.AudioManager.PlaySound("gifle.mp3")
        glob.AudioManager.PlaySound("gifle.mp3")
        self.wait(2500)
        self.ShowMessage("Chara Melmou","A moi le réglisse !!")
        self.ShowMessage("Anne","Tiens un petit cadeau !")
        
        self.ShowMessage("Narrateur","Vous obtenez une arme")
        """Ajout arme dans l'inventaire"""
        
        self.ShowMessage("Chara Melmou","merci Anne")
        self.ShowMessage("Anne","Continuons !")
        self.wait(4500)
        
        
        
        """ COMBAT 3 """
        
        
        """self.SwitchBackground("une eternité plus tard",100)"""
        """glob.AudioManager.PlaySound("one eternity later.mp3")"""
        
        """self.SwitchBackground("étage donjon 3",100)"""
        
        self.ShowMessage("Narrateur","vous rencontrez un ennemie")
        
        self.ShowMessage("Anne","Voici la personne que je voulais que tu élimine, fais attention il est dangereux !!")
        
        """introduction de l'ennemie ("shrek" (meme))"""
        """phase combat"""
        
        
        
        
        

        






