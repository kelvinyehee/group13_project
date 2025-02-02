import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon

class Level:
    def __init__(self):
    
    	# get the display surface
    	self.display_surface = pygame.display.get_surface()

        # sprite group setup
    	self.visible_sprites = YSortCameraGroup()
    	self.obstacle_sprites = pygame.sprite.Group()
    	
    	#attack sprites
    	self.current_attack = None
    	
    	#sprite setup
    	self.create_map()
    	
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('/home/kyd/group13_project/cool/01_Block.csv'),
            '01': import_csv_layout('/home/kyd/group13_project/cool/01_配件.csv'),
            '02': import_csv_layout('/home/kyd/group13_project/cool/01_物件.csv')
            
        }
        graphics = {
            '01':import_folder('/home/kyd/group13_project/graphics/pic'),
            'ob':import_folder('/home/kyd/group13_project/graphics/pic')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == '01':
                            random_grass_image = choice(graphics['01'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'01',random_grass_image)    
                        if style == '02':
                            random_grass_image = choice(graphics['01'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'02',random_grass_image)
                        if style == 'ob': 
                            surf = graphics['ob'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'ob',surf)
                            
        self.player = Player((2000,1430),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)
                            
        

    def run(self):
        #update and draw the pygame
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #creating the floor
        floor_surf = pygame.image.load('/home/kyd/test/03.png').convert()
        self.floor_surf = pygame.transform.scale(floor_surf,(1280*4,800*4))
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        #for sprite in self.sprites()
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset 
            self.display_surface.blit(sprite.image,offset_pos)
            
