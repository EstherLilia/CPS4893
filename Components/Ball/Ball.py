import pygame
import time

class Ball_Engine():
    def __init__(self, path, pos, amount, model, scale=1):

        self.model = model
        self.amount = amount
        self.imgList = []
        self.pos = pos
        self.current_sprite = 0
        
        for i in range(1, self.amount+1):
            img = pygame.image.load(path + "frame" + str(i) + ".png").convert_alpha()
            self.width, self.height = img.get_size()
            img = pygame.transform.smoothscale(img, (int(self.width * scale), int(self.height * scale)))
            self.imgList.append(img)

        self.img = self.imgList[self.current_sprite]

        self.starting_time = time.time()

        

    def draw(self, speed):
        self.model.screen.blit(self.img, self.pos)
        current_time = time.time()
        remaining_time = current_time - self.starting_time
        self.current_sprite = remaining_time / speed * self.amount
        self.actucal_sprite = int(self.current_sprite)
        if current_time - self.starting_time >= speed:
            self.starting_time = current_time
            self.current_sprite = 0
            self.actucal_sprite = 0
        self.img = self.imgList[self.actucal_sprite]
