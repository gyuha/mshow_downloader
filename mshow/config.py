import configparser
import os

NAME = ""
DOMAIN = ""
DOWNLOAD_PATH = ""

class Config(object):
    def loadConfig(self, path):
        global DOMAIN, DOWNLOAD_PATH, NAME
        if not os.path.exists(path):
            return ""
        config = configparser.ConfigParser()
        config.read(path)
        NAME = config["default"]["name"]
        DOMAIN = config["default"]["domain"]
        DOWNLOAD_PATH = config["default"]["path"]
    
    def getName(self):
        global NAME
        return NAME

    def getDomain(self):
        global DOMAIN
        return DOMAIN
    
    def getDownloadPath(self):
        global DOWNLOAD_PATH
        return DOWNLOAD_PATH
    
