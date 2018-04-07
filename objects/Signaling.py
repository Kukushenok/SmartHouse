import os
import pygame
import objects.Manager
class Signaling:
    def __init__(self):
        self.transparency=0
        self.job = {}
        self.image = pygame.image.load(os.path.join(os.getcwd(), "resources", "images","bubble.png"))
        self.lock_icon = pygame.image.load(os.path.join(os.getcwd(), "resources", "images","lock.png"))

    def blit_alpha(self,target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def set_transparency(self,set_to,time=0,context = "",user=""):
        self.job = {"time": time, "transparency_set_to": set_to, "transparency_was": self.transparency,"total_time": time,"context":context,"user":user}

    def update(self,tick):
        if self.job:
            self.transparency += (self.job["transparency_set_to"] - self.job["transparency_was"]) / self.job["total_time"] * tick
            self.job["time"] -= tick
            if self.job["time"] <=0:
                context = self.job["context"]
                self.transparency = int(self.job["transparency_set_to"])
                objects.Manager.Manager.getUsers().white_to_user(self.job["user"],"Сигнализация "+context)
                self.job = None

    def draw(self,surface,tick):
        self.update(tick)
        res = surface.copy()
        self.blit_alpha(res,pygame.transform.scale(self.image,(800,600)),(0,0),self.transparency)
        self.blit_alpha(res, pygame.transform.scale(self.lock_icon, (300, 400)), (250, 100), self.transparency//4)
        return res