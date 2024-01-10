import json

admin_prompt = f"""
You are the narrator and game master in a video game.
Your role is to narrate in a enticing manner the user interactions with their environment and with NPCs, and to make up the backstories, goal and motivations of said NPCs.
You should always adhere to the constrains specified in each prompt.  
"""

def backstory_prompt(setting, user_actions, npc_actions):
	return [{"role": "user", "content": f"""The first goal is setting up the plot.
Here is the context.

Settings: woods.
Vibe of the story: dark, twisted.
NPCs of the story: dog, lady.

Let's define the backstory of the NPCs, and what a winning scenario is for the protagonist. 
Let's try to make the story nteresting, with the NPCs interconnected between them and with a clear objective.

Please reply with a JSON object with the following fields:
'dog_backstory': with the backstory for dog
'lady_backstory': the backstory for lady
the backstory should answer the following questions, for each npc:
why are they here, what is their mood? what are they trying to do?
In order for the story to be interesting the npcs backstory should be connected.

'goal': this field in the JSON output should contain a win condition.
Plese be aware that this is a videogame, and the user can only talk, kill and kiss,
so make sure the can be an ending with all or some of those activties.
"""},
{"role": "assistant", "content": 
json.dumps({
"dog": "The dog is just a normal dog, it ran from its owner and is wandering the woods. It is very aggressive with poeple he doesn't know, and will attack if not approached.",
"lady": "The lady is trying to find her dog, who ran in the woods. She is a nice lady but very emotionally fragile.",
"goal": "Don't kill the dog. Make him calm, and then talk tell the lady where to find it"
})
},
{"role": "user", "content": f"""The first goal is setting up the plot.
Here is the context.

Setting: {setting['setting']}.
Vibe of the story: {setting['vibe']}
NPCs of the story: {list(npc_actions.keys())}.

Let's define the backstory of the NPCs, and what a winning scenario is for the protagonist. 
Let's try to make the story nteresting, with the NPCs interconnected between them and with a clear objective.

Please reply with a JSON object with the following fields:
{", ".join([f"'{npc}_backstory'" for npc in list(npc_actions.keys())])}, 'goal'

the backstories should answer the following questions, for each npc:
why are they here, what is their mood? what are they trying to do?
In order for the story to be interesting the npcs backstory should be connected.

the 'goal' field in the JSON output should contain a win condition.
Plese be aware that this is a videogame, and the user can only {user_actions},
so make sure the can be an ending with all or some of those activties.
"""}
]


def opening_prompt(setting):
	return f"""
The protagonist finds him self in {setting['setting']}.
As the narrator of this video game, write a sentence, using second person, to introduce the user to the level,
and invite them to explore the surroundings. 
The vibe is {setting['vibe']}.

Return the sentence in a JSON object in the 'intro' field. It should be around 50 words.
"""

def npc_prompt(npc_type, actions, user_actions, backstory, story_so_far):
	print(backstory)
	print(story_so_far)
#	first = f"The user encounters {npc_type}. Describe briefly what do they look like and their demeanor."
	story = ""
	if len(story_so_far) > 0:
		# first = f"The user continue the conversation with {npc_type}."
		story = f"Story so far:\n{story_so_far}"
	return [{"role": "user", "content": f"""
The interacts with {npc_type}.

Backstory:
{backstory}

{story}

Based on the backstory and the story so far, write a sentence from the point of view of {npc_type}: What do they say or do to user?
Please DO NOT spoil any of the backstory that has not been discovered yet. Narrate and propose options ONLY based on what the user already knows.
Remember that {npc_type} avaialble actions in the game are:
{", ".join(actions)}.
NPC cannot perform other interactions other than that because they are not implemented in the game, please avoid anything that is not that.
Put this in the 'narrator_text' key of the JSON output, use up to 40 words for this.

Furthermore, provide 3 options for the protagonist to respond to {npc_type}. 
One of the three options should lead to improving towards the goal of the story, one should lead towards failing the goal, and one should be neutral.
Don't make it too obvious which one is which!
Actions available are the following.
{", ".join(user_actions)}.
Talk actions consist in a sentence that the protagonist say, in the following form:
'''
you say "[the sentence]"
'''
All options must be expressed in second person.
Put the options in a list of objects under the 'user_options' key in the JSON output, each object should contain two fields:
- "option": the text of the option
- "result": the outcome of the option, if it gets choosen by the protagonist, it MUST be among the following codes:
	- "DN": if the npc dies, e.g. because it gets attacked by user
	- "FN": npc flees and won't return
	- "L": the player lost the objective, and thus the game should ends in a loss; this will end the game and should ONLY be reutrned when the goal above cannot be reached anymore
	- "W": the player succeed in reaching the objective, and thus the game ends in a win; this will end the game and should ONLY be reutrned when the goal above is completely reached and its condition satisfied
	- "N": for anything else, in this case maybe the protagonist is closer or further away from the goal, but the game continues

Example 1, lady is necessary to reach the end goal
"option": "the user attacks the lady with its sword and cuts her throat", "result": "L"

Example 2, lady is not necessary to reach the end goal
"option": "the user attacks the lady with its sword and cuts her throat", "result": "DN"

Example 3, lady was actually an evil witch, and the goal was to kill her
"option": "the user attacks the lady with its sword and cuts her throat", "result": "W"

Example 4, conversation
"option": "the user asks the lady why is she in distress", "result": "N"

Example 5, dog is not essential in the story anymore
"option": "the user shoosh the dog away threatening him with its sword", "result": "FN"

Note: these are just general example, the actual options MUST involve EXCLUSIVELY {npc_type} and be based on the Backstory and Story.
Be very careful with "L" and "W" outcomes, as they will end the game, only use them when the story is absolutely over with a positive or negative ending.
"""}]







last_interaction_prompt = f"""
Put [] under the 'user_options' key in the JSON output.
You must put True under 'is_done' in the JSON output.
"""

def user_options_prompt(user_options):
	return f"""
	Provide further 3 options for the protagonist to respond. 
	Please remember this is a story, be sure the new options add to it based on the history you narrated before.
	Of the three options, two must be talk interactions and one must be action interaction.
	Actions available are the following.
	{", ".join(user_options)}.
	Talk actions consist in a sentence that the protagonist say, in the following form:
	'''
	you say "[the sentence]"
	'''
	All options must be expressed in second person.
	Put the options in a list under the 'user_options' key in the JSON output.
	"""

def remaining_interactions_prompt(npc_type, remaining_interactions):
	return f"""
	There can be up to {remaining_interactions} remaining_interactions between the user and {npc_type}.
	If this is the last interaction, put True under 'is_done' in the JSON output, put False otherwise.
	If this is the last interaction, put [] under the 'user_options' key in the JSON output.
	"""

# example_prompt1 = [
# {"role": "user", "content": f"""
# We are going to start with an example! The next few interactions are an example, in the view of the actual game design.
# """}
# # {opening_prompt}
# ,

# {"role": "assistant", "content": json.dumps({
# "intro": "As you step into the dark and eerie woods, the ominous silence surrounds you, urging you to explore further and unravel the mysteries hidden within.",
# "backstory": {
#   "dog": "The dog is just a normal dog, it ran from its owner and is wandering the woods. It is very aggressive with poeple he doesn't know, and will attacked them if touched.",
#   "lady": "The lady is trying to find her dog, who ran in the woods. She is a nice lady but very fragile."
# 	}
# })
# },

# {"role": "user", "content": f"""
# {npc_prompt("dog", ['bark','attack_user','wiggle_its_tail'])}

# {user_options_prompt(['kill','pet'])}

# {remaining_interactions_prompt("dog", 2)}
# """},

# {"role": "assistant", "content": json.dumps(
# {
#   "narrator_text":"The dog growls menacingly at you, as if it's deciding whether to attack or not.",
#   "user_options": [
#     "you say 'Easy, boy. I mean you no harm.'",
#     "you say 'Shoo away! You evil monster!'",
#     "kill"
#   ],
#   "remaining_interactions": 1,
#   "is_done": False
# }
# )},

# {"role": "user", "content": f"""
# Now we continue the interaction with dog.
# The user chose the following action:
# kill.

# {npc_prompt("dog", ['bark','attack user','wiggle_its_tail'])}

# {user_options_prompt(['kill','pet'])}

# {remaining_interactions_prompt("dog", 1)}
# """	
# },

# {"role": "assistant", "content": json.dumps(
# {
#   "narrator_text": "The dog attacks the user, which in turn kills him with is sword, leaving the dead dog bleeding in the ground",
#   "user_options": [],
#   "is_done": True
# }
# )},

# {"role": "user", "content": f"""
# {npc_prompt("lady", ['talk','scream','kiss', 'stab user'])}

# {user_options_prompt(['kill','kiss'])}

# {remaining_interactions_prompt("lady", 2)}
# """},
# {"role": "assistant", "content": json.dumps(
# {
#   "narrator_text": "The lady approaches you with an intense gaze, full of anxiety and trepidation. Please, good sir, have you seen my dog? It must very scared and could seem aggressive, but it's a good boy!",
#   "user_options": [
#     "you say 'Who are you? No I haven't seen a single dog around these parts.'",
#     "you say 'Yes, sorry I need to put it down. It attacked me I had no choice.'",
#     "kiss"
#   ],
#   "remaining_interactions": 1,
#   "is_done": False
# })
# },

# {"role": "user", "content": f"""
# Now we continue the interaction with lady.
# The user chose the following action:
# you say 'Yes, sorry I need to put it down. It attacked me I had no choice.

# {npc_prompt("lady", ['talk','scream','kiss', 'stab user'])}

# {user_options_prompt(['kill','kiss'])}

# {remaining_interactions_prompt("lady", 1)}
# """	
# },

# {"role": "assistant", "content": json.dumps(
# {
#   "narrator_text": "The lady drops to her knees, tears pouring across her face, as she understands she lost her friend forever. You can just look at her and ask yourself if all this suffering is actually your fault. Maybe different choices on your part could have led to a better world, but alas, this is not the world we are living in.",
#   "user_options": [],
#   "is_done": True
# })
# }

# ]


