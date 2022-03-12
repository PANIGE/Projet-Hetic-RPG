from framework import glob
from framework.data import helper
from os import path
from math import cos, sin, radians
import pygame
import  time
from framework.data.data import *


class pSprite:
    """The main sprite class to make things more easier"""
    def __init__(self, filename:str, position:vector2, skinSource:SkinSource, field:Positions, origin:Positions, color:Color=Color(255,255,255,255), clock:Clocks=Clocks.game, load:bool=True):
        """
        :param filename: the filename of the file (relative to skinSource)
        :param position: the Origin position of the sprite (relative to the field and origin)
        :param skinSource: SkinSource is the directory of the sprite,
            user = Take from the user skin, if not present, take from local SkinSource
            local = Take from the dir /data/sprites/<filename>
        :param field: Anchor of the sprite, where should it be placed on the screen
        :param origin: the origin of the sprite, if the (0,0) is on the top or the bottom of the sprite, or even center !
        :param color: Color of the sprite, act as a Multiplier mask on the sprite (useful for glob.PixelWhite to get a color)
        :param clock: How the transformations should be applied
        :param load: is the sprite should be directly loaded, mainly used in game to use the same object instead of overloading
            the ram with copy of same object
        """
        if load:
            if skinSource == SkinSource.absolute:
                self.image = pygame.image.load(filename)
            else:
                self.image = pygame.image.load(glob.currentDirectory + "/data/sprites/"+filename)
            self.image = self.image.convert_alpha()
        else:
            self.image = None
        self.field = field
        self.Clock = clock
        self.origin = origin
        self.Depth = 0
        self.BorderRadius = 0
        self.originPosition = position
        self.posMult = 1
        self.posMultY = 1
        self.position = vector2(0,0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale" : {}, "fade" : {}, "VectorScale": {}, "position": {}, "colorFade":{}, "rotation":{}}
        self.alpha = 1
        self.vectorScale = vector2(1,1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.offset = None

        self.isonHover = False
        self.onhover = []
        self.onhoverlost = []
        self.onclick = []
        self.enabled =True
        self.data = []

        if load:
            width = self.image.get_width()
            height = self.image.get_height()
            self.srcImg = self.image.convert_alpha()
            self.unBlendedImg = self.image.convert_alpha()
            colorR = self.color.r
            colorG = self.color.g
            colorB = self.color.b
            colorA = self.color.a
            self.srcImg.fill((colorR,colorG,colorB,colorA), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = pygame.transform.scale(self.srcImg, (
            int(width * glob.windowManager.getPixelSize() * self.scale),
            int(height * glob.windowManager.getPixelSize() * self.scale)))
            self.UpdateStats()
        else:
            self.srcImg = None
            self.unBlendedImg = None


        



    def loadFrom(self, other):
        """Used to use this sprite from another sprite as reference, and avoiding ram overloading, but remind that any transformaiton except position change will result to a copy of the sprite"""
        self.srcImg = other.srcImg
        self.unBlendedImg = other.unBlendedImg
        self.image = other.image
        self.UpdateStats()


    def Horiflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, False, True)
        self.Scale(self.scale)

    def Vertflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, True, False)
        self.Scale(self.scale)

    def changeImageFromString(self, string, size):
        self.unBlendedImg = pygame.image.fromstring(string, size,
                                             mode).convert_alpha()
        self.Color(self.color)



    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](**hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](**hoverLostAction[1])

    def __onClick__(self):
        for onClick in self.onclick:
            if onClick[1] == {}:
                onClick[0]()
            else:
                onClick[0](**onClick[1])

    def onHover(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is enabled and just got hovered
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onhover.append([function, kwargs])

    def disable(self):
        """
        Disable any transition and every input if enabled
        """
        self.enabled = False
        self.image.set_alpha(int((self.alpha/4)*255))
        self.HiddenColor(Color(self.color.r*0.3, self.color.g*0.3, self.color.b*0.3))


    def enable(self):
        """
        Enable any transition and every input if disabled
        """
        self.enabled = True
        self.image.set_alpha(self.alpha)
        self.HiddenColor(self.color)


    def onHoverLost(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is enabled and just lost hover
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is clicked on
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onclick.append([function, kwargs])

    def Rotate(self, deg):
        """
        Rotate the sprite (must be done after scaling or color change)
        :param deg: rotation deg from 1 to 360
        """
        self.rotation = deg
        self.image = pygame.transform.rotate(self.image, deg)
        self.UpdateStats(True)

    def borderBounds(self, borderRadius):
        """
        :param borderRadius: BorderRadius of the sprite, refer to css border-radius
        """
        self.BorderRadius = borderRadius
        self.image = pygame.image.fromstring(helper.cornerBounds(self, borderRadius), self.image.get_size(), "RGBA").convert_alpha()

    def crop(self, x, y):
        """
        Image cropping (must be done after scaling) (will take the center of the image as origin)
        :param x: Width of the image
        :param y: Height of the image
        """
        offset = vector2(0, 0)
        width = self.unBlendedImg.get_width()
        height = self.unBlendedImg.get_height()
        self.Scale(1920/width)
        self.image = self.image.subsurface((width/2, height/2-(y/2), x*glob.windowManager.getPixelSize(), y*glob.windowManager.getPixelSize()))
        self.UpdateStats()

    def Scale(self, x):
        """
        Image rescaling
        :param x: Scale factor
        """
        self.scale = x
        width = self.srcImg.get_width()
        height = self.srcImg.get_height()
        self.image = pygame.transform.smoothscale(self.srcImg, (int(width*glob.windowManager.getPixelSize()*x*self.vectorScale.x), int(height*glob.windowManager.getPixelSize()*x*self.vectorScale.y)))
        if self.BorderRadius > 0:
            self.image = pygame.image.fromstring(helper.cornerBounds(self, self.BorderRadius), self.image.get_size(), "RGBA").convert_alpha()
        self.image.set_alpha(255 * self.alpha)
        self.UpdateStats()

    def Color(self, color):
        """
        Multiply mask Color (will replace other Color transformations)
        :param color: Color of the sprite
        """
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcImg.fill((color.r, color.g, color.b, color.a), special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)


    def HiddenColor(self, color):
        """
        Same as Color, but will not register color in variable, so can be cancelled with obj.Color(obj.color)
        :param color: Color of the sprite
        """
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.srcImg.fill((color.r, color.g, color.b, color.a), special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def FillColor(self, Color):
        """
        Will add a normal filter on the sprite, act like Color
        :param color: Color of the sprite
        """
        self.Color(self.color)
        s = pygame.Surface((self.srcImg.get_width(), self.srcImg.get_height()))
        s.set_alpha(Color.a)
        s.fill((Color.r, Color.g, Color.b))
        self.srcImg.blit(s, (0,0))
        self.Scale(self.scale)



    def VectorScale(self, vectorScale):
        """
        Allow Different Width/height Scaling, Useful for glob.WhitePixel to fill surfaces
        :param vectorScale:
        :return:
        """
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        """
        Set global opacity of the sprite
        :param x: 0 to 1 float opacity
        """
        self.alpha = x
        self.image.set_alpha(255*x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["position"]["beginTime"] = time.time()*1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["position"]["endTime"] = time.time()*1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos()+ duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x,y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop



    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["fade"]["beginTime"] = time.time()*1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["fade"]["endTime"] = time.time()*1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos()+ duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["colorFade"]["beginTime"] = time.time()*1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["colorFade"]["endTime"] = time.time()*1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos()+ duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop



    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["VectorScale"]["beginTime"] = time.time()*1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["VectorScale"]["endTime"] = time.time()*1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos()+ duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop


    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["scale"]["beginTime"] = time.time()*1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["scale"]["endTime"] = time.time()*1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos()+ duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop


    def ClearTransformations(self, type=None):
        self.transformations = {"scale" : {}, "fade" : {}, "VectorScale": {}, "position": {}, "colorFade":{}, "rotation":{}}

    def UpdateStats(self, init=False):
        if self.field == Positions.topLeft:
            self.offset = vector2(0,0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(glob.windowManager.width/2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(glob.windowManager.width,0)
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, glob.windowManager.height/2)
        elif self.field == Positions.centre:
            self.offset = vector2(glob.windowManager.width/2, glob.windowManager.height/2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(glob.windowManager.width, glob.windowManager.height/2)

        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, glob.windowManager.height)
            self.posMultY = -1
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(glob.windowManager.width/2, glob.windowManager.height)
            if init:
                self.posMultY = -1
        elif self.field == Positions.bottomRight:
            self.offset = vector2(glob.windowManager.width, glob.windowManager.height)

        width = self.image.get_width()
        height = self.image.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width/2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height/2
        elif self.origin == Positions.centre:
            self.offset.x -= width/2
            self.offset.y -= height/2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height/20
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width/2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.offset.x,self.offset.y)

    def angularMove(self, angle, dis, duration, easing=EaseTypes.linear):
        xx = self.position.x + (dis * cos(radians(angle)))
        yy = self.position.y + (dis * sin(radians(angle)))
        self.MoveTo(xx, yy, duration, easing)

    def isColliding(self, collider):
        beginRect = vector2((
            self.effectivePosition.x + glob.windowManager.getPixelSize()*
                            ((self.originPosition.x + self.position.x))),
            self.effectivePosition.y + glob.windowManager.getPixelSize()*
                            ((self.originPosition.y + self.position.y)))

        endRect = vector2(
                        beginRect.x + (self.image.get_width()),
                        beginRect.y + (self.image.get_height())
                        )

        oBeginRect, oEndRect = collider.getRect()

        return ((oBeginRect.x > beginRect.x and oBeginRect.x < endRect.x) \
            or (oEndRect.x > beginRect.x and oEndRect.x < endRect.x)) \
                \
            and ((oBeginRect.y > beginRect.y and oBeginRect.y < endRect.y)\
            or (oEndRect.y > beginRect.y and oEndRect.y < endRect.y))

    def getRect(self):
        beginRect = vector2((
            self.effectivePosition.x + glob.windowManager.getPixelSize()*
                            ((self.originPosition.x + self.position.x))),
            self.effectivePosition.y + glob.windowManager.getPixelSize()*
                            ((self.originPosition.y + self.position.y)))

        endRect = vector2(
                        beginRect.x + (self.image.get_width()),
                        beginRect.y + (self.image.get_height())
                        )
        return beginRect, endRect

    def draw(self):
        if self.enabled:
            beginRect = vector2((
                self.effectivePosition.x + glob.windowManager.getPixelSize()*
                                ((self.originPosition.x + self.position.x) * self.posMult)),
                self.effectivePosition.y + glob.windowManager.getPixelSize()*
                                ((self.originPosition.y + self.position.y) * self.posMultY))

            endRect = vector2(
                            beginRect.x + (self.image.get_width()),
                            beginRect.y + (self.image.get_height())
                            )
            actuallyHover = (glob.cursorPos.x > beginRect.x and glob.cursorPos.x < endRect.x) and (glob.cursorPos.y > beginRect.y and glob.cursorPos.y < endRect.y) and self.alpha > 0
            if  actuallyHover and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not actuallyHover and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()

            if self.Clock == Clocks.game:
                now = time.time()*1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"]["endTime"] - self.transformations["rotation"]["beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"]["endTime"] = now+duration
                        self.transformations["rotation"]["beginValue"] = endValue
                        self.transformations["rotation"]["endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Rotate(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))


            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - self.transformations["scale"][
                            "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"]["endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - self.transformations["fade"]["beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"]["endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(helper.getTimeValue(beginTime, endtime, beginValue, endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime, beginValue, endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"]["beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"]["beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if self.vectorScale.x == endValueX and self.vectorScale.y == endValueY:
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"]["endTime"] - self.transformations["VectorScale"][
                            "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"]["endTime"] = now + duration
                        self.transformations["VectorScale"]["beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"]["endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(vector2(helper.getTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                                helper.getTimeValue(beginTime, endtime, beginValueY, endValueY, easing)))
                    else:
                        self.VectorScale(vector2(helper.getAudioTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                                helper.getAudioTimeValue(beginTime, endtime, beginValueY, endValueY, easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if self.color.r == endValueR and self.color.g == endValueG and self.color.b == endValueB:
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"]["endTime"] - self.transformations["colorFade"][
                            "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"]["endTime"] = now + duration
                        self.transformations["colorFade"]["beginValue"] = Color(endValueR, endValueG, endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime, beginValueR, endValueR, easing),
                            helper.getTimeValue(beginTime, endtime, beginValueG, endValueG, easing),
                            helper.getTimeValue(beginTime, endtime, beginValueB, endValueB, easing) ))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime, beginValueR, endValueR, easing),
                            helper.getAudioTimeValue(beginTime, endtime, beginValueG, endValueG, easing),
                            helper.getAudioTimeValue(beginTime, endtime, beginValueB, endValueB, easing)))


            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if self.position.x == endValueX and self.position.y == endValueY:
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"]["endTime"] - self.transformations["position"][
                            "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"]["endTime"] = now + duration
                        self.transformations["position"]["beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(helper.getTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                                helper.getTimeValue(beginTime, endtime, beginValueY, endValueY, easing))
                    else:
                        self.position = vector2(helper.getAudioTimeValue(beginTime, endtime, beginValueX, endValueX, easing),
                                                helper.getAudioTimeValue(beginTime, endtime, beginValueY, endValueY, easing))
        self.UpdateStats()
        if self.alpha != 0:
            glob.surface.blit(self.image,
                            (self.effectivePosition.x + glob.windowManager.getPixelSize()*
                            ((self.originPosition.x + self.position.x) * self.posMult),
                            self.effectivePosition.y + glob.windowManager.getPixelSize()*
                            ((self.originPosition.y + self.position.y) * self.posMultY)))



    