import datetime
import os
import sys
import time

import pygame

class CountdownTimer(object):
    def __init__(self):
        now = datetime.datetime.now()
        year = now.year + 1
        if now.month < 2:
            year = now.year
        self.nye = datetime.datetime(year, 1, 1, 0, 0, 0)
        print self.nye
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600)) #, pygame.FULLSCREEN)
        self.canvas = pygame.Surface(self.screen.get_size())
        self.fonts = [pygame.font.Font("SourceSansPro-Regular.ttf", 86),
                      pygame.font.Font("SourceSansPro-Regular.ttf", 108),
                      pygame.font.Font("SourceSansPro-Bold.ttf", 222),
                      pygame.font.Font("SourceSansPro-Bold.ttf", 72)]
        if os.path.isfile('bgimage.jpg'):
            self.image = pygame.image.load('bgimage.jpg')
            #if (self.image.get_height() < self.screen.get_height() or
            #    self.image.get_width() < self.screen.get_width()):
            self.image = pygame.transform.smoothscale(self.image,
                    (self.screen.get_width(), self.screen.get_height()))
        else:
            self.bg = None
        pygame.display.set_caption("Countdown to {}".format(year))
        pygame.mouse.set_visible(0)
    @property
    def font(self):
        txt = self.timeleft
        linecount = len(txt.split("\n"))
        if datetime.datetime.now() > self.nye:
            return self.fonts[3]
        elif linecount > 2:
            return self.fonts[0]
        elif linecount > 1 or len(txt) > 4:
            return self.fonts[1]
        else:
            return self.fonts[2]
    @property
    def done(self):
        return ((self.nye - datetime.datetime.now()) >
                datetime.timedelta(days=1))
    @property
    def graphic(self):
        font = self.font
        tlines = self.timeleft.split("\n")
        graphics = [font.render(line, 1, (0, 0, 0)) for line in tlines]
        wd = max(g.get_width() for g in graphics)
        ht = sum(g.get_height() for g in graphics)
        surf = pygame.Surface((wd, ht), flags=pygame.SRCALPHA)
        y = 0
        for g in graphics:
            if len(tlines) > 2:
                x = 0
            else:
                x = (wd / 2) - (g.get_width() / 2)
            surf.blit(g, (x, y))
            y += g.get_height()
        return surf
    def tick(self):
        timeleft = self.timeleft
        self.canvas.fill((255, 255, 255))
        if self.image:
            bgx = (self.screen.get_width() / 2) - (self.image.get_width() / 2)
            bgy = (self.screen.get_height() / 2) - (self.image.get_height() / 2)
            self.canvas.blit(self.image, (bgx, bgy))
        graphic = self.graphic
        x = (self.screen.get_width() / 2) - (graphic.get_width() / 2)
        y = (self.screen.get_height() / 2) - (graphic.get_height() / 2)
        self.canvas.blit(graphic, (x, y))
        self.screen.blit(self.canvas, (0, 0))
        pygame.display.flip()
        for item in pygame.event.get():
            if ((item.type == pygame.QUIT) or
                (item.type == pygame.KEYUP and item.key == pygame.K_ESCAPE)):
                sys.exit()
    def loop(self):
        while not timer.done:
            self.tick()
            time.sleep(0.125)
    @property
    def timeleft(self):
        if datetime.datetime.now() > self.nye:
            return "HAPPY\nNEW\nYEAR"
        delta = self.nye - datetime.datetime.now()
        returnstringlist = []
        days, seconds = delta.days, delta.seconds
        if days == 0 and seconds < 30:
            return str(seconds)
        if days > 0:
            returnstringlist.append("{} day{}".format(days, 's' if
                days != 1 else ''))
        if seconds > (60 * 60):
            hours = seconds / (60 * 60)
            returnstringlist.append("{} hour{}".format(hours, 's' if
                hours != 1 else ''))
        if seconds > 60:
            minutes = (seconds / 60) % 60
            returnstringlist.append("{} minute{}".format(minutes, 's' if
                minutes != 1 else ''))
        returnstringlist.append("{} second{}".format(seconds % 60, 's' if
        seconds % 60 != 1 else ''))
        return "\n".join(returnstringlist)

if __name__ == "__main__":
    timer = CountdownTimer()
    timer.loop()
