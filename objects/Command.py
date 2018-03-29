class Command():
    def __init__(self,image,variable,calling):
        self.calling = calling
        self.variable = variable
        self.image = image
    def check_calling(self,calling):
        if calling == self.calling:
            self.variable = not self.variable
    def __bool__(self):
        return self.variable