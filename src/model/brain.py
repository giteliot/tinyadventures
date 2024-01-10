import os
from openai import OpenAI
import json
from src.model.prompts import *
from src.model.llm_connector import LLMConnector

class Brain(LLMConnector):
	def __init__(self, base_prompt):
		super().__init__()

		self.prompt = [{"role": "system", "content": f"{base_prompt} Use maximum 20 words for each reply."}]

	def interact(self, user_message):
		self.prompt.append({"role": "user", "content": user_message})

		answer = self.get_str_answer(self.prompt)

		self.prompt.append({"role": "assistant", "content": answer})

		return answer
