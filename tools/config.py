import configparser
import os
class Config():
    def __init__(self,defaultPath = None,path = None):
        self.defaultPath = defaultPath
        self.path = path
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
    def getAsList(self,item):
        res = []
        for e in self.config["SETTINGS"][item].split(","):
            res.append(e)
        return res
    def SaveChanges(self):
        with open(os.path.join(self.path,'config.ini'), 'w') as configfile:
            self.config.write(configfile)
