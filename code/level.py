import pygame
from settings import *

from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI

from random import choice

from support import *
from debug import debug

class Level:
	def __init__(self):

		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortingCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.current_attack = None

		self.create_map()

		self.ui = UI()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_LargeObjects.csv'),
		}

		graphics = {
			'grass': import_folder('../graphics/grass'),
			'objects': import_folder('../graphics/objects'),
		}

		for style, layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILE_SIZE
						y = row_index * TILE_SIZE

						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invinsible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)


		self.player = Player((2000, 1350), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()

		self.current_attack = None

	def run(self):
		self.visible_sprites.custom_drawing(self.player)
		self.visible_sprites.update()

		self.ui.display(self.player)

class YSortingCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.mid_x = self.display_surface.get_size()[0] // 2
		self.mid_y = self.display_surface.get_size()[1] // 2

		self.offset = pygame.math.Vector2()

		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

	def custom_drawing(self, player):

		self.offset.x = player.rect.centerx - self.mid_x
		self.offset.y = player.rect.centery - self.mid_y

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset

			self.display_surface.blit(sprite.image, offset_pos)