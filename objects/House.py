import pygame
import os
import objects.Command
import objects.Room
import objects.Signaling
class House():

    def __init__(self):
        rooms = ["bath","bedroom2","kitchen","corridor","bedroom1","boiler"]
        ru_rooms = ["ванная","детская","гостиная","коридор","спальня","бойлерная"]
        ru_rooms_cased = ["в ванной","в детской","в гостиной","в коридоре","в спальне","в бойлерной"]
        coords = [(200,150),(450,130),(550,300),(400,200),(300,80),(150,220)]
        self.rooms = []
        self.signalization = objects.Signaling.Signaling()
        for i in range(6):
            added_room = objects.Room.Room(rooms[i])
            added_room.text_pos=coords[i]
            added_room.temperature = 22
            added_room.ru_name = ru_rooms[i]
            added_room.ru_name_cased = ru_rooms_cased[i]
            self.rooms.append(added_room)

    def call(self,calling,user):
        #print(calling)
        if not calling["ready"]: return None

        if calling["intent"]["type"] == "light_on":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        if room.light_transparency == 0:
                            return "Свет уже включён."
                        room.set_transparency("light",0,3,"Включён свет ",user)
                        break
                    else:
                        return "Busy"

        elif calling["intent"]["type"] == "light_off":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        if room.light_transparency == 100:
                            return "Свет уже выключен"
                        room.set_transparency("light",100,3,"Выключен свет ",user)
                        break
                    else:
                        return "Busy"

        elif calling["intent"]["type"] == "set_temperature":
            for room in self.rooms:
                if room.ru_name == calling["params"]["roomid"]["value"]:
                    if not room.job:
                        if room.temperature == int(calling["params"]["sys-number"]["value"]):
                            return "Температура уже такая"
                        if int(calling["params"]["sys-number"]["value"]) > 40:
                            return "So hot"
                        elif int(calling["params"]["sys-number"]["value"]) < 10:
                            return "So cold"
                        room.set_transparency("temperature",int(calling["params"]["sys-number"]["value"]),abs(int(calling["params"]["sys-number"]["value"])-room.temperature),"Установлена температура "+calling["params"]["sys-number"]["value"]+"° ",user)
                        break
                    else:
                        return "Busy"
        elif calling["intent"]["type"] == "signaling_on":
            if not self.signalization.job:
                if self.signalization.transparency == 100:
                    return "Сигнализация уже включена"
                self.signalization.set_transparency(100,3,"включена",user)
            else: return "Busy"
        elif calling["intent"]["type"] == "signaling_off":
            if not self.signalization.job:
                if self.signalization.transparency == 0:
                    return "Сигнализация уже выключена"
                self.signalization.set_transparency(0,3,"выключена",user)
            else: return "Busy"

    def draw(self,tick):
        result = pygame.image.load(os.path.join(os.getcwd(),"resources","images","house.jpg"))
        callback = None
        for room in self.rooms: result = room.draw(result,tick)
        result = self.signalization.draw(result, tick)
        pygame.image.save(result,os.path.join(os.getcwd(),"house.png"))
        return result,callback