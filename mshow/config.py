import configparser
import os

NAME = ""
DOMAIN = ""
DOWNLOAD_PATH = ""
FILE_EXTENSION = ""

class Config(object):
    def loadConfig(self, path):
        global DOMAIN, DOWNLOAD_PATH, NAME, FILE_EXTENSION
        if not os.path.exists(path):
            return ""
        config = configparser.ConfigParser()
        config.read(path)
        NAME = config["default"]["name"]
        DOMAIN = config["default"]["domain"]
        DOWNLOAD_PATH = config["default"]["path"]
        FILE_EXTENSION = config["default"]["file_extension"]
    
    def getName(self):
        global NAME
        return NAME

    def getDomain(self):
        global DOMAIN
        return DOMAIN
    
    def getDownloadPath(self):
        global DOWNLOAD_PATH
        return DOWNLOAD_PATH

    def getFileExtension(self):
        global FILE_EXTENSION
        return FILE_EXTENSION
    
