import pygame
import os
import objects.Command
import objects.Room
import random
class House():
    def __init__(self):
        #self.main_door_open = False
        #self.ventilation = False
        #self.condition = False
        #self.temperature_mode = 20
        #self.sauna_on = False
        #self.light = False
        #self.signalisation = True
        #icon_list = ["signalization.png","ventilation.png","condition.png","light.png","sauna.png"]
        #on_offs_list = [self.signalisation, self.ventilation, self.condition, self.light, self.sauna_on]
        #callings = ["signalisation","ventilation","condition","light","sauna"]
        #ru_callings = ["сигнализация","вентиляция","кондиционер","свет","сауна"]
        #speeds = [7,7,11,5,15]
        #womanity_list = [True,True,False,False,True]
        #self.command_list = []
        #for i in range(5):
        #    cmd = objects.Command.Command(icon_list[i],on_offs_list[i],callings[i])
        #    cmd.speed = speeds[i]
        #    cmd.ru_calling = ru_callings[i]
        #    cmd.woman = womanity_list[i]
        #    self.command_list.append(cmd)
        rooms = ["bath","bedroom2","kitchen","corridor","bedroom1","boiler"]
        coords = [(200,150),(450,130),(550,300),(400,200),(300,80),(150,220)]
        self.rooms = []
        for i in range(6):
            added_room = objects.Room.Room(rooms[i])
            added_room.text_pos=coords[i]
            added_room.temperature = 22
            self.rooms.append(added_room)
    #def call(self,calling):
    #    for e in self.command_list:e.check_calling(calling)
    #def callback(self):
    #    callback = ""
    #    for e in self.command_list:
    #        if not callback: callback = e.check_callback()
    #    if callback: return callback
    def draw(self,tick):
        result = pygame.image.load(os.path.join(os.getcwd(),"resources","images","house.jpg"))
        #for i in range(5):
        #    self.command_list[i].update()
        #    icon = pygame.image.load(os.path.join(os.getcwd(),"resources","images",self.command_list[i].image))
        #    work = pygame.image.load(os.path.join(os.getcwd(),"resources","images","on.png" if self.command_list[i] else "off.png"))
        #    work.blit(pygame.transform.scale(icon,(work.get_rect().width//2,work.get_rect().height//2)),(work.get_rect().width//2-work.get_rect().width//4,work.get_rect().height//2-work.get_rect().height//4))
        #    result.blit(pygame.transform.scale(work,(50,50)),(result.get_rect().width-50,55*i))
        for e in self.rooms: result = e.draw(result,tick)
        return result