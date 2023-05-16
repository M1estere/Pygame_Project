import pygame
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacles):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		self.hitbox = self.rect.inflate(0, -26)

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacles = obstacles

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]: self.direction.y = -1
		elif keys[pygame.K_DOWN]: self.direction.y = 1
		else: self.direction.y = 0

		if keys[pygame.K_RIGHT]: self.direction.x = 1
		elif keys[pygame.K_LEFT]: self.direction.x = -1
		else: self.direction.x = 0

	def movement(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collisions('horizontal')

		self.hitbox.y += self.direction.y * speed
		self.collisions('vertical')

		self.rect.center = self.hitbox.center

	def collisions(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacles:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left # right
					if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right # left

		if direction == 'vertical':
			for sprite in self.obstacles:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top # down
					if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom # up

	def update(self):
		self.input()
		self.movement(self.speed)