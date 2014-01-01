import datetime
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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.canvas = pygame.Surface(self.screen.get_size())
        self.fonts = [pygame.font.Font("SourceSansPro-ExtraLight.ttf", 86),
                      pygame.font.Font("SourceSansPro-Regular.ttf", 108),
                      pygame.font.Font("SourceSansPro-Bold.ttf", 222),
                      pygame.font.Font("SourceSansPro-Bold.ttf", 72)]
        pygame.display.set_caption("Countdown to {}".format(year))
        pygame.mouse.set_visible(0)
    @property
    def font(self):
        txt = self.timeleft
        linecount = len(txt.split("\n"))
        if datetime.datetime.now() > self.nye:
            return self.fonts[3]
        elif linecount > 3:
            return self.fonts[0]
        elif linecount > 1 or len(txt) > 4:
            return self.fonts[1]
        else:
            return self.fonts[2]
    @property
    def done(self):
        return ((self.nye - datetime.datetime.now()) >
                datetime.timedelta(days=1))
    def tick(self):
        timeleft = self.timeleft
        self.canvas.fill((255, 255, 255))
        graphic = self.font.render(timeleft, 1, (0, 0, 0))
        x = 100
        if len(timeleft.split("\n")) < 2:
            x = (self.screen.get_width() / 2) - (graphic.get_width() / 2)
        y = (self.screen.get_height() / 2) - (graphic.get_height() / 2)
        self.canvas.blit(graphic, (x, y))
        self.screen.blit(self.canvas, (0, 0))
        pygame.display.flip()
        for item in pygame.event.get():
            if ((item.type == pygame.QUIT) or
                (item.type == pygame.KEYUP and item.key == pygame.K_ESCAPE)):
                sys.exit()
    @property
    def timeleft(self):
        if datetime.datetime.now() > self.nye:
            return "HAPPY NEW YEAR"
        delta = self.nye - datetime.datetime.now()
        returnstringlist = []
        days, seconds = delta.days, delta.seconds
        if days == 0 and seconds < 30:
            return str(seconds)
        if days > 0:
            returnstringlist.append("{:>3} day{}".format(days, 's' if
                days != 1 else ''))
        if seconds > (60 * 60):
            hours = seconds / (60 * 60)
            returnstringlist.append("{:>3} hour{}".format(hours, 's' if
                hours != 1 else ''))
        if seconds > 60:
            minutes = (seconds / 60) % 60
            returnstringlist.append("{:>3} minute{}".format(minutes, 's' if
                minutes != 1 else ''))
        returnstringlist.append("{:>3} second{}".format(seconds % 60, 's' if
        seconds % 60 != 1 else ''))
        return "\n".join(returnstringlist)

if __name__ == "__main__":
    #pygame.init()
    #pygame.font.init()
    timer = CountdownTimer()
    while not timer.done:
        timer.tick()
        time.sleep(0.25)
