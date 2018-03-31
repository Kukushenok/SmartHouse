class Command():
    def __init__(self,image,variable,calling):
        self.calling = calling
        self.variable = variable
        self.ru_calling = ""
        self.image = image
        self.speed = 5
        self.frame = 0
        self.woman = True
        self.future_variable = "N"
    def check_calling(self,calling):
        if calling.lower() == self.calling or self.ru_calling == calling.lower():
            self.frame = self.speed
            self.future_variable = not self.variable
    def check_callback(self):
        if self.frame == -1:
            self.frame-=1
            return (("Включена " if self.woman else "Включён ") if self.variable else ("Выключена " if self.woman else "Выключен ")) + self.ru_calling
    def update(self):
        if self.frame>0:
            self.variable = not self.variable
            self.frame -=1
        elif self.frame == 0 and not self.future_variable == "N":
            self.variable = self.future_variable
            self.frame=-1

    def __bool__(self):
        return self.variable