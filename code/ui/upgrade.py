import pygame

from misc.settings import *

class Upgrade:
	def __init__(self, player):
		self.display_surface = pygame.display.get_surface()
		self.player = player

		self.attribute_nr = len(player.stats)
		self.attribute_names = list(player.stats.keys())
		self.max_values = list(player.max_stats.values())

		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		self.height = self.display_surface.get_size()[1] * 0.8
		self.width = self.display_surface.get_size()[0] // 7 - 20
		self.create_items()

		self.selection_index = 0
		self.selection_time = None
		self.can_move = True

		self.pause_selection_index = 0
		self.pause_selected = True

	def input(self):
		keys = pygame.key.get_pressed()

		if self.can_move:
			if keys[pygame.K_d] and self.selection_index < self.attribute_nr:
				self.selection_index += 1
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()
			elif keys[pygame.K_a] and self.selection_index > 0:
				self.selection_index -= 1
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()
			
			if self.pause_selected:
				if keys[pygame.K_w] and self.pause_selection_index > 0:
					self.pause_selection_index -= 1
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()
				elif keys[pygame.K_s] and self.pause_selection_index < 1:
					self.pause_selection_index += 1
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()
					
				self.pause_screen.move(self.pause_selection_index)
				
			if keys[pygame.K_SPACE]:
				if self.selection_index != 0:
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()
					self.item_list[self.selection_index].trigger(self.player)
				else:
					if self.pause_selection_index == 0:
						self.can_move = False
						self.selection_time = pygame.time.get_ticks()
						self.game.toggle()
					else:
						self.can_move = False
						self.selection_time = pygame.time.get_ticks()

						self.game.open_main_menu()

	def cooldown(self):
		if not self.can_move:
			current_time = pygame.time.get_ticks()

			if current_time - self.selection_time >= 300:
				self.can_move = True

	def create_items(self):
		self.item_list = list()

		for item, index in enumerate(range(self.attribute_nr + 1)):
			full_width = self.display_surface.get_size()[0]
			increment = full_width // 6

			left = (item * increment) + (increment - self.width)
			top = self.display_surface.get_size()[1] * 0.1

			if index == 0:
				self.pause_screen = PauseScreen(0, 0, self.width + 75, HEIGTH, index, self.font)
				self.item_list.append(self.pause_screen)
			else:
				item = Item(left, top, self.width, self.height, index, self.font)
				self.item_list.append(item)

	def display(self, game):
		self.game = game

		self.input()
		self.cooldown()

		self.pause_screen.display(self.display_surface, self.selection_index, 'Paused')

		for index, item in enumerate(self.item_list):
			if index == 0: continue

			name = self.attribute_names[index-1]
			value = self.player.get_value_by_index(index-1)
			max_value = self.max_values[index-1]
			cost = self.player.get_cost_by_index(index-1)

			item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

		if self.selection_index == 0: self.pause_selected = True
		else: self.pause_selected = False

class PauseScreen():
	def __init__(self, l, t, w, h, index, font):
		self.rect = pygame.Rect(l, t, w, h)
		self.index = index
		self.font = font

		self.selected_index = 0

		self.selected = True
		
	def move(self, index):
		self.selected_index = index

	def display_name(self, surface, name, selected):
		colour = TEXT_COLOUR_SELECTED if selected else TEXT_COLOUR

		# title
		title_surf = self.font.render(name, False, colour)
		title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

		# draw
		surface.blit(title_surf, title_rect)

	def draw_content(self, surface):
		self.draw_text('Continue Game', surface, 120, 0)
		self.draw_text('Quit Game', surface, 30, 0)

	def draw_text(self, text, surface, move_value_y, move_value_x):
		font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
		colour = TEXT_COLOUR_SELECTED if self.selected else TEXT_COLOUR

		text_surface = font.render(text, False, colour)
		text_rect = text_surface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(move_value_x, move_value_y))

		surface.blit(text_surface, text_rect)

	def draw_cursor(self, surface):
		self.draw_text('*', surface, 120 if self.selected_index == 0 else 30, 105)

	def display(self, surface, selection_number, name):
		if self.index == selection_number:
			self.selected = True

			pygame.draw.rect(surface, UPGRADE_BG_COLOUR_SELECTED, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)
		else:
			self.selected = False

			pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)

		self.draw_content(surface)
		self.display_name(surface, name, self.index == selection_number)

		self.draw_cursor(surface)

class Item:
	def __init__(self, l, t, w, h, index, font):
		self.rect = pygame.Rect(l, t, w, h)
		self.index = index
		self.font = font

	def display_names(self, surface, name, cost, selected):
		colour = TEXT_COLOUR_SELECTED if selected else TEXT_COLOUR

		# title
		title_surf = self.font.render(name, False, colour)
		title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

		# cost
		cost_surf = self.font.render(str(int(cost)), False, colour)
		cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))

		# draw
		surface.blit(title_surf, title_rect)
		surface.blit(cost_surf, cost_rect)

	def display_bar(self, surface, value, max_value, selected):
		top = self.rect.midtop + pygame.math.Vector2(0, 60)
		bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
		colour = BAR_COLOUR_SELECTED if selected else BAR_COLOUR

		full_height = bottom[1] - top[1]
		relative_number = (value / max_value) * full_height
		value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

		pygame.draw.line(surface, colour, top, bottom, 5)
		pygame.draw.rect(surface, colour, value_rect)

	def trigger(self, player):
		upgrade_attr = list(player.stats.keys())[self.index - 1]

		if player.exp >= player.upgrades_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
			player.exp -= player.upgrades_cost[upgrade_attr]
			player.stats[upgrade_attr] *= 1.2
			player.upgrades_cost[upgrade_attr] *= 1.4

		if player.stats[upgrade_attr] > player.max_stats[upgrade_attr]:
			player.stats[upgrade_attr] = player.max_stats[upgrade_attr]

	def display(self, surface, selection_number, name, value, max_value, cost):
		if self.index == selection_number:
			pygame.draw.rect(surface, UPGRADE_BG_COLOUR_SELECTED, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)
		else:
			pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)

		self.display_names(surface, name, cost, self.index == selection_number)
		self.display_bar(surface, value, max_value, self.index == selection_number)