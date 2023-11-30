import pygame 
import random
from src.model.level_generator import LevelGenerator

class Npc(pygame.sprite.Sprite):
	def __init__(self, pos, groups, narrator, level_generator, name, type):
		super().__init__(groups)
		self.name = name
		self.image = pygame.image.load(f'./graphics/{type}.png')
		self.rect = self.image.get_rect(topleft = pos)
		# self.hitbox = self.rect.inflate(0, -10)
		self.hitbox = self.rect
		self.narrator = narrator
		self.level_generator = level_generator

		self.type = type
		self.name = name

		self.options = []
		self.text = ""
		self.narrator_intro = ""
		self.remaining_interactions = random.randint(1, 4)
		self.status = "NOT_SEEN" # NOT_SEEN, IDLE, ACTIVE, DONE
		self.processing = False

	def _make_next_interaction(self, is_opening, narrator_intro, user_choice):
		self.narrator_intro, self.options, is_done = self.level_generator.get_npc_message(
			self.type, is_opening, narrator_intro, user_choice, self.remaining_interactions
		)

		self.remaining_interactions -= 1
		self.processing = False
		if is_done:
			self.status = "DONE"
			self.narrator.text = self.narrator_intro
			return

		narrator_text = self.narrator_intro+" XXX "
		for i, option in enumerate(self.options):
			narrator_text += f"{i+1}. {option} XXX "
		self.narrator.text = narrator_text
		self.text = narrator_text
		self.status = "ACTIVE"

	def action(self):
		if self.status == "NOT_SEEN":
			self._make_next_interaction(True, "", "")

		elif self.status == "IDLE":
			self.narrator.text = self.text
			self.status = "ACTIVE"


	def leave(self):
		if self.status == "ACTIVE":
			self.status = "IDLE"
			self.narrator.text = "Our hero continues his journey"

	def interact(self):
		if self.status != "ACTIVE" or self.processing:
			return

		keys = pygame.key.get_pressed()
		for key in range(len(self.options)):
			if keys[key+49]:
				self.processing = True
				print(self.options[key])
				self._make_next_interaction(False, self.narrator_intro, self.options[key])
