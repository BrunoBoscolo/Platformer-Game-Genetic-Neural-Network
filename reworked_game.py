#Imports
import pygame
from pygame.locals import *
import random
import network
import sys

#Entity classes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Generate a random color for the player's surface
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surf = pygame.Surface((30, 30))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def force_moviment(self, direction):
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

    def force_jump(self, force):
        """
        Applies a force to the player sprite, causing it to jump with the specified force.

        Args:
            force (float): The force of the jump.
        """
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -force       
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                        # Update the corresponding score in the scores list
                        scores[players.index(self)] = self.score

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

#Simulation Control Classes

class simulation_setup:

    def create_bottom_platform():
        global all_sprites, platforms
        #Sets up the platform
        PT1 = platform()
        PT1.surf = pygame.Surface((WIDTH, 20))
        PT1.surf.fill((255,0,0))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 20))

        
        #include it in sprite groups
        all_sprites = pygame.sprite.Group()
        all_sprites.add(PT1)

        platforms = pygame.sprite.Group()
        platforms.add(PT1)

    def plat_gen():
        global all_sprites, platforms
        while len(platforms) < 12:
            width = random.randint(60, 80)
            p = platform()
            p.rect.center = (random.randint(0, WIDTH - width), random.randint(0, HEIGHT - 30))
            
            platforms.add(p)
            all_sprites.add(p)

    def create_players(num_players):
        players = []
        scores = [0]*num_players

        for _ in range(num_players):
            player = Player()
            all_sprites.add(player)
            players.append(player)

        return players, scores

    def create_first_player_generation(num_players):
        players, scores = simulation_setup.create_players(num_players)

        for player in players:
                    square_neural_network = network.RandomNeuralNetwork()
                    player_network_list.append(square_neural_network)

        return players, scores

    #Note: Probably useless
    def delete_players(players_list):
        for player in players_list:
            all_sprites.remove(player)
        del players_list[:]


class simulation_data:

    def print_high_score(scores):
        highest_score = max(scores)
        highest_score_index = scores.index(highest_score)
        print(f"High Score: {highest_score}, achieved by player {highest_score_index}")
        return highest_score

    def find_player_with_highest_score(players):
        highest_score = max(player.score for player in players)
        players_with_highest_score = [player for player in players if player.score == highest_score]

        if highest_score == 0:
            return None
        elif len(players_with_highest_score) !=1:
            return None
        else:
            return players_with_highest_score[0]
        
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
    

class network_usage:
    
    def compute_moviment(target, randomNetwork, player_x, player_y, closest_platform_x, closest_platform_y):
        input = [player_x, player_y, closest_platform_x, closest_platform_y]
        #print(f'input: {input}')
        output = randomNetwork.forward(input)
        #print(f'output: {output}')
        target.force_jump(abs(output[0]/10))
        target.force_moviment(output[1]/10)

    def network_moviments():
        i = 0
        for player in players:
                sq_x = int(player.pos.x)
                sq_y = int(player.pos.y)
                closest_platform = simulation_data.get_closest_platform(player, platforms)

                if closest_platform:
                    closest_platform_x = closest_platform.rect.centerx
                    closest_platform_y = closest_platform.rect.centery

                    #print('COMPUTING FUCKING SQUARE MOVIMENT ')
                    network_usage.compute_moviment(player, player_network_list[i], sq_x, sq_y, closest_platform_x, closest_platform_y)
                
                i += 1 

                player.update()
                displaysurface.blit(player.surf, player.rect)

    def create_new_generation(player_network_list, scores):
        player_scores = [[player_network_list[i], scores[i]] for i in range(len(players))]
            
        sorted_networks = network.Evolution.select_top_half(player_scores)
        
        new_generation = network.genetics.mutate_network_parameters(sorted_networks)
        
        new_generation = new_generation+new_generation

        return new_generation

if __name__ == '__main__':

    #Pygame iniciator
    pygame.init()
    vec = pygame.math.Vector2 #2 for two dimensional

    #Simulation Parameters

    HEIGHT = 800
    WIDTH = 400
    ACC = 0.5
    FRIC = -0.12
    FPS = 60

    num_players = 50
    max_cicles = 12
    fps_network = 30

    #Sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Counters

    cicle = 0
    frame_count = 0
    player_count = 0
    generation_count = 0
    highest_score = 0

    #lists

    scores = []
    print("Score reseted")
    players = []
    player_network_list = []

    #Simulation settings

    FramePerSec = pygame.time.Clock()
    
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")


    simulation_setup.create_bottom_platform()
    simulation_setup.plat_gen()

    players, scores = simulation_setup.create_first_player_generation(num_players)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.quit()
                    sys.exit()

        for player in players:
            player.update()

        displaysurface.fill((0,0,0))
        f = pygame.font.SysFont("Verdana", 20)
        g  = f.render(f'Generation: {generation_count} Highest Score: {highest_score}', True, (123,255,0))   ##
        displaysurface.blit(g, (10, 10))
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        if frame_count == 30 and cicle <=(max_cicles-1):

            network_usage.network_moviments()
            frame_count = 0
            cicle += 1

        else:
            frame_count += 1
            
            player.update()
            displaysurface.blit(player.surf, player.rect)

        if cicle == max_cicles:
            
            new_generation = network_usage.create_new_generation(player_network_list, scores)
            
            highest_score = simulation_data.print_high_score(scores)
            
            players, scores = simulation_setup.create_players(num_players)

            player_network_list = new_generation
            
            cicle = 0
            generation_count += 1

        #print(scores)
        pygame.display.update()
        FramePerSec.tick(30)

 
