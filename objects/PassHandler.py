class PassHandler():
    def __init__(self,config):
        self.whitelist = config.getAsList("whitelist")
        self.passKey = config.get("passkey")
    def CheckOnWhitelist(self,name):
        if name in self.whitelist: return True
        return False
    def LogIn(self,password):
        if password == self.passKey: return True
        return False