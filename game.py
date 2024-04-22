import pygame
from pygame.locals import *
import sys
import random
import network
import moviment

pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0

    def force_moviment(self, space, direction):
        self.acc = vec(0,0.5)
        self.acc.x = direction

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
     
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1

                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.point = True
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
 
    def move(self):
        pass
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
def get_closest_platform(player, platforms):
    closest_platform = None
    closest_distance = float('inf')  # Initialize with infinity

    for platform in platforms:
        distance = ((platform.rect.centerx - player.rect.centerx) ** 2 +
                    (platform.rect.centery - player.rect.centery) ** 2) ** 0.5
        
        if distance < closest_distance:
            closest_platform = platform
            closest_distance = distance

    return closest_platform

PT1 = platform()
P1 = Player()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)
 
for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
randomNetwork = network.RandomNeuralNetwork()
count = 0

def compute_moviment(player_x, player_y, closest_platform_x, closest_platform_y):

    input = [player_x, player_y, closest_platform_x, closest_platform_y]
    print(input)
    output = randomNetwork.forward(input)
    print(output)
    moviment.press_keys(output[0]*10, output[1]*10)

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()  
 
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
 
    plat_gen()
    displaysurface.fill((0,0,0))

    displaysurface.fill((0,0,0))
    f = pygame.font.SysFont("Verdana", 20)     ##
    g  = f.render(str(P1.score), True, (123,255,0))   ##
    displaysurface.blit(g, (WIDTH/2, 10))   ##
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
    
    player_x = int(P1.pos.x)
    player_y = int(P1.pos.y)

    closest_platform = get_closest_platform(P1, platforms)

    if closest_platform:
        closest_platform_x = closest_platform.rect.centerx
        closest_platform_y = closest_platform.rect.centery

    
    print(count)
    if count == 30:
        print('COMPUTING FUCKING MOVIMENT ')
        compute_moviment(player_x, player_y, closest_platform_x, closest_platform_y)
        count = 0
    
    else:
        count += 1

    pygame.display.update()
    FramePerSec.tick(30) 
