import pygame
from settings import *

from tile import Tile
from player import Player

from debug import debug

class Level:
	def __init__(self):

		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortingCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE

				if col == 'x': Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
				if col == 'p': self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

	def run(self):
		self.visible_sprites.custom_drawing(self.player)
		self.visible_sprites.update()

class YSortingCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.mid_x = self.display_surface.get_size()[0] // 2
		self.mid_y = self.display_surface.get_size()[1] // 2

		self.offset = pygame.math.Vector2()

	def custom_drawing(self, player):

		self.offset.x = player.rect.centerx - self.mid_x
		self.offset.y = player.rect.centery - self.mid_y

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset

			self.display_surface.blit(sprite.image, offset_pos)