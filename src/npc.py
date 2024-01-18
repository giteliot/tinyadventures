import pygame 
import random
from src.model.brain import Brain

class Npc(pygame.sprite.Sprite):
	def __init__(self, pos, groups, narrator, game_master, name, type):
		super().__init__(groups)
		self.name = name
		self.image = pygame.image.load(f'./graphics/{type}.png')
		self.rect = self.image.get_rect(topleft = pos)

		self.hitbox = self.rect
		self.narrator = narrator
		self.game_master = game_master
		self.brain = Brain(game_master.get_npc_prompt(type))

		self.type = type
		self.name = name

		self.user_options = []
		self.last_message = ""

		self.status = "NOT_SEEN" # NOT_SEEN, IDLE, ACTIVE, DONE
		self.processing = False

	def _make_user_interaction(self):
		npc_message = self.last_message
		user_options = self.game_master.get_interaction_outcome(npc_message, self.type)

		self.user_options = user_options['options']
		#TODO update history on user choice

		for k, opt in enumerate(user_options['options']):
			npc_message += f"\n{k+1}: {opt['option_text']}"
		self.narrator.set_text(npc_message)


	def _make_npc_interaction(self, user_choice):
		if user_choice is None:
			user_text = "who are you? what are you doing here?"
		else:
			user_text = user_choice['option_text']
			# here I should take action if game is over or npc is dead
			if user_choice['is_game_over_win'] == True or user_choice['is_game_over_loss'] == True:
				print(f"GAME OVER DIO CAN;")
			if user_choice['is_npc_done'] == True:
				print(f"KILL THE MF; {user_choice['is_npc_done']}")

		npc_message = self.brain.interact(user_text)

		self.game_master.update_history(user_text, self.type, npc_message)

		self.narrator.set_text(npc_message)
		self.last_message = npc_message

		self._make_user_interaction()


	def leave(self):
		if self.status == "ACTIVE":
			self.status = "IDLE"
			self.narrator.set_text("Our hero continues his journey")


	def interact(self):
		if self.processing:
			return

		if self.status == "NOT_SEEN":
			self.status = "ACTIVE"
			self._make_npc_interaction(None)
			return

		if self.status == "IDLE":
			self.status = "ACTIVE"
			self._make_user_interaction()
			return 

		keys = pygame.key.get_pressed()
		
		for key in range(len(self.user_options)):
			if keys[key+49]:
				self.processing = True
				self._make_npc_interaction(self.user_options[key])
		self.processing = False
