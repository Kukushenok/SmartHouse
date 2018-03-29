import configparser
import os
class Config():
    def __init__(self,defaultPath = None,path = None):
        self.defaultPath = defaultPath
        self.config = configparser.ConfigParser()
        self.defaultConfig = configparser.ConfigParser()
        if path:
            self.config.read(os.path.join(path,'config.ini'))
            if self.defaultPath:self.defaultConfig.read(os.path.join(self.defaultPath, 'default_config.ini'))
        else:
            self.config.read('config.ini')
            if self.defaultPath:self.defaultConfig.read(os.path.join(self.defaultPath, 'default_config.ini'))
    def get(self,item):
        try:
            return self.config["SETTINGS"][item]
        except KeyError:
            return self.defaultConfig["SETTINGS"][item]
    def getAsDict(self,item):
        toDict = ""
        try:
            toDict = self.config["SETTINGS"][item]
        except KeyError:
            toDict =  self.defaultConfig["SETTINGS"][item]
        dictPairs = toDict.split(",")
        resDict = {}
        for e in dictPairs:
            splittedE = e.split(":")
            exec("resDict["+splittedE[0]+"] = "+splittedE[1])
        return resDict