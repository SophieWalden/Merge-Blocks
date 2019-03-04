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

def rankup(rank):
    #Defines the new colors for each rank
    Colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,128),(0,255,255),
              (0,128,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127), (0,0,0)]
    return Colors[rank-1]

class Tile():
    def __init__(self,Pos, Rank):
        self.x = Pos[0]*110+200
        self.y = Pos[1]*110+170
        self.width = 100
        self.height = 100
        if Rank >= 1:
            self.color = rankup(Rank)
        else:
            self.color = (0,150,150)
        self.drag = False
        self.OldPos = [self.x,self.y]
        self.rank = Rank

    def draw(self):
        try:
            pygame.draw.rect(gameDisplay,self.color,(self.x,self.y,80,80),0)
        except Exception:
            self.color = (0,150,150)
    
    def update(self):
        self.draw()


#The Buttons
class Button():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, y):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width and self.y - y <= pos[1] <= self.y + self.height - y:
            pygame.draw.rect(gameDisplay,(150,0,0),(self.x,self.y - y,self.width,self.height),0)
        else:
            pygame.draw.rect(gameDisplay,(250,0,0),(self.x,self.y - y,self.width,self.height),0)
        pygame.draw.rect(gameDisplay,(100,100,100),(self.x,self.y - y,self.width,self.height),5)
    

#This is used to have numbers that are smaller, but still retain their value
def shorten(Num):
    count = 0
    let = ""
    while Num >= 1000:
        Num /= 1000
        count += 1
    Num = str(Num)
    Num2 = ""
    if count >= 1:
        for i in range(Num.index(".")+2):
            Num2 += Num[i]
        Num = Num2
    if count == 1:
        Num += "K"
    if count == 2:
        Num += "M"
    if count == 3:
        Num += "B"
    if count == 4:
        Num += "T"
    if count == 5:
        Num += "q"
    if count == 6:
        Num += "Q"
    if count == 7:
        Num += "s"
    if count == 8:
        Num += "S"
    return Num

def shop(upgrades, board, gold):
    run = True
    y = 0
    drag = False
    #Colors for all the ranks
    Colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,128),(0,255,255),
              (0,128,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127), (200,200,200)]
    Names = ["Red", "Orange", "Yellow", "Green", "Emerald", "Cyan", "Lapis", "Blue", "Purple",
             "Magenta", "Pink", "Black"]
    Buttons = []
    for i in range(12):
        if i != 0:
            Buttons.append(Button(400,117*i + 80,150,75))
        else:
            Buttons.append(Button(400,117*i + 90,150,75))

    while run:

        #Getting the position of the mouse
        pos = pygame.mouse.get_pos()

        #Drawing the background
        pygame.draw.rect(gameDisplay,(150,150,150),(100,0,500,800),0)

        #Drawing the squares
        for i in range(12):
            if upgrades[i][0] == False:
                if i != 0:
                    pygame.draw.rect(gameDisplay,(80,80,80),(110, 117*i + 73 - y,90, 90),0)
                    pygame.draw.rect(gameDisplay,(150,150,150),(145, 117*i + 130 - y,20, 20),0)
                    pygame.draw.line(gameDisplay,(150,150,150),(155, 117*i + 120 - y),(155, 117*i + 110 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(153, 117*i + 110 - y),(170, 117*i + 110 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(168, 117*i + 110 - y),(168, 117*i + 90 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(145, 117*i + 90 - y),(170, 117*i + 90 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(147, 117*i + 90 - y),(147, 117*i + 100 - y),5)
                    text_surface, rect = font_30.render(str("Locked"), (0, 0, 0))
                    gameDisplay.blit(text_surface, (210, 117*i + 105 - y))
                else:
                    pygame.draw.rect(gameDisplay,(80,80,80),(115, 117*i + 85 - y,75, 75),0)
                    pygame.draw.rect(gameDisplay,(150,150,150),(145, 117*i + 135 - y,20, 20),0)
                    pygame.draw.line(gameDisplay,(150,150,150),(155, 117*i + 125 - y),(155, 117*i + 115 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(153, 117*i + 115 - y),(170, 117*i + 115 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(168, 117*i + 115 - y),(168, 117*i + 95 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(145, 117*i + 95 - y),(170, 117*i + 95 - y),5)
                    pygame.draw.line(gameDisplay,(150,150,150),(147, 117*i + 95 - y),(147, 117*i + 105 - y),5)
                    text_surface, rect = font_30.render(str("Locked"), (0, 0, 0))
                    gameDisplay.blit(text_surface, (210, 117*i + 105 - y))
            else:
                if i != 0:
                    pygame.draw.rect(gameDisplay,Colors[i],(110, 117*i + 73 - y,90, 90),0)
                    text_surface, rect = font_30.render(str(Names[i]), (0, 0, 0))
                    gameDisplay.blit(text_surface, (210, 117*i + 90 - y))
                    text_surface, rect = font_30.render("Cost: " + str(shorten(upgrades[i][1])), (0, 0, 0))
                    gameDisplay.blit(text_surface, (210, 117*i + 130 - y))
                else:
                    pygame.draw.rect(gameDisplay,Colors[i],(115, 117*i + 85 - y,75, 75),0)
                    text_surface, rect = font_30.render(str(Names[i]), (0, 0, 0))
                    gameDisplay.blit(text_surface, (200, 117*i + 90 - y))
                    text_surface, rect = font_30.render("Cost: " + str(shorten(upgrades[i][1])), (0, 0, 0))
                    gameDisplay.blit(text_surface, (200, 117*i + 130 - y))

        #Drawing the buttons
        for i, button in enumerate(Buttons):
            if upgrades[Buttons.index(button)][0] == True:
                button.draw(y)
                if i != 0:
                    text_surface, rect = font_30.render(str("Buy"), (0, 0, 0))
                    gameDisplay.blit(text_surface, (450, 117*i + 105 - y))
                else:
                    text_surface, rect = font_30.render(str("Buy"), (0, 0, 0))
                    gameDisplay.blit(text_surface, (450, 117*i + 115 - y))

        #Drawing the lines
        for i in range(11):
            pygame.draw.line(gameDisplay,(80,80,80),(100,(i*117)-y+175),(560,(i*117)-y+175),3)

        #Drawing the top bar
        pygame.draw.rect(gameDisplay,(125,125,125),(100,0,500,75),0)
        pygame.draw.rect(gameDisplay,(125,125,125),(560,75,40,725),0)
        pygame.draw.line(gameDisplay,(80,80,80),(100,75),(600,75),5)
        text_surface, rect = font_50.render(("Shop"), (0, 0, 0))
        gameDisplay.blit(text_surface, (110, 10))
        if pos[0] >= 525 and pos[0] <= 575 and pos[1] >= 10 and pos[1] <= 60:
            pygame.draw.rect(gameDisplay,(150,0,0),(525,10,50,50),0)
        else:
            pygame.draw.rect(gameDisplay,(175,0,0),(525,10,50,50),0)
        pygame.draw.rect(gameDisplay,(50,0,0),(525,10,50,50),1)
        pygame.draw.line(gameDisplay,(80,80,80),(535,20),(565,50),5)
        pygame.draw.line(gameDisplay,(80,80,80),(565,20),(535,50),5)

        #Drawing the scroll bar
        pygame.draw.line(gameDisplay,(80,80,80),(560,75),(560,800),3)
        pygame.draw.rect(gameDisplay,(150,150,150),(565,80+y,30,50),0)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] >= 525 and pos[0] <= 575 and pos[1] >= 10 and pos[1] <= 60:
                    run = False
                if pos[0] >= 565 and pos[0] <= 595 and pos[1] >= 80+y and pos[1] <= 130+y:
                    drag = True
                for i, button in enumerate(Buttons):
                    if button.x <= pos[0] <= button.x + button.width and button.y - y <= pos[1] <= button.y + button.height - y and upgrades[i][0] == True and gold >= upgrades[i][1]:
                        count = 0
                        for row in board:
                            for tile in row:
                                if tile.rank == 0:
                                    count += 1
                        if count >= 1:
                            gold -= upgrades[i][1]
                            placed = False
                            while not placed:
                                num = random.randint(0,8)
                                if board[int(num/3)][num%3].rank == 0:
                                    board[int(num/3)][num%3] = Tile([int(num/3),num%3], i+1)
                                    placed = True
                        
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False

        if drag == True:
            y = pos[1] - 105
            if y >= 665:
                y = 665
            if y <= 0:
                y = 0


        

        pygame.display.flip()
        clock.tick(60)

    return upgrades, board, gold

if __name__ == "__main__":
    upgrades = []
    for i in range(12):
        upgrades.append([True, 50 * (2**(i+1))])
    upgrades[0][0] = True
    shop(upgrades)
