import configparser
import os

DOMAIN = ""
DOWNLOAD_PATH = ""

class Config(object):
    def loadConfig(self, path):
        global DOMAIN, DOWNLOAD_PATH
        if not os.path.exists(path):
            return ""
        config = configparser.ConfigParser()
        config.read(path)
        DOMAIN = config["default"]["domain"]
        DOWNLOAD_PATH = config["default"]["path"]
    
    def getDomain(self):
        global DOMAIN
        return DOMAIN
    
    def getDownloadPath(self):
        global DOWNLOAD_PATH
        return DOWNLOAD_PATH
