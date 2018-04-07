import os
import objects.PassHandler
import objects.House
import tools.config
import objects.Users
class Manager(object):
    users = None
    config = None
    passHandler = None
    house = None

    @staticmethod
    def getConfig():
        if not Manager.config: Manager.config = tools.config.Config(False, os.getcwd())
        return Manager.config

    @staticmethod
    def getPassHandler():
        if not Manager.passHandler: Manager.passHandler = objects.PassHandler.PassHandler(Manager.getConfig())
        return Manager.passHandler

    @staticmethod
    def getHouse():
        if not Manager.house: Manager.house = objects.House.House()
        return Manager.house

    @staticmethod
    def getUsers():
        if not Manager.users: Manager.users = objects.Users.Users()
        return Manager.users