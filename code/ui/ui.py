import pygame

from misc.settings import *

class UI:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		self.health_bar_rect = pygame.Rect(25, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10, 40, ENERGY_BAR_WIDTH, BAR_HEIGHT)

		self.weapon_graphics = self.load_graphics(weapon_data.values())
		self.magic_graphics = self.load_graphics(magic_data.values())

		self.full_heart = pygame.image.load('../graphics/hearts/heart_full.png').convert_alpha()
		self.empty_heart = pygame.image.load('../graphics/hearts/heart_empty.png').convert_alpha()

	def load_graphics(self, values):
		result = list()

		for element in values:
			path = element['graphic']
			element = pygame.image.load(path).convert_alpha()

			result.append(element)

		return result

	def show_bar(self, current, max_amount, bg_rect, colour):
		pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)

		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		pygame.draw.rect(self.display_surface, colour, current_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)

	def show_exp(self, exp):
		text_surf = self.font.render('EXP: ' + str(int(exp)), False, TEXT_COLOUR)

		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x, y))

		pygame.draw.rect(self.display_surface, UI_BG_COLOUR, text_rect.inflate(20, 20))
		self.display_surface.blit(text_surf, text_rect)
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, text_rect.inflate(20, 20), 3)

	def full_hearts(self, max_amount, bg_rect):
		offset = 0

		for heart in range(int(max_amount) // 10):
			heart_surf = self.full_heart
			heart_surf = pygame.transform.scale(heart_surf, (30, 30))
			heart_rect = heart_surf.get_rect(center = bg_rect.midleft + pygame.math.Vector2(offset, 0))
			offset += 35

			self.display_surface.blit(heart_surf, heart_rect)

	def empty_hearts(self, max_amount, current, bg_rect):
		offset = 0

		for heart in range(int(max_amount) // 10):
			if heart < int(current) // 10:
				heart_surf = self.full_heart
			else:
				heart_surf = self.empty_heart

			heart_surf = pygame.transform.scale(heart_surf, (30, 30))
			heart_rect = heart_surf.get_rect(center = bg_rect.midleft + pygame.math.Vector2(offset, 0))
			offset += 35

			self.display_surface.blit(heart_surf, heart_rect)

	def selection_box(self, left, top, has_switched):
		bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)

		pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)

		if has_switched: pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_ACTIVE, bg_rect, 3)
		else: pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)

		return bg_rect

	def weapon_overlay(self, weapon_index, has_switched):
		bg_rect = self.selection_box(10, 100, has_switched)

		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf, weapon_rect)

	def magic_overlay(self, magic_index, has_switched):
		bg_rect = self.selection_box(10, 180, has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(magic_surf, magic_rect)

	def display(self, player):
		self.full_hearts(player.health, self.health_bar_rect)
		self.empty_hearts(player.stats['health'], player.health, self.health_bar_rect)

		self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOUR)

		self.show_exp(player.exp)

		self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
		self.magic_overlay(player.magic_index, not player.can_switch_magic)