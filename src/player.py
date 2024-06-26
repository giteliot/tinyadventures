import pygame 
from src.utils import distance

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, action_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('./graphics/player.png')
		self.rect = self.image.get_rect(topleft = pos)
		# self.hitbox = self.rect.inflate(-26, 0)
		self.hitbox = self.rect
		self.direction = pygame.math.Vector2()
		self.speed = 10

		self.obstacle_sprites = obstacle_sprites
		self.action_sprites = action_sprites

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_a]:
			self.direction.x = -1
		elif keys[pygame.K_d]:
			self.direction.x = 1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.move(self.speed)

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		self.action_interactions()

	def action_interactions(self):
		for sprite in self.action_sprites:
			if distance(sprite.hitbox, self.hitbox) > 70:
				sprite.leave()
			else:
				sprite.interact()

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom