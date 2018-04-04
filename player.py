import pygame
class Player(pygame.sprite.Sprite):
   
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = self.getImage()
        self.rect = self.image.get_rect()

        self.speed = PLAYERSPEED
    
    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
            self.checkForSide()
    def moveLeft(self):
        self.rect .x -= -1 * self.speed            
        self.checkForSide()

    def moveRight(self):
        self.rect.x += 1 * self.speed    
        self.checkForSide()

    def checkForSide(self):
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
            
        elif self.rect.left < 0:
            self.rect.left = 0
    def getImage(self):
        image = pygame.image.load('spaceship.png') 
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image