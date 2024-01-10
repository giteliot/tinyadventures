import os
from openai import OpenAI
import json
from src.model.prompts import *


class LevelGenerator:
	def __init__(self, setting, user_actions, npc_actions):
		self.model = "gpt-3.5-turbo-1106"
		self.client = OpenAI()
		self.temperature = 1.0

		self.setting = setting
		self.user_actions = user_actions
		self.npc_actions = npc_actions

		self.prompt = [{"role": "system", "content": admin_prompt}]

		_backstory_response = self._one_shot_call(
			self.prompt+backstory_prompt(
				self.setting,
				self.user_actions,
				self.npc_actions
			))

		self.backstory = "\n".join([f"{k}: {v}" for k,v in _backstory_response.items()]) 

		print(self.backstory)

		self.story_so_far = ""

		# self.actions = {
		# 	'lady': ['talk','scream','kiss', 'stab user'],
		# 	'dog': ['bark','attack user','wiggle_its_tail'],
		# }

		# self.options = {
		# 	'lady': ['kill','kiss'],
		# 	'dog': ['kill','pet'],
		# }

		# self.interactions = {
		# 	'lady': 1,
		# 	'dog': 1
		# }

	def _one_shot_call(self, prompt):
		response = self.client.chat.completions.create(
		   model=self.model,
		   messages=prompt,
		   temperature=self.temperature,
		   response_format={'type': 'json_object'}
		)

		return json.loads(response.choices[0].message.content)


	def _call_gpt(self, prompt):
		self.prompt.append(
			{"role": "user", "content": prompt}
		)

		response = self.client.chat.completions.create(
		   model=self.model,
		   messages=self.prompt,
		   temperature=self.temperature,
		   response_format={'type': 'json_object'}
		)

		self.prompt.append(
			{"role": "assistant", "content": response.choices[0].message.content
		})

		print(response.choices[0].message.content)

		return json.loads(response.choices[0].message.content)


	def get_opening_message(self):
		# return "go look for stuff"

		resp_obj = self._call_gpt(opening_prompt(self.setting))

		intro = "something bad happened in the generation of the level"
		if 'intro' in resp_obj:
			intro = resp_obj['intro']

		return intro

	def get_npc_message(
			self, 
			npc_type, 
			user_response
	):
		if len(user_response) > 1:
			self.backstory += f"\nUser to {npc_type}: {user_response}"
		resp_obj = self._one_shot_call(
			self.prompt+npc_prompt(
				npc_type, 
				self.npc_actions[npc_type],
				self.user_actions,
				self.backstory,
				self.story_so_far)
			)

		print()
		print(resp_obj)
		print()

		narrator_text = " "
		if 'narrator_text' in resp_obj:
			narrator_text = resp_obj['narrator_text']

		self.backstory += f"\n{narrator_text}"

		user_options = []
		if 'user_options' in resp_obj:
			user_options = [r['option'] for r in resp_obj['user_options']]

		return narrator_text, user_options, False

	# def get_npc_message(
	# 		self, 
	# 		npc_type, 
	# 		is_opening, 
	# 		narrator_intro, 
	# 		user_response, 
	# 		remaining_interactions
	# ):
	# 	if is_opening:
	# 		new_prompt = f"""
	# 			{npc_prompt(npc_type, self.actions[npc_type])}

	# 			{user_options_prompt(self.options[npc_type])}

	# 			{remaining_interactions_prompt(npc_type, remaining_interactions)}
	# 			"""
	# 	elif remaining_interactions > 0:
	# 		new_prompt = f"""
	# 			Now we continue the interaction with {npc_type}.
	# 			The user chose the following action:
	# 			{user_response}.

	# 			{npc_prompt(npc_type, self.actions[npc_type])}

	# 			{user_options_prompt(self.options[npc_type])}

	# 			{remaining_interactions_prompt(npc_type, remaining_interactions)}
	# 			"""	
	# 	else:
	# 		self.interactions[npc_type] = 0
	# 		if sum(self.interactions.values()) > 0:
	# 			new_prompt = f"""
	# 				Now we continue the interaction with {npc_type}.
	# 				The user chose the following action:
	# 				{user_response}.
					
	# 				{npc_prompt(npc_type, self.actions[npc_type])}

	# 				This is the last interaction between {npc_type} and the user, so be sure there is closure.
	# 				{last_interaction_prompt}
	# 				"""	
	# 		else:
	# 			new_prompt = f"""
	# 				Now we continue the interaction with {npc_type}.
	# 				The user chose the following action:
	# 				{user_response}.
	# 				This is the end of the story! Write up the last {npc_type} message or action and add an ending of the story.
	# 				The ending of the story should consist of a nice epilogue and potentially a moral of the story.
	# 				Put this in the 'narrator_text' key of the JSON output, use up to 60 words for this.
	# 				{last_interaction_prompt}
	# 				"""	
			

	# 	print(new_prompt)

	# 	resp_obj = self._call_gpt(new_prompt)

	# 	if resp_obj['is_done'] == True:
	# 		self.interactions[npc_type] = 0

	# 	narrator_text = " "
	# 	if 'narrator_text' in resp_obj:
	# 		narrator_text = resp_obj['narrator_text']

	# 	user_options = []
	# 	if 'user_options' in resp_obj:
	# 		user_options = resp_obj['user_options']

	# 	is_done = False
	# 	if 'is_done' in resp_obj:
	# 		is_done = resp_obj['is_done']

	# 	return narrator_text, user_options, is_done

