Class documentation:

# Square Sprite

A class representing a square sprite that can be moved programmatically.

## Overview

This class provides functionality to create a square sprite in a Pygame environment. The square can be moved programmatically by applying forces to it.

## Installation

No installation is required. Simply copy the `Square` class into your Pygame project.

## Usage

```python
import pygame
from pygame.math import Vector2

class Square(pygame.sprite.Sprite):
    """
    A class representing a square sprite that can be moved programmatically.
    
    Attributes:
        surf (pygame.Surface): The surface representing the square.
        rect (pygame.Rect): The rectangular area that encompasses the square.
        pos (pygame.math.Vector2): The position vector of the square.
        vel (pygame.math.Vector2): The velocity vector of the square.
        acc (pygame.math.Vector2): The acceleration vector of the square.
    
    Methods:
        __init__(self, pos_x, pos_y):
            Initializes the Square object with the specified position.
        
        force_movement(self, force_x, force_y):
            Applies a force to the square, adjusting its acceleration accordingly.
        
        update(self):
            Updates the position of the square based on its velocity and acceleration.
    """
    def __init__(self, pos_x, pos_y):
        """
        Initializes the Square object with the specified position.
        
        Args:
            pos_x (int): The x-coordinate of the initial position.
            pos_y (int): The y-coordinate of the initial position.
        """
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 0, 0))  # Red color for the square
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))

        self.pos = Vector2(pos_x, pos_y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def force_movement(self, force_x, force_y):
        """
        Applies a force to the square, adjusting its acceleration accordingly.
        
        Args:
            force_x (float): The force to be applied along the x-axis.
            force_y (float): The force to be applied along the y-axis.
        """
        self.acc.x += force_x
        self.acc.y += force_y

    def update(self):
        """
        Updates the position of the square based on its velocity and acceleration.
        """
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        self.acc *= 0  # Reset acceleration for the next frame

# Player Sprite

A class representing a player sprite that can move and jump in a Pygame environment.

## Overview

This class provides functionality to create a player sprite in a Pygame environment. The player can move left, right, and jump within the game world.

## Installation

No installation is required. Simply copy the `Player` class into your Pygame project.

## Usage

```python
import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    """
    A class representing a player sprite that can move and jump.
    
    Attributes:
        surf (pygame.Surface): The surface representing the player sprite.
        rect (pygame.Rect): The rectangular area that encompasses the player sprite.
        pos (pygame.math.Vector2): The position vector of the player sprite.
        vel (pygame.math.Vector2): The velocity vector of the player sprite.
        acc (pygame.math.Vector2): The acceleration vector of the player sprite.
        jumping (bool): Indicates whether the player is currently jumping.
        score (int): The score accumulated by the player.
    
    Methods:
        __init__(self):
            Initializes the Player object.
        
        move(self):
            Updates the position of the player based on user input.
        
        jump(self):
            Causes the player to jump.
        
        cancel_jump(self):
            Cancels the player's jump if it is still rising.
        
        update(self):
            Updates the position and state of the player sprite.
    """
    def __init__(self):
        """
        Initializes the Player object.
        """
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 0))  # Yellow color for the player sprite
        self.rect = self.surf.get_rect()
   
        self.pos = Vector2(10, 360)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        """
        Updates the position of the player based on user input.
        """
        self.acc = Vector2(0, 0.5)
    
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
        """
        Causes the player to jump.
        """
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        """
        Cancels the player's jump if it is still rising.
        """
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        """
        Updates the position and state of the player sprite.
        """
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1

                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

# Platform Sprite

A class representing a platform sprite in a Pygame environment.

## Overview

This class provides functionality to create a platform sprite in a Pygame environment. Platforms are static objects that can serve as surfaces for the player sprite to stand on.

## Installation

No installation is required. Simply copy the `Platform` class into your Pygame project.

## Usage

```python
import pygame
import random

class Platform(pygame.sprite.Sprite):
    """
    A class representing a platform sprite.
    
    Attributes:
        surf (pygame.Surface): The surface representing the platform.
        rect (pygame.Rect): The rectangular area that encompasses the platform.
        point (bool): Indicates whether the platform awards points when landed on.
    
    Methods:
        __init__(self):
            Initializes the Platform object.
        
        move(self):
            Moves the platform (not implemented in this class).
    """
    def __init__(self):
        """
        Initializes the Platform object.
        """
        super().__init__()
        self.point = True
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))  # Green color for the platform
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))

    def move(self):
        """
        Moves the platform (not implemented in this class).
        """
        pass
