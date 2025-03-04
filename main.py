"""
Main module for the game.
"""

import sys
import os
import pygame

# Start
LEVEL = 0  # Changed to 0 to match the condition in main()

class Tiles:
    def __init__(self, tiles, tileset):
        self.tiles = tiles
        self.tileset = tileset

    @staticmethod
    def script(trigger, tile, code):
        print(f"Script {trigger} assigned to {code}")
        if trigger == 'onTouch':
            if tile == 'player':
                code()
        elif trigger == 'onDestroy':
            if tile == 'player':
                code()
        elif trigger == 'onUpdate':
            if tile == 'player':
                code()

    def draw(self, screen):
        tile_size = 100  # Assuming each tile is 100x100 pixels
        for row, tileset_row in enumerate(self.tileset):
            for col, tile_id in enumerate(tileset_row):
                if tile_id != 0:
                    tile_image = self.tiles[tile_id]
                    screen.blit(tile_image, (col * tile_size, row * tile_size))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.speed = 5
        self.sprite = self.load_image('resources/sprites/error.png')

    def load_image(self, path):
        try:
            base_path = os.path.dirname(__file__)
            return pygame.image.load(os.path.join(base_path, path))
        except (pygame.error, FileNotFoundError):
            base_path = os.path.dirname(__file__)
            return pygame.image.load(os.path.join(base_path, 'resources/sprites/error.png'))

    def update(self, keys, tileset):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and self.y_velocity == 0:
            self.y_velocity = self.jump_strength

        self.y_velocity += self.gravity
        self.y += self.y_velocity

        # Collision detection
        tile_size = 100  # Assuming each tile is 100x100 pixels
        for row, tileset_row in enumerate(tileset):
            for col, tile_id in enumerate(tileset_row):
                if tile_id != 0:
                    tile_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                    player_rect = pygame.Rect(self.x, self.y, tile_size, tile_size)
                    if player_rect.colliderect(tile_rect):
                        if self.y_velocity > 0:  # Falling
                            self.y = tile_rect.top - tile_size
                            self.y_velocity = 0
                        elif self.y_velocity < 0:  # Jumping
                            self.y = tile_rect.bottom
                            self.y_velocity = 0
                        if keys[pygame.K_LEFT]:
                            self.x = tile_rect.right
                        if keys[pygame.K_RIGHT]:
                            self.x = tile_rect.left - tile_size

    def draw(self, screen):
        print(f"Drawing player at {self.x}, {self.y}")
        screen.blit(self.sprite, (self.x, self.y))

    def kill(self):
        global LEVEL
        LEVEL = 'gameover'
        print("Player killed, game over")

class Enemy:
    def __init__(self):
        self.enemies = {
            0: pygame.Rect(50, 50, 100, 100),
            1: self.load_image('resources/sprites/enemy/enemy1.png')
        }

    def load_image(self, path):
        try:
            base_path = os.path.dirname(__file__)
            return pygame.image.load(os.path.join(base_path, path))
        except (pygame.error, FileNotFoundError):
            base_path = os.path.dirname(__file__)
            return pygame.image.load(os.path.join(base_path, 'resources/sprites/error.png'))

    def draw(self, screen, enemy_id, x, y):
        print(f"Drawing enemy {enemy_id} at {x}, {y}")
        if enemy_id in self.enemies and isinstance(self.enemies[enemy_id], pygame.Surface):
            screen.blit(self.enemies[enemy_id], (x, y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.enemies[0])

    def destroy(self, enemy_id):
        if enemy_id != 'all':
            print(f"Enemy {enemy_id} destroyed")
        else:
            print("All enemies destroyed")

class Room:
    @staticmethod
    def goto(room_id):
        print(f"Going to room {room_id}")

class Script:
    @staticmethod
    def tile(tile_id, loop, code):
        print(f"tile {tile_id} assigned to {code}")
        if loop == '*':
            loop = True
            while loop:
                code()
        else:
            for _ in range(loop):
                code()

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player = Player(50, 50)
    enemy = Enemy()
    tileset = []

    if LEVEL == 0:
        tiles = {
            1: pygame.image.load('resources/tiles/grass.png'),
            2: pygame.image.load('resources/tiles/dirt.png')
        }
        tileset = [
            [0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

    if LEVEL == 1:
        tileset = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

        tiles.script('onTouch', 'player', player.kill)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        player.update(keys, tileset)
        screen.fill((0, 0, 0))  # Clear screen
        player.draw(screen)
        enemy.draw(screen, 1, 100, 100)  # Example of drawing an enemy
        pygame.display.flip()
        clock.tick(60)
    sys.exit()

if __name__ == "__main__":
    main()