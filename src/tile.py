import pygame 

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load('./graphics/rock.png')
		self.rect = self.image.get_rect(topleft = pos)
		# self.hitbox = self.rect.inflate(0, -10)
		self.hitbox = self.rect