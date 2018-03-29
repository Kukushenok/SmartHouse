import pygame
import os
import objects.Command
class House():
    def __init__(self):
        self.main_door_open = False
        self.ventilation = False
        self.condition = False
        self.temperature_mode = 20
        self.sauna_on = False
        self.light = False
        self.signalisation = True
        icon_list = ["signalization.png","ventilation.png","condition.png","light.png","sauna.png"]
        on_offs_list = [self.signalisation, self.ventilation, self.condition, self.light, self.sauna_on]
        callings = ["signalisation","ventilation","condition","light","sauna"]
        self.command_list = []
        for i in range(5):
            self.command_list.append(objects.Command.Command(icon_list[i],on_offs_list[i],callings[i]))
    def call(self,calling):
        for e in self.command_list: e.check_calling(calling)
    def draw(self):

        result = pygame.image.load(os.path.join(os.getcwd(),"resources","images","house.jpg"))
        for i in range(5):
            icon = pygame.image.load(os.path.join(os.getcwd(),"resources","images",self.command_list[i].image))
            work = pygame.image.load(os.path.join(os.getcwd(),"resources","images","on.png" if self.command_list[i] else "off.png"))
            work.blit(pygame.transform.scale(icon,(work.get_rect().width//2,work.get_rect().height//2)),(work.get_rect().width//2-icon.get_rect().width//4,work.get_rect().height//2-icon.get_rect().height//4))
            result.blit(pygame.transform.scale(work,(50,50)),(result.get_rect().width-50,50*i))
        return result
    def colder(self):
        self.temperature_mode-=5
        if self.temperature_mode<10:
            self.temperature_mode = 10
            return "Отклонено в связи безопасности"
        return "Текущая температура: "+str(self.temperature_mode)
    def hotter(self):
        self.temperature_mode+=5
        if self.temperature_mode>30:
            self.temperature_mode = 30
            return "Отклонено в связи безопасности"
        return "Текущая температура: " + str(self.temperature_mode)