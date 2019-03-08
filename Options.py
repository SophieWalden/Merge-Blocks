#Importing all the modules
try:
    import time, random, sys, os
except ImportError:
    print("Make sure to have the time module")
    sys.exit()
try:
    import pygame
except ImportError:
    print("Make sure you have python 3 and pygame.")
    sys.exit()
from pygame import freetype


#game_font = pygame.freetype.Font("Font.ttf", 75)
#text_surface, rect = game_font.render(("Programmer: 8BitToaster"), (0, 0, 0))
#gameDisplay.blit(text_surface, (150, 300))

# Initialize the game engine
pygame.init()


DisplayWidth,DisplayHeight = 700, 800
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Name")
font_50 = pygame.freetype.Font("Font.ttf", 50)
font_30 = pygame.freetype.Font("Font.ttf", 30)
SizeCheck = pygame.font.Font(None, 50)

class Button():
    def __init__(self, x, y, width, height, Text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = Text

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            pygame.draw.rect(gameDisplay,(150,0,0),(self.x,self.y,self.width,self.height),0)
        else:
            pygame.draw.rect(gameDisplay,(250,0,0),(self.x,self.y,self.width,self.height),0)
        pygame.draw.rect(gameDisplay,(100,100,100),(self.x,self.y,self.width,self.height),5)

        text_surface, rect = font_50.render(str(self.text), (0, 0, 0))
        gameDisplay.blit(text_surface, (self.x + int(self.width/2)+30 - int(SizeCheck.size(str(self.text))[0]), self.y + int(self.height/2) - 20))
            

def menu(board, gold, upgrades, Stats):
    game_run = True
    Buttons = [Button(125,100,200,100,"Save"), Button(375,100,200,100,"Load"),Button(125,225,200,100,"Stats")]
    screen = "Main"

    while game_run == True:


        pos = pygame.mouse.get_pos()
        pygame.draw.rect(gameDisplay,(150,150,150),(100,0,500,800),0)

        #Drawing the top bar
        pygame.draw.rect(gameDisplay,(125,125,125),(100,0,500,75),0)
        pygame.draw.line(gameDisplay,(80,80,80),(100,75),(600,75),5)
        if screen == "Main":
            text_surface, rect = font_50.render(("Options"), (0, 0, 0))
        if screen == "Stats":
            text_surface, rect = font_50.render(("Stats"), (0, 0, 0))
        gameDisplay.blit(text_surface, (110, 10))
        if pos[0] >= 525 and pos[0] <= 575 and pos[1] >= 10 and pos[1] <= 60:
            pygame.draw.rect(gameDisplay,(150,0,0),(525,10,50,50),0)
        else:
            pygame.draw.rect(gameDisplay,(175,0,0),(525,10,50,50),0)
        pygame.draw.rect(gameDisplay,(50,0,0),(525,10,50,50),1)
        pygame.draw.line(gameDisplay,(80,80,80),(535,20),(565,50),5)
        pygame.draw.line(gameDisplay,(80,80,80),(565,20),(535,50),5)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Checking all the mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen == "Main":
                    if pos[0] >= 525 and pos[0] <= 575 and pos[1] >= 10 and pos[1] <= 60:
                        game_run = False
                    for i, button in enumerate(Buttons):
                        if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                            if i == 0:
                                DataList = []
                                DataList.append(str(gold))
                                for row in board:
                                    for tile in row:
                                        DataList.append(str(tile.rank))
                                for upgrade in upgrades:
                                    DataList.append(str(upgrade[0]))
                                    DataList.append(str(upgrade[1]))
                                
                                SaveFile = open("Save File/SaveFile.txt","w")
                                SaveFile.write(" ".join(DataList))
                            if i == 1:
                                return "Load"
                            if i == 2:
                                screen = "Stats"
                if screen == "Stats":
                    if pos[0] >= 525 and pos[0] <= 575 and pos[1] >= 10 and pos[1] <= 60:
                        screen = "Main"
                            
        #Displaying all the buttons in the menu
        if screen == "Main":      
            for button in Buttons:
                button.draw()

        #Displaying the stats
        if screen == "Stats":
            text_surface, rect = font_50.render(("Tiles Spawned: " + str(Stats["Tiles"])), (0, 0, 0))
            gameDisplay.blit(text_surface, (150, 100))

            #Calculating Time
            Time = time.process_time()
            TimeList = [0,0,0]
            while Time >= 3600:
                Time -= 3600
                TimeList[0] += 1
            while Time >= 60:
                Time -= 60
                TimeList[1] += 1
            TimeList[2] = int(Time)
            for i, var in enumerate(TimeList):
                TimeList[i] = str(TimeList[i])
                if len(TimeList[i]) != 2:
                    TimeList[i] = "0" + TimeList[i]
            text_surface, rect = font_50.render("Time spent: " + str(TimeList[0]) + ":" + str(TimeList[1]) + ":" + str(TimeList[2]), (0, 0, 0))
            gameDisplay.blit(text_surface, (110, 150))
            
        
        pygame.display.flip()
        clock.tick(60)

    return False

if __name__ == "__main__":
    menu(0,0,0, {"Tiles": 0})
