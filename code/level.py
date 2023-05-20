import pygame

from misc.settings import *
from misc.support import *

from entities.player import Player
from entities.enemy import Enemy

from low_classes.tile import Tile
from low_classes.particles import AnimationPlayer

from low_classes.weapon import Weapon
from low_classes.magic import MagicPlayer

from ui.ui import UI
from ui.pause import Pause

from random import choice, randint

class Level:
	def __init__(self):
		self.game_paused = False

		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortingCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.current_attack = None

		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		self.create_map()

		self.ui = UI()
		self.pause = Pause(self.player)

		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_LargeObjects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv'),
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
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
						if style == 'entities':
							if col == '394':
								self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
							else:
								if col == '390': name = 'bamboo'
								elif col == '391': name = 'spirit'
								elif col == '392': name = 'raccoon'
								else: name = 'squid'

								Enemy(name, (x, y), [self.visible_sprites, self.attackable_sprites], 
									self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_experience_points)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()

		self.current_attack = None

	def create_magic(self, style, strength, cost):
		if style == 'heal':
			self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

		if style == 'flame':
			self.magic_player.fire(self.player, cost, [self.visible_sprites, self.attack_sprites])

	def attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0, 45)

							for leaf in range(randint(6, 9)):
								self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player, attack_sprite.sprite_type)

	def trigger_death_particles(self, pos, particles_type):
		self.animation_player.create_particles(particles_type, pos, [self.visible_sprites])

	def add_experience_points(self, amount):
		self.player.exp += amount

	def damage_player(self, damage_value, attack_type):
		if self.player.can_take_damage:
			self.player.health -= damage_value
			self.player.can_take_damage = False

			self.player.hurt_time = pygame.time.get_ticks()

			self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

	def toggle_menu(self, game):
		self.game_paused = not self.game_paused
		self.game = game

	def run(self):
		self.visible_sprites.custom_drawing(self.player)
		self.ui.display(self.player)

		if self.game_paused:
			self.pause.display(self.game)
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.attack_logic()

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

	def enemy_update(self, player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)