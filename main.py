#Importing all the modules
try:
    import time, random, sys, os, datetime
except ImportError:
    print("Make sure to have the time module")
    sys.exit()
try:
    import pygame
except ImportError:
    print("Make sure you have python 3 and pygame.")
    sys.exit()
try:
    import Shop, MainMenu, Options
except ImportError:
    print("Make sure you have all the extra files")
from pygame import freetype




#game_font = pygame.freetype.Font("Font.ttf", 75)
#text_surface, rect = game_font.render(("Programmer: 8BitToaster"), (0, 0, 0))
#gameDisplay.blit(text_surface, (150, 300))

# Initialize the game engine
pygame.init()
font_50 = pygame.freetype.Font("Font.ttf", 50)
font_40 = pygame.freetype.Font("Font.ttf", 40)
font_35 = pygame.freetype.Font("Font.ttf", 35)
SizeCheck = pygame.font.Font(None, 50)
DisplayWidth,DisplayHeight = 700, 800
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Name")

#All of the blocks
class Tile():
    def __init__(self,Pos, Rank):
        self.x = Pos[0]*110+200
        self.y = Pos[1]*110+170
        self.width = 100
        self.height = 100
        if Rank >= 1:
            self.color = rankup(Rank%12)
        else:
            self.color = (0,200,200)
        self.drag = False
        self.OldPos = [self.x,self.y]
        self.rank = Rank

    def draw(self):
        pygame.draw.rect(gameDisplay,self.color,(self.x,self.y,80,80),0)
        if int(self.rank/12) != 0:
            text_surface, rect = font_50.render(str(int(self.rank/12)), (0, 0, 0))
            gameDisplay.blit(text_surface, (self.x+45 - int(SizeCheck.size(str(int(self.rank/12)))[0]), self.y+20))

    
    def update(self):
        self.draw()
                            
#The Buttons
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
        if self.text != "Options":
            gameDisplay.blit(text_surface, (self.x + int(self.width/2)+30 - int(SizeCheck.size(str(self.text))[0]), self.y + int(self.height/2) - 20))
        else:
            gameDisplay.blit(text_surface, (self.x + int(self.width/2)+43 - int(SizeCheck.size(str(self.text))[0]), self.y + int(self.height/2) - 20))
            

def rankup(rank):
    #Defines the new colors for each rank
    Colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,128),(0,255,255),
              (0,128,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127), (0,0,0)]
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
    

def game_loop(Load):
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
    Popup = False
    GoldCooldown = time.process_time()+1
    Buttons = [Button(50,650,200,100, "Shop"),Button(450,650,200,100, "Options")]
    upgrades = []
    for i in range(12):
        upgrades.append([False, 50 * (2**(i+1))])
    SaveTime = time.process_time() + 10
    Stats = {"Tiles": 0}

    SaveFile = open("Save File/SaveFile.txt","r")
    Data = SaveFile.readline().split()
    count = 0
    if Load != "New":
        if len(Data) >= 1:
            gold = int(Data[count])
            count += 1
        if len(Data) >= 10:
            board = [[0] * 3 for _ in range(3)]
            for j in range(3):
                for i in range(3):
                    board[j][i] = Tile([j,i],int(Data[count]))
                    count += 1
        if len(Data) >= 22:
            for upgrade in upgrades:
                if Data[count] == "True":
                    upgrade[0] = True
                else:
                    upgrade[0] = False
                upgrade[1] = int(Data[count+1])
                count += 2

        if len(Data) >= 23:
            #Giving you gold for the missed time
            PastSeconds = int(Data[count])
            seconds = 0
            currentDT = datetime.datetime.now()
            seconds += currentDT.year * 31536000
            seconds += currentDT.month * 2592000
            seconds += currentDT.day * 86400
            seconds += currentDT.hour * 3600
            seconds += currentDT.minute * 60
            seconds += currentDT.second
            Change = seconds - PastSeconds
            gain = 0
            for row in board:
                for tile in row:
                    gain += (2**tile.rank - 1) * Change
            gold += gain
            count += 1

            Popup = True

    PopupButton = [Button(485,265,50,50,"")]

    while game_run == True:

        #Drawing the background
        gameDisplay.fill((0,200,200))
        pos = pygame.mouse.get_pos()
        for j in range(len(board)):
            for i in range(len(board[0])):
                pygame.draw.rect(gameDisplay,(150,150,150),(i*110 + 190,j*110+160,100,100),5)


        text_surface, rect = font_50.render(("Gold: " + str(shorten(gold))), (0, 0, 0))
        gameDisplay.blit(text_surface, (285 - int(SizeCheck.size(str(shorten(gold)))[0]), 50))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DataList = []
                DataList.append(str(gold))
                for row in board:
                    for tile in row:
                        DataList.append(str(tile.rank))
                for upgrade in upgrades:
                    DataList.append(str(upgrade[0]))
                    DataList.append(str(upgrade[1]))

                seconds = 0
                currentDT = datetime.datetime.now()
                seconds += currentDT.year * 31536000
                seconds += currentDT.month * 2592000
                seconds += currentDT.day * 86400
                seconds += currentDT.hour * 3600
                seconds += currentDT.minute * 60
                seconds += currentDT.second
                DataList.append(str(seconds))
                
                SaveFile = open("Save File/SaveFile.txt","w")
                SaveFile.write(" ".join(DataList))
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
                #Opening Shop
                if pos[0] >= 50 and pos[0] <= 250 and pos[1] >= 650 and pos[1] <= 750:
                    upgrades, board, gold = Shop.shop(upgrades, board, gold)
                if pos[0] >= 450 and pos[0] <= 650 and pos[1] >= 650 and pos[1] <= 750:
                    Loading = Options.menu(board, gold, upgrades, Stats)
                    if Loading == "Load":
                        SaveFile = open("Save File/SaveFile.txt","r")
                        Data = SaveFile.readline().split()
                        count = 0
                        if Load != "New":
                            if len(Data) == 34:
                                gold = int(Data[count])
                                count += 1
                                board = [[0] * 3 for _ in range(3)]
                                for j in range(3):
                                    for i in range(3):
                                        board[j][i] = Tile([j,i],int(Data[count]))
                                        count += 1
                                for upgrade in upgrades:
                                    upgrade[0] = bool(Data[count])
                                    upgrade[1] = int(Data[count+1])
                                    count += 2
                #Exiting the popup box
                for button in PopupButton:
                    if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                        Popup = False

                        
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
                        Stats["Tiles"] += 1
                                
                            
            if event.type == pygame.MOUSEBUTTONUP:
                #Putting down the blocks
                for j in range(len(board)):
                    for i in range(len(board[0])):
                        if board[j][i] != 0:
                            if selected != []:
                                if pos[0] >= board[j][i].x and pos[0] <= board[j][i].x + board[j][i].width and pos[1] >= board[j][i].y and pos[1] <= board[j][i].y + board[j][i].height and board[j][i].drag == False and board[j][i].rank == board[selected[1]][selected[0]].rank:
                                    board[selected[1]][selected[0]] = Tile([selected[1],selected[0]], 0)
                                    board[j][i].rank += 1
                                    if 14 >= board[j][i].rank >= 3:
                                        upgrades[board[j][i].rank-3][0] = True
                                    board[j][i].color = rankup(board[j][i].rank % 12)
                                    
                                '''#Used to swap tiles(Currently Broken)
                                elif pos[0] >= board[j][i].x and pos[0] <= board[j][i].x + board[j][i].width and pos[1] >= board[j][i].y and pos[1] <= board[j][i].y + board[j][i].height and board[j][i].drag == True and board[j][i].rank != board[selected[1]][selected[0]].rank:
                                    board[j][i], board[selected[1]][selected[0]] = board[selected[1]][selected[0]], board[j][i]
                                    board[j][i].x, board[j][i].y = board[j][i].OldPos[0],board[j][i].OldPos[1]
                                    board[selected[1]][selected[0]].x, board[selected[1]][selected[0]].y = board[selected[1]][selected[0]].OldPos[0],board[selected[1]][selected[0]].OldPos[1]
                                    board[selected[1]][selected[0]].drag = False'''
                                
                                if 50 <= board[j][i].x <= 125 and 310 <= board[j][i].y <= 425:
                                    board[j][i] = Tile([i,j],0)
                                else:
                                    if [board[j][i].x,board[j][i].y] != board[j][i].OldPos:
                                        board[j][i].x, board[j][i].y = board[j][i].OldPos[0], board[j][i].OldPos[1]
                                
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
                        if 50 <= pos[0] <= 125 and 310 <= pos[1] <= 425:
                            pygame.draw.rect(gameDisplay,(150,150,150),(65,325,75,100),0)
                            pygame.draw.rect(gameDisplay,(100,100,100),(52,290,100,15),0)
                        else:
                            pygame.draw.rect(gameDisplay,(150,150,150),(65,325,75,100),0)
                            pygame.draw.rect(gameDisplay,(100,100,100),(52,310,100,15),0)
                            
                        
        #Drawing the selected tile over the other ones
        for j in range(len(board)):
            for i in range(len(board[0])):
                if board[j][i].drag == True:
                    board[j][i].update()


        #Shows the little loading thing to spawn in a box at the bottom
        pygame.draw.rect(gameDisplay,(150,130,42),(300,750-Fillup,100,Fillup),0)
        pygame.draw.rect(gameDisplay,(100,80,32),(300,650,100,100),5)
        if Fillup < 100:
            Fillup += 2

        #Calculating gold
        if GoldCooldown - time.process_time() <= 0:
            GoldCooldown = time.process_time()+1
            for row in board:
                for tile in row:
                    gold += 2**tile.rank - 1

        #Shop Buttons
        for button in Buttons:
            button.draw()

        #Drawing the popup thing to show gold made when your offline
        if Popup:
            pygame.draw.rect(gameDisplay,(0,150,150),(150,250,400,300),0)
            pygame.draw.rect(gameDisplay,(0,100,100),(150,250,400,300),5)
            for button in PopupButton:
                button.draw()
            Time = Change
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
            text_surface, rect = font_40.render("Time gone: " + str(TimeList[0]) + ":" + str(TimeList[1]) + ":" + str(TimeList[2]), (0, 0, 0))
            gameDisplay.blit(text_surface, (160, 350))
            text_surface, rect = font_35.render("Gold earned: " + shorten(gain), (0, 0, 0))
            gameDisplay.blit(text_surface, (270 - int(SizeCheck.size(shorten(gain))[0]), 400))
            pygame.draw.line(gameDisplay,(150,150,150),(489,272),(529,307),3)
            pygame.draw.line(gameDisplay,(150,150,150),(489,307),(529,272),3)
            


        #Automatically Saving the game every 10 seconds
        if SaveTime - time.process_time() <= 0:
            SaveTime = time.process_time() + 10
            DataList = []
            DataList.append(str(gold))
            for row in board:
                for tile in row:
                    DataList.append(str(tile.rank))
            for upgrade in upgrades:
                DataList.append(str(upgrade[0]))
                DataList.append(str(upgrade[1]))

            seconds = 0
            currentDT = datetime.datetime.now()
            seconds += currentDT.year * 31536000
            seconds += currentDT.month * 2592000
            seconds += currentDT.day * 86400
            seconds += currentDT.hour * 3600
            seconds += currentDT.minute * 60
            seconds += currentDT.second
            DataList.append(str(seconds))

            SaveFile = open("Save File/SaveFile.txt","w")
            SaveFile.write(" ".join(DataList))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    MainMenu.HomeScreen()
