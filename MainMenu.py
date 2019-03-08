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
try:
    import main
except ImportError:
    print("Make sure you have the main file")
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
font_75 = pygame.freetype.Font("Font.ttf", 75)
font_50 = pygame.freetype.Font("Font.ttf", 30)
SizeCheck = pygame.font.Font(None, 30)

#Maybe the little mainscreen thing can be a cube combining together
#And then splitting apart going up the ranks as it goes

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
        gameDisplay.blit(text_surface, (self.x + int(self.width/2)+30 - int(SizeCheck.size(str(self.text))[0]), self.y + int(self.height/2) - 20))

def HomeScreen():
    game_run = True
    Colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,128),(0,255,255),
              (0,128,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127), (0,0,0)]
    Buttons = [Button(100,525,200,100,"New Game"),Button(400,525,200,100,"Continue"),Button(100,650,200,100,"Credits"),Button(400,650,200,100,"Options")]
    ExtraButtons = [Button(400,650,200,100,"Exit")]
    screen = "Main"
    rank = 1
    x =  100
    forward = True
    backward = False
    ColorChange = 0
    waitTime = 0.1

    while game_run == True:

        pos = pygame.mouse.get_pos()

        #Drawing Background and title screen
        gameDisplay.fill((0,200,200))

        if screen == "Main":
            text_surface, rect = font_75.render(("Merge Blocks"), (0, 0, 0))
            gameDisplay.blit(text_surface, (130, 100))
            for button in Buttons:
                button.draw()
        elif screen == "Credits":
            ExtraButtons[0].draw()
            text_surface, rect = font_50.render(("Programmer: 8BitToaster"), (0, 0, 0))
            gameDisplay.blit(text_surface, (170, 100))
            text_surface, rect = font_50.render(("Helper: INNERBOOST"), (0, 0, 0))
            gameDisplay.blit(text_surface, (200, 150))
            text_surface, rect = font_50.render(("Go Check out these channels:"), (0, 0, 0))
            gameDisplay.blit(text_surface, (150, 300))
            text_surface, rect = font_50.render(("The8BitToaster - The Main Programmer"), (0, 0, 0))
            gameDisplay.blit(text_surface, (75, 350))
            text_surface, rect = font_50.render(("ZJ Sketches - A Good Friend"), (0, 0, 0))
            gameDisplay.blit(text_surface, (170, 400))
        elif screen == "Options":
            ExtraButtons[0].draw()
            text_surface, rect = font_50.render(("Coming Soon"), (0, 0, 0))
            gameDisplay.blit(text_surface, (250, 300))
    
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen == "Main":
                    for button in Buttons:
                        if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                            if button.text == "New Game":
                                main.game_loop("New")
                            if button.text == "Continue":
                                main.game_loop("Continue")
                            if button.text == "Credits":
                                screen = "Credits"
                            if button.text == "Options":
                                screen = "Options"
                elif screen == "Credits" or screen == "Options":
                    for button in ExtraButtons:
                        if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
                            screen = "Main"


        #Drawing a cool little animation
        if forward:
            x += 5
            if x >= 300:
                forward = not forward
                waitTime = time.process_time() + 1
            pygame.draw.rect(gameDisplay,Colors[rank-1],(x,300,50,50),0)
            pygame.draw.rect(gameDisplay,Colors[rank-1],(600-x,300,50,50),0)
        if not forward and not backward:
            pygame.draw.rect(gameDisplay,Colors[rank],(275,275,100,100),0)
            if waitTime - time.process_time() <= 0:
                backward = True
        if backward:
            x -= 5
            pygame.draw.rect(gameDisplay,Colors[rank],(x,300,50,50),0)
            pygame.draw.rect(gameDisplay,Colors[rank],(600-x,300,50,50),0)
            if x <= 105:
                backward = not backward
                forward = True
                ColorChange = 0
                x = 100
                rank += 1
                rank %= 12
                waitTime = time.process_time() + 1

        
                

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    HomeScreen()
