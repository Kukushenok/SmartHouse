class Command():
    def __init__(self,image,variable,calling):
        self.calling = calling
        self.variable = variable
        self.ru_calling = ""
        self.image = image
        self.speed = 5
        self.frame = 0
        self.woman = True
        self.future_variable = "None"
        self.callback = ""
    def check_calling(self,calling):
        call,res = calling.split("_")
        if call == self.calling:
            self.frame = self.speed
            self.future_variable = (res == "on")
            if self.future_variable == self.variable:
                self.frame = 0
                self.future_variable = "None"
                self.callback = self.ru_calling[0].upper()+self.ru_calling[1:]+" "
                self.callback +=("была уже включена" if self.woman else "был уже включён") if self.variable else ("была уже выключена" if self.woman else "был уже выключен")
    def check_callback(self):
        if self.callback:
            res = self.callback
            self.callback = ""
            return res
        if self.frame == -1:
            self.frame-=1
            return (("Включена " if self.woman else "Включён ") if self.variable else ("Выключена " if self.woman else "Выключен ")) + self.ru_calling
    def update(self):
        if self.frame>0:
            self.variable = not self.variable
            self.frame -=1
        elif self.frame == 0 and not self.future_variable == "None":
            self.variable = self.future_variable
            self.frame=-1

    def __bool__(self):
        return self.variable