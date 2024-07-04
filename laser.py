import pygame

class Laser():
    def __init__(self,x,y,image):
        self.x = x
        self.y = y 
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, velocity):
        self.y -= velocity
        
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        
    def collision (self, obj):
        return collide(obj, self)
             
#obj1 ve obj2 nesnelerinin çarpışıp çarpışmadığını kontrol eder.
#Eğer çarpışma gerçekleşiyorsa,True değerini döndürür. 
#Eğer çarpışma gerçekleşmiyorsa veya maskelerin örtüşme işlevi tanımlanmamışsa, False değerini döndürür.
def collide(obj1 , obj2):
    offsetx = obj2.x - obj1.x
    offsety = obj2.y - obj1.y    
    return obj1.mask.overlap(obj2.mask, (offsetx, offsety)) != None
    
