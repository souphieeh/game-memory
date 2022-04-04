from lib2to3.pgen2.token import GREATER
from string import whitespace
import pygame, cv2, random, os
from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,filename,x,y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('images/aliens/' + filename)

        self.back_image = pygame.image.load('images/aliens/' + filename)
        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft = (x,y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False


class Game():
    def __init__(self):
        self.level = 6
        self.level_complete = False

        #aliens
        self.all_aliens = [f for f in os.listdir('images/aliens') if os.path.join('images/aliens',f)]

        self.img_width, self.image_height = (128,128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        # flipping and timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate level
        self.generate_level(self.level)

        self.title_font = pygame.font.SysFont(None, 44)
        self.title_text = self.title_font.render('Memory Game',True, WHITE)
        self.title_rect = self.title_text.get_rect(midtop = (WINDOW_WIDTH // 2, 10))

    def update(self, event_list):
        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self,event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else: 
                                            self.level_complete + False
                                            break
        else: 
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []


    def generate_level(self, level):
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self,aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        tiles = []
        self.tiles_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARGIN + (self.img_width + self.padding) * (i % self.cols)
            y = self.margin_top + (i // self.rows * (self.image_height + self.padding))
            tile = Tile(aliens[i], x, y)
            self.tiles_group.add(tile)


    def select_random_aliens(self, level):
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens



    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.title_rect.collidepoint(pygame.mouse.get_pos()):
                    self.title_text = self.title_font.render('Memory Game',True, RED)


    def draw(self):
        screen.fill(DARKBLUE)
        content_font = pygame.font.SysFont(None, 24)
        

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop = (50,50))

        screen.blit(self.title_text,self.title_rect)
        screen.blit(level_text,level_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

pygame.init()


screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Memory Game')

clock = pygame.time.Clock()

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
    
    game.update(event_list)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()