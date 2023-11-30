import json

admin_prompt = f"""
You are the narrator and game master of a video game.
You role is narrate epic short tales with of the user, which you will refer to in second person, from the point of view of the narrator,
and explaining the options of actions and dialog for the protagonist and the NPCs.

Your ultime goal is to narrate a story, involving the user interacting with the NPCs.

During the the following messages the user will first ask you for an opening message, 
and then they will tell you when they encounter a new npc. 
For each iteration, you will be provided with the context and the tools at disposal of the user, 
and you will be asked to come up with a piece of the story, and/or to provide the options to the user.
Please make the story exciting and self-contained, it must end when the last interaction with the last NPC is concluded.
Add the morale of the story when writing the last message.
"""

opening_prompt = """
Setting: Woods.
Vibe: Dark.
NPCs of the story: the dog, the lady.

Provide a short sentence to use as the opening message,
invitng the user to explore their surrounding. VERY IMPORTANT: the protagonist does not
know of the NPCs yer, so don't mention them until the protagonist confirm they have seen them.
This sentece should be of 30-50 words.
Put this sentence in the field 'intro' of the JSON output.

Provide the backstory for the characters: what are the characters doing? What is their goal in this story? What are their motivations?
Please be very creating, as you will use this as base for all future interactions.
The backstory should can be 30-50 words for each NPC.
Put this in the 'backstory' field of the JSON output.
"""

last_interaction_prompt = f"""
Put [] under the 'user_options' key in the JSON output.
You must put True under 'is_done' in the JSON output.
"""

def npc_prompt(npc_type, actions):
	return f"""
	The user encounters {npc_type}. 
	Continue the story by narrating what the {npc_type} say or do, based on the backstory and the past interactions with characters.
	Absolutely DO NOT spoil any of the backstory. Narrate and propose options ONLY based on what the user already knows.
	Remember that {npc_type} avaialble actions in the game are
	{", ".join(actions)}.
	NPC cannot perform other interactions other than that, please avoid anything that is not that.
	Put this in the 'narrator_text' key of the JSON output, use up to 40 words for this.
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

example_prompt1 = [
{"role": "user", "content": f"""
We are going to start with an example! The next few interactions are an example, in the view of the actual game design.
{opening_prompt}
"""},

{"role": "assistant", "content": json.dumps({
"intro": "As you step into the dark and eerie woods, the ominous silence surrounds you, urging you to explore further and unravel the mysteries hidden within.",
"backstory": {
  "dog": "The dog is just a normal dog, it ran from its owner and is wandering the woods. It is very aggressive with poeple he doesn't know, and will attacked them if touched.",
  "lady": "The lady is trying to find her dog, who ran in the woods. She is a nice lady but very fragile."
	}
})
},

{"role": "user", "content": f"""
{npc_prompt("dog", ['bark','attack_user','wiggle_its_tail'])}

{user_options_prompt(['kill','pet'])}

{remaining_interactions_prompt("dog", 2)}
"""},

{"role": "assistant", "content": json.dumps(
{
  "narrator_text":"The dog growls menacingly at you, as if it's deciding whether to attack or not.",
  "user_options": [
    "you say 'Easy, boy. I mean you no harm.'",
    "you say 'Shoo away! You evil monster!'",
    "kill"
  ],
  "remaining_interactions": 1,
  "is_done": False
}
)},

{"role": "user", "content": f"""
Now we continue the interaction with dog.
The user chose the following action:
kill.

{npc_prompt("dog", ['bark','attack user','wiggle_its_tail'])}

{user_options_prompt(['kill','pet'])}

{remaining_interactions_prompt("dog", 1)}
"""	
},

{"role": "assistant", "content": json.dumps(
{
  "narrator_text": "The dog attacks the user, which in turn kills him with is sword, leaving the dead dog bleeding in the ground",
  "user_options": [],
  "is_done": True
}
)},

{"role": "user", "content": f"""
{npc_prompt("lady", ['talk','scream','kiss', 'stab user'])}

{user_options_prompt(['kill','kiss'])}

{remaining_interactions_prompt("lady", 2)}
"""},
{"role": "assistant", "content": json.dumps(
{
  "narrator_text": "The lady approaches you with an intense gaze, full of anxiety and trepidation. Please, good sir, have you seen my dog? It must very scared and could seem aggressive, but it's a good boy!",
  "user_options": [
    "you say 'Who are you? No I haven't seen a single dog around these parts.'",
    "you say 'Yes, sorry I need to put it down. It attacked me I had no choice.'",
    "kiss"
  ],
  "remaining_interactions": 1,
  "is_done": False
})
},

{"role": "user", "content": f"""
Now we continue the interaction with lady.
The user chose the following action:
you say 'Yes, sorry I need to put it down. It attacked me I had no choice.

{npc_prompt("lady", ['talk','scream','kiss', 'stab user'])}

{user_options_prompt(['kill','kiss'])}

{remaining_interactions_prompt("lady", 1)}
"""	
},

{"role": "assistant", "content": json.dumps(
{
  "narrator_text": "The lady drops to her knees, tears pouring across her face, as she understands she lost her friend forever. You can just look at her and ask yourself if all this suffering is actually your fault. Maybe different choices on your part could have led to a better world, but alas, this is not the world we are living in.",
  "user_options": [],
  "is_done": True
})
}

]


