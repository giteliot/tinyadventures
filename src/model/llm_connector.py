from openai import OpenAI
import json

class LLMConnector:
	def __init__(self):
		# self.model = "gpt-3.5-turbo-1106"
		self.model = "gpt-4-1106-preview"
		self.client = OpenAI()
		self.temperature = 1.0

	def get_json_answer(self, prompt):

		print(prompt)
		response = self.client.chat.completions.create(
		   model=self.model,
		   messages=prompt,
		   temperature=self.temperature,
		   response_format={'type': 'json_object'}
		)

		print(f"-----\n{response.choices[0].message.content}\n")

		return json.loads(response.choices[0].message.content) 

	def get_str_answer(self, prompt):

		print(prompt)
		response = self.client.chat.completions.create(
		   model=self.model,
		   messages=prompt,
		   temperature=self.temperature
		)

		print(f"-----\n{response.choices[0].message.content}\n")

		return response.choices[0].message.content