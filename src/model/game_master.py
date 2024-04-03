from src.model.llm_connector import LLMConnector
from src.model.prompts import *


class GameMaster(LLMConnector):
	def __init__(self):
		super().__init__()

		prompt = [{"role": "system", "content": admin_prompt},
				  {"role": "user", "content": backstory_prompt}]

		story_obj = self.get_json_answer(prompt)

		print(story_obj)
		print()
		# story_obj = {'lady_prompt': 'You are a graceful lady wandering through the woods, searching for your lost pet dog. You are kind-hearted and in need of assistance to find and reunite with your beloved companion.', 'dog_prompt': 'You are a loyal dog, but currently distressed and wary of strangers in the woods. You cannot communicate verbally and may appear aggressive at first, but you deeply desire to be reunited with your lady companion.', 'win_scenario': 'The dog is successfully calmed and reunited with the lady.', 'lose_scenarios': 'The dog runs away and is lost forever; the lady is injured or lost in the woods.'}
		
		for k,v in story_obj.items():
			setattr(self, k, v)

		self.history = []


	def get_npc_prompt(self, npc_type):
		return getattr(self, f'{npc_type}_prompt')

	def get_intro_message(self):
		prompt = [{"role": "system", "content": admin_prompt},
				  {"role": "user", "content": intro_prompt}]

		return self.get_str_answer(prompt)

	def _get_pretty_history(self, new_npc_msg, new_npc):
		pretty = ""
		met_npcs = set([])

		for i in range(len(self.history)):
			usr_msg, npc, npc_msg = self.history[i]
			if i == 0 or npc not in met_npcs:
				met_npcs.add(npc)
				pretty += f"The protagonist meets a {npc}\n"
			elif i > 0 and npc != self.history[i-1][1]:
				pretty += f"The protagonist goes back to the {npc}\n"
			
			pretty += f"Protagonist: {usr_msg}\n"
			pretty += f"{npc}: {npc_msg}\n"

		return pretty

	def update_history(self, usr_msg, npc, npc_msg):
		self.history.append((usr_msg, npc, npc_msg))

	def get_interaction_outcome(self, npc_message, npc_type):

		npc_prompt = npc_interaction_prompt(
						self._get_pretty_history(npc_message, npc_type), 
						self.win_scenario, 
						self.lose_scenarios, 
						npc_message, 
						npc_type
					)

		prompt = [{"role": "system", "content": admin_prompt},
				  {"role": "user", "content": npc_prompt}]

		return self.get_json_answer(prompt)
