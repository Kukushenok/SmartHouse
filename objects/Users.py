import pygame
class Users():
    def __init__(self):
        self.users = []
    def add_user(self,nickname):
        self.users.append(nickname)
    def remove_user(self,nickname):
        self.users.pop(self.users.index(nickname))
    def render(self,screen):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        color = pygame.Color("black")
        textsurface = myfont.render("Управляющих: "+str(len(self.users)), False, color)
        screen.blit(textsurface,(screen.get_rect().width-textsurface.get_rect().width,0))
        for i in range(len(self.users)):
            textsurface = myfont.render(self.users[i], False, color)
            screen.blit(textsurface, (screen.get_rect().width - textsurface.get_rect().width, (i+1)*10))