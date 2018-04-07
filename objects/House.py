import pygame
import os
import objects.Command
import objects.Room
import random
class House():

    def __init__(self):

        rooms = ["bath","bedroom2","kitchen","corridor","bedroom1","boiler"]
        ru_rooms = ["ванная","детская","гостинная","коридор","спальня","бойлерная"]
        ru_rooms_cased = ["в ванной","в детской","в гостинной","в коридоре","в спальне","в бойлерной"]
        coords = [(200,150),(450,130),(550,300),(400,200),(300,80),(150,220)]
        self.rooms = []

        for i in range(6):
            added_room = objects.Room.Room(rooms[i])
            added_room.text_pos=coords[i]
            added_room.temperature = 22
            added_room.ru_name = ru_rooms[i]
            added_room.ru_name_cased = ru_rooms_cased[i]
            self.rooms.append(added_room)

    def call(self,calling):

        print(calling)
        if not calling["ready"]: return None

        if calling["intent"]["type"] == "light_on":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        room.set_transparency("light",0,3,"Включён свет ")
                        break
                    else:
                        return "Busy"

        elif calling["intent"]["type"] == "light_off":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        room.set_transparency("light",100,3,"Выключен свет ")
                        break
                    else:
                        return "Busy"

        elif calling["intent"]["type"] == "set_temperature":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        room.set_transparency("temperature",int(calling["params"]["sys-number"]["value"]),int(calling["params"]["sys-number"]["value"])/3,"Установлена температура "+calling["params"]["sys-number"]["value"]+"° ")
                        break
                    else:
                        return "Busy"

    def draw(self,tick):

        result = pygame.image.load(os.path.join(os.getcwd(),"resources","images","house.jpg"))
        callback = None

        for room in self.rooms:
            draw = room.draw(result,tick)
            if draw[1]: callback = draw[1]
            result = draw[0]

        return result,callback