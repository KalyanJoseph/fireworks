import pygame
from pygame.locals import *
import random
import math
import time

class Particle:
    def __init__(self, running, width, height, color):
        # initialising pygame
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Fireworks")  # setting title
        self.screen.fill(color)

        pygame.display.update()
        self.running = running

        # initialising clock
        self.clock = pygame.time.Clock()

        self.init_time = time.process_time()

        # colors
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)

    # function to create
    # one particle on the screen

    def createParticle(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, 3, 3))

    # returns a dict

    def returnParticle(self, x, y, color, vx, vy, maxHeight, delay):
        return {"x": x, "y": y, "color": color, "vx": vx, "vy": vy, "maxHeight": maxHeight, "exploded": False, "delay": delay}

    # returns a list consisting
    # of all the necessary things

    def manyParticles(self, number, color):
        group = []
        for i in range(number):
            x = random.randint(1, self.width-1)
            y = self.height-1
            vx = 0
            vy = 0
            maxHeight = random.randint(75, math.floor((self.height-1)/2))
            delay = random.uniform(0.1,500)

            group.append(self.returnParticle(x, y, color, vx, vy, maxHeight, delay))
        return group

    # the function to create
    # many particles

    def createParticles(self, particles):
        for particle in particles:
            self.createParticle(
                particle["x"], particle["y"], particle["color"])
        



    def mainRule(self, particles, g):
        particles1 = particles.copy()

        for i in range(len(particles1)):
            a = particles1[i]

            diff =  a["y"] - a["maxHeight"]

            if diff >= 50 and time.process_time() - self.init_time > a["delay"]:
                fy = diff/500
                fy *= -1
            elif a["exploded"] == False and time.process_time() - self.init_time > a["delay"]:
                fy = 0
                self.explosionGroup.append(self.manyExplode(20,a["x"], a["y"], a["color"]))
                a["color"] = self.black
                a["exploded"] = True
                particles.remove(a)
            else:
                fy=0



            a["vy"] = (a["vy"] + fy)*0.5

            a["x"] += a["vx"]
            a["y"] += a["vy"]

        for j in range(len(self.explosionGroup)):
            a = self.explosionGroup[j]

            self.createExplodes(a)

            self.explode(a)


    def returnExplode(self, x, y, color, vx, vy, init_x, init_y, size):
        return {"x": x, "y": y, "color": color, "vx": vx, "vy": vy, "init_x": init_x, "init_y": init_y, "size": size}


    def manyExplode(self, number, x, y, color):
        group = []
        for i in range(number):
            angle = ((i+1) / number) * 360
            vx = math.sin(math.radians(angle)) * 0.01
            vy = math.cos(math.radians(angle)) * 0.01
            init_x = x
            init_y = y
            size = 40

            group.append(self.returnExplode(x, y, color, vx, vy, init_x, init_y, size))
        return group
    

    def createExplodes(self, particles):
        for particle in particles:
            self.createExplode(
                particle["x"], particle["y"], particle["color"])
    

    def createExplode(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, 4, 4))


    def explode(self, particles):
        particles1 = particles.copy()

        for i in range(len(particles1)):
            a = particles1[i]

            diff_x = abs(a["x"] - a["init_x"])
            diff_y = abs(a["y"] - a["init_y"])

            if diff_x < a["size"] and diff_y < a["size"]:
                a["x"] += a["vx"]
                a["y"] += a["vy"]
            else:
                a["color"] = self.black
                particles.remove(a)
        

    
    def gameLoop(self):

        # defining particles
        self.yellowParticles = self.manyParticles(200, self.yellow)
        self.redParticles = self.manyParticles(200, self.red)
        self.greenParticles = self.manyParticles(200, self.green)
        self.blueParticles = self.manyParticles(200, self.blue)
        self.explosionGroup = []

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.createParticles(self.yellowParticles)
            self.createParticles(self.redParticles)
            self.createParticles(self.greenParticles)
            self.createParticles(self.blueParticles)

            self.mainRule(self.yellowParticles, -0.1)
            self.mainRule(self.redParticles, -0.1)
            self.mainRule(self.greenParticles, -0.1)
            self.mainRule(self.blueParticles, -0.1)
            
            pygame.display.update()

            self.screen.fill(0)

        pygame.quit()


def main():
    particleLife = Particle(True, 700, 500, (0, 0, 0))
    particleLife.gameLoop()


if __name__ == "__main__":
    main()