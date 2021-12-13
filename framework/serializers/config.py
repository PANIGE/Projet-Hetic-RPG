import configparser
from os import path
from framework import glob
from pygame.locals import *
from json import loads, dumps

class Config:
    def __init__(self):
        self.writer = configparser.ConfigParser()
        if path.exists(glob.currentDirectory + "/DeltaDashConf.ini"):
            self.writer.read(glob.currentDirectory + "/DeltaDashConf.ini")
            self.config = self.writer["Delta Dash Config"]
        else:
            self.writer["Delta Dash Config"] = {}
            self.config = self.writer["Delta Dash Config"]
            self.config["volume"] = "float://"+str(1)
            self.config["CurrentRoom"] = "int://"+str(0)
            self.config["stats"] = "json://"+dumps(self.getBasicsStats())
            self.Save()

    def getValue(self, key:str):
        try:
            value = self.config[key]
            type, value = value.split("://")
            if type == "float":
                return float(value)
            if type == "int":
                return int(value)
            if type == "str":
                return str(value)
            if type == "json":
                return loads(value)
            else:
                return value
        except:
            glob.Logger.error("Tried to read unexisting value ({}) in DeltaDashConf.ini".format(key))
            return

    def setValue(self, key, value, type):
        if type == "float":
            ftype = float
        elif type == "str":
            ftype = str
        elif type == "int":
            ftype = int
        elif type == "json":
            type = "json"
        else:
            ftype = str
        self.config[key] = type + "://" + ftype(value) if type != "json" else "json://"+dumps(value)
        self.Save()


    def __getitem__(self, item):
        return self.getValue(item)

    def Save(self):
        with open(glob.currentDirectory + "/DeltaDashConf.ini", "w") as f:
            self.writer.write(f)

    def getBasicsStats(self):
        return {
            "pv" : 20,
            "lv" : 1,
            "inventory": []
        }