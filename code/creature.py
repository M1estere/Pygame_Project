import pygame

class Creature(pygame.sprite.Sprite):
	def __init__(self, groups):
		super().__init__(groups)

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