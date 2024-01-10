import pygame
from src.settings import WIDTH, HEIGHT, TILESIZE, NARRATOR_HEIGHT, WORLD_MAP
from src.tile import Tile
from src.player import Player
from src.npc import Npc
from src.narrator import Narrator
from src.utils import get_free_tile
from src.model.game_master import GameMaster


class Level:
	def __init__(self):

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.action_sprites = pygame.sprite.Group()

		self.narrator = Narrator()
		
		self.game_master = GameMaster()

		self.create_map()
		self.run()
		
		self.narrator.set_text(self.game_master.get_intro_message())

	def create_map(self):
		for row_index, row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index*TILESIZE
				y = row_index*TILESIZE
				if col == 'x':
					Tile((x,y), [self.visible_sprites, self.obstacle_sprites])

		active_chars = ['p','l','d']
		current_wm = WORLD_MAP
		for c in active_chars:
			x,y,current_wm = get_free_tile(current_wm, c)
			x,y = x*TILESIZE,y*TILESIZE
			if c == 'p':
				self.player =  Player((x,y), [self.visible_sprites], self.obstacle_sprites, self.action_sprites)
			if c == 'l':
				Npc((x,y), [self.visible_sprites, self.obstacle_sprites, self.action_sprites], self.narrator, self.game_master, 'Genoveffa', 'lady')
			if c == 'd':
				Npc((x,y), [self.visible_sprites, self.obstacle_sprites, self.action_sprites], self.narrator, self.game_master, 'Charly', 'dog')

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.narrator.display()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface  = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height + NARRATOR_HEIGHT//2

		for sprite in sorted(self.sprites(),key= lambda s : s.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

		


