import pygame
class Users():
    def __init__(self):
        self.users = []
    def add_user(self,nickname,messager):
        self.users.append({"nickname":nickname,"messager":messager})
    def remove_user(self,nickname):
        for i in range(len(self.users)):
            if self.users[i]["nickname"] == nickname:
                self.users.pop(i)
                return None
    def white_to_user(self,nickname,text):
        print(text)
        for user in self.users:
            if user["nickname"] == nickname:

                user["messager"].message.reply_text(text)
    def render(self,screen):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        color = pygame.Color("black")
        textsurface = myfont.render("Управляющих: "+str(len(self.users)), False, color)
        screen.blit(textsurface,(screen.get_rect().width-textsurface.get_rect().width,0))
        for i in range(len(self.users)):
            textsurface = myfont.render(self.users[i]["nickname"], False, color)
            screen.blit(textsurface, (screen.get_rect().width - textsurface.get_rect().width, (i+1)*10))