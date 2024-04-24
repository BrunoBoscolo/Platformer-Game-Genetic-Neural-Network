#Imports
import pygame
from pygame.locals import *
import random
import network
import sys

import matplotlib.pyplot as plt

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
        self.interacted_platforms = []
    
    def reset_interacted_platforms(self):
        self.interacted_platforms = []

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
        self.rect.midbottom = self.pos  # Update player position

        # Check collision with platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and self.vel.y > 0:
            for hit in hits:
                if self.pos.y < hit.rect.bottom:
                    self.pos.y = hit.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

            # Scores
            for hit in hits:
                if not hit.platform_id == 99:
                    collision_id = hit.platform_id
                    
                    if collision_id in self.interacted_platforms:
                        pass
                    else:
                        self.interacted_platforms.append(collision_id)
                        self.score += 1
                        scores[players.index(self)] = self.score
                    
                
class platform(pygame.sprite.Sprite):
    def __init__(self, platform_id):
        super().__init__()
        self.point = True
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))
        self.interacted = False  # Attribute to track if the platform has been interacted with
        self.platform_id = platform_id  # Unique ID for each platform
    
    def move(self):
        pass

#Simulation Control Classes

class simulation_setup:

    def update_entitys(players):
        for player in players:
            player.update()

    def create_bottom_platform():
        global all_sprites, platforms
        #Sets up the platform
        PT1 = platform(99)
        PT1.surf = pygame.Surface((WIDTH, 1000))
        PT1.surf.fill((255,0,0))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT + 490))

        
        #include it in sprite groups
        all_sprites = pygame.sprite.Group()
        all_sprites.add(PT1)

        platforms = pygame.sprite.Group()
        platforms.add(PT1)

    def plat_gen():
        global all_sprites, platforms
        platform_id = 0  # Initialize platform ID
        while len(platforms) < 12:
            last_x = 30
            last_y = 40
            width = random.randint(60, 80)
            p = platform(platform_id)  # Pass platform ID when creating the platform
            p.rect.center = (random.randint(last_x, WIDTH - width), random.randint(last_y, HEIGHT - 40))
            
            platforms.add(p)
            all_sprites.add(p)
            last_x += 30
            platform_id += 1  # Increment platform ID for the next platform

    def create_players(num_players):
        players = []
        scores = [0]*num_players

        for n in range(num_players):
            player = Player()
            all_sprites.add(player)
            players.append(player)

        return players, scores

    def create_first_player_generation(num_players):
        #players = simulation_setup.create_players(num_players)

        for n in range(num_players):
            #print(f'Network number: {n}')
            square_neural_network = network.RandomNeuralNetwork()
            player_network_list.append(square_neural_network)

        #print(f'Player Network \n {player_network_list}')
        return player_network_list

    #Note: Probably useless
    def delete_players(players_list):
        for player in players_list:
            all_sprites.remove(player)
        del players_list[:]

    def reset_players_position(players):
        for player in players:
            player.pos.x = 200  # Set horizontal position to the center of the screen
            player.pos.y = HEIGHT - 30  # Set vertical position 30 pixels from the bottom

class simulation_data:

    def create_graph(mean_scores):
        # Create an array of iteration numbers from 1 to the length of scores
        x_values = [point[0] for point in mean_scores]
        y_values = [point[1] for point in mean_scores]

        # Plot the scores
        plt.plot(x_values, y_values)


        # Add labels and title
        plt.xlabel('Iteration')
        plt.ylabel('Performance')
        plt.title('Simulation Scores')

        # Show the plot
        plt.show()

    def reset_score(scores, num_players):
        scores = [0]*num_players
        return scores

    def calculate_mean(scores):
        total_score = sum(scores)
        n_players = len(scores)

        if n_players == 0:
            return 0
        
        mean_score = total_score / n_players

        return mean_score

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
        target.force_jump(abs(output[0]/300))
        target.force_moviment(output[1]/300)

    def network_moviments(players):
        i = 0
        for player in players:
            sq_x = int(player.pos.x)
            sq_y = int(player.pos.y)
            closest_platform = simulation_data.get_closest_platform(player, platforms)

            if closest_platform:
                closest_platform_x = closest_platform.rect.centerx
                closest_platform_y = closest_platform.rect.centery

                #print('COMPUTING FUCKING SQUARE MOVIMENT ')
                network_usage.compute_moviment(player, player_network_list[players.index(player)], sq_x, sq_y, closest_platform_x, closest_platform_y)
            
            #i += 1 

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
    
    framerate = 30
    num_players = 1000
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
    scores = [0]*50
    print("Score reseted")
    
    global players, player_network_list

    players = []
    player_network_list = []

    #Simulation settings

    FramePerSec = pygame.time.Clock()
    
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")


    simulation_setup.create_bottom_platform()
    simulation_setup.plat_gen()
    
    players, scores =  simulation_setup.create_players(num_players)
    player_network_list = simulation_setup.create_first_player_generation(num_players)
    simulation_setup.reset_players_position(players)

    mean_scores = []

    while True:

        for player in players:
            player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.quit()
                    simulation_data.create_graph(mean_scores)
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    cicle = max_cicles
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    for player in players:
                        player.force_jump(abs(random.randint(10,100)))
                        player.force_moviment(abs(random.randint(10,100)))

        simulation_setup.update_entitys(players)

        displaysurface.fill((0,0,0))
        f = pygame.font.SysFont("Verdana", 15)
        g  = f.render(f'Generation: {generation_count} Highest Score: {highest_score} Gen. Mean: {simulation_data.calculate_mean(scores)}', True, (123,255,0))   ##
        displaysurface.blit(g, (10, 10))
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

            # Draw platform ID on screen
            if isinstance(entity, platform):  # Check if the entity is a platform
                platform_id_text = f.render(str(entity.platform_id), True, (255, 255, 255))  # Render platform ID
                platform_id_rect = platform_id_text.get_rect(center=entity.rect.center)  # Get rectangle for positioning
                displaysurface.blit(platform_id_text, platform_id_rect)  # Blit the platform ID text on the screen


        if frame_count == 30 and cicle <=(max_cicles-1):

            network_usage.network_moviments(players)
            frame_count = 0
            cicle += 1

        if cicle == max_cicles:

            '''print("STARTING DEBUIGGING")
            player_score_debug = 0
            for player in players:
                print(f'Player Index: {player_score_debug} SCORE = {player.score}')
                player_score_debug += 1
            print("END DEBUGGING")'''
            
            new_generation = network_usage.create_new_generation(player_network_list, scores)
            
            highest_score = simulation_data.print_high_score(scores)
            print(f'Valor médio de otimização da geração: {simulation_data.calculate_mean(scores)}')
            mean_scores.append([generation_count, simulation_data.calculate_mean(scores)])
            #print(mean_scores)
            scores = simulation_data.reset_score(scores, num_players)
            

            player_network_list = new_generation

            simulation_setup.reset_players_position(players)

            for player in players:
                player.score = 0
                player.reset_interacted_platforms()
            
            cicle = 0
            generation_count += 1

        frame_count += 1
        pygame.display.update()
        FramePerSec.tick(framerate)

 
