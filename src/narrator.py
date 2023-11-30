from src.settings import NARRATOR_HEIGHT
import pygame

class Narrator:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.base_width = self.display_surface.get_size()[0]
		self.base_height = self.display_surface.get_size()[1]
		self.text = ""
		self.border_size = 2
		self.font = pygame.font.Font('./graphics/narrator.ttf', 30)
		self.loading_init_time = 0

	def set_loading(self):
		self.loading_init_time = pygame.time.get_ticks

	def set_text(self, text):
		self.loading_init_time = 0
		self.text = text

	def wrap_text(self):
		max_width = self.display_surface.get_size()[0]-self.border_size*12
		words = self.text.split()
		lines = []
		current_line = ""
		
		for word in words:
			test_line = current_line + word + " "
			test_size = self.font.size(test_line)
			if test_size[0] <= max_width and word != 'XXX':
				current_line = test_line
			else:
				lines.append(current_line)
				current_line = word.replace("XXX","") + " "
		
		lines.append(current_line)
		
		return lines

	def display_loading(self):
		dt = self.loading_init_time-pygame.time.get_ticks
		n_dots = (dt//1000)%3+1
		print(n_dots)
		text_surface = self.font.render(" ".join(["."]*n_dots), True, (255,255,255))
		self.display_surface.blit(text_surface, (
			self.base_width//2-12, self.base_height-NARRATOR_HEIGHT+self.border_size*4-4))

	def display_text(self):
		wrapped_text = self.wrap_text()
		text_height = len(wrapped_text) * self.font.get_linesize()
		text_y = self.base_height-NARRATOR_HEIGHT + (NARRATOR_HEIGHT - text_height) // 2

		for line in wrapped_text:
			text_surface = self.font.render(line, True, (255,255,255))
			text_width, text_height = text_surface.get_size() 
			text_x = self.border_size+(self.base_width - text_width) // 2
			self.display_surface.blit(text_surface, (text_x, text_y))
			text_y += self.font.get_linesize()


	def display(self):
		pygame.draw.rect(
				self.display_surface, (0,0,0), 
				(
					0, 
					self.base_height-NARRATOR_HEIGHT, 
					self.base_width,
					NARRATOR_HEIGHT
				)
		)

		pygame.draw.rect(
				self.display_surface, (255,255,255), 
				(
					self.border_size*3, 
					self.base_height-NARRATOR_HEIGHT+self.border_size*3,
					self.base_width-self.border_size*6, 
					NARRATOR_HEIGHT-self.border_size*6
				)
		)

		pygame.draw.rect(
				self.display_surface, (0,0,0), 
				(
					self.border_size*4, 
					self.base_height-NARRATOR_HEIGHT+self.border_size*4, 
					self.base_width-self.border_size*8,
					NARRATOR_HEIGHT-self.border_size*8
				)
		)

		if self.loading_init_time > 0:
			self.display_loading()
		else:
			self.display_text()
