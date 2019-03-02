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
font_50 = pygame.freetype.Font("Font.ttf", 50)
DisplayWidth,DisplayHeight = 700, 800
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Name")

class Tile():
    def __init__(self,Pos, Rank):
        self.x = Pos[0]*110+210
        self.y = Pos[1]*110+180
        self.width = 100
        self.height = 100
        if Rank == 1:
            self.color = (255,0,0)
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

def rankup(rank):
    #Defines the new colors for each rank
    Colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,128),(0,255,255),
              (0,128,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127)]
    return Colors[rank-1]

#A function that takes a number and returns a shorter number with a letter on its end
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
    

def game_loop():
    game_run = True
    board = [[0] * 3 for _ in range(3)]
    for j in range(3):
        for i in range(3):
            if j == 0 and i <= 1:
                board[j][i] = Tile([j,i], 1)
            else:
                board[j][i] = Tile([j,i], 0)
    MousePos = [0,0]
    selected = []
    Fillup = 0
    gold = 0
    GoldCooldown = time.process_time()+1

    while game_run == True:

        #Drawing the background
        gameDisplay.fill((0,150,150))
        pos = pygame.mouse.get_pos()
        for j in range(len(board)):
            for i in range(len(board[0])):
                pygame.draw.rect(gameDisplay,(150,150,150),(i*110 + 200,j*110+170,100,100),5)

        #Displays the Text
        text_surface, rect = font_50.render(("Gold: " + str(shorten(gold))), (0, 0, 0))
        gameDisplay.blit(text_surface, (285, 50))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Checking to see if any of the blocks are selected
                for j in range(len(board)):
                    for i in range(len(board[0])):
                        if board[j][i] != 0:
                            if board[j][i].x <= pos[0] <= board[j][i].x + board[j][i].width and board[j][i].y <= pos[1] <= board[j][i].y + board[j][i].height and board[j][i].rank >= 1:
                                MousePos = [board[j][i].x-pos[0], board[j][i].y-pos[1]]
                                board[j][i].OldPos = [board[j][i].x, board[j][i].y]
                                board[j][i].drag = True
                                selected = [i, j]
                #Spawning a new box
                if pos[0] >= 310 and pos[0] <= 410 and pos[1] >= 650 and pos[1] <= 750 and Fillup == 100:
                    count = 0
                    for row in board:
                        for tile in row:
                            if tile.rank == 0:
                                count += 1
                    if count >= 1:
                        placed = False
                        while not placed:
                            num = random.randint(0,8)
                            if board[int(num/3)][num%3].rank == 0:
                                board[int(num/3)][num%3] = Tile([int(num/3),num%3], 1)
                                placed = True
                                Fillup = 0
                                
                            
            if event.type == pygame.MOUSEBUTTONUP:
                #Putting down the blocks
                for j in range(len(board)):
                    for i in range(len(board[0])):
                        if board[j][i] != 0:
                            if selected != []:
                                if pos[0] >= board[j][i].x and pos[0] <= board[j][i].x + board[j][i].width and pos[1] >= board[j][i].y and pos[1] <= board[j][i].y + board[j][i].height and board[j][i].drag == False and board[j][i].rank == board[selected[1]][selected[0]].rank:
                                    board[selected[1]][selected[0]] = Tile([selected[1],selected[0]], 0)
                                    board[j][i].rank += 1
                                    board[j][i].color = rankup(board[j][i].rank)

                                
                                if [board[j][i].x,board[j][i].y] != board[j][i].OldPos:
                                    board[j][i].x, board[j][i].y = board[j][i].OldPos[0], board[j][i].OldPos[1]
                            
                                if board[j][i].drag == True:
                                    for h in range(3):
                                        for l in range(3):
                                            if h * 110 + 210 <= pos[0] <= h * 110 + 310 and l * 110 + 180 <= pos[1] <= l * 110 + 280 and board[h][l].rank != board[j][i].rank:
                                                board[j][i], board[h][l] = board[h][l], board[j][i]
                                                board[j][i].x, board[j][i].y = board[j][i].OldPos[0],board[j][i].OldPos[1]
                                                board[h][l].x, board[h][l].y = board[h][l].OldPos[0],board[h][l].OldPos[1]
                                                board[h][l].drag = False
                                
                                board[j][i].drag = False
                                            
                                    
            
                            
                selected = []

        #Drawing and updating all the tiles
        for j in range(len(board)):
            for i in range(len(board[0])):
                if board[j][i] != 0:
                    board[j][i].update()
                    if board[j][i].drag == True:
                        board[j][i].x = pos[0] + MousePos[0]
                        board[j][i].y = pos[1] + MousePos[1]

        #Drawing the selected tile over the other ones
        for j in range(len(board)):
            for i in range(len(board[0])):
                if board[j][i].drag == True:
                    board[j][i].update()
                
        


        #Shows the little loading thing to spawn in a box at the bottom
        pygame.draw.rect(gameDisplay,(150,130,42),(310,750-Fillup,100,Fillup),0)
        pygame.draw.rect(gameDisplay,(100,80,32),(310,650,100,100),5)
        if Fillup < 100:
            Fillup += 2

        #Calculating gold
        if GoldCooldown - time.process_time() <= 0:
            GoldCooldown = time.process_time()+1
            for row in board:
                for tile in row:
                    gold += 2**tile.rank - 1

        


        pygame.display.flip()
        clock.tick(60)



game_loop()
