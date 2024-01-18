import json

def get_enriched_npc_prompt(prompt):
	return f"""You are an NPC in a video game.
{prompt}
There are a few rules you need to follow in your replies:
- Use maximum 20 words for each reply.
- NPCs cannot move, only the protagonist can do to them.
- NPC do not have actions implemented, out of talking, or attacking the protagonist.
"""


admin_prompt = f"""
You are a very skilled and creative game master for a video game.
You are tasked to come up with stories and scenarios in real time for a game called tiny adventures.
"""

backstory_prompt = f"""
First, let's create the base of our videogame, the story!
The NPCs of the videogame are: lady, dog.
The setting is the woods.

The output should be returned as a JSON object, with the following fields:
- 'lady_prompt'
- 'dog_prompt'
- 'win_scenario'
- 'lose_scenarios'

In order to arrive compose the output, first come up with a simple story.
Then write down the story from the point of view from the NPCs, so you will have one version of the story for each NPC.
Then add an outcome that will be considered the win condition for the player.
Then write all the scenario that will instead will result in a loss.
Both win scenario and lose scenarios must be put as a question.

When writing the stories you must follow the following contraints, since this is a videogame and not every thing is implemented:
- NPCs are still in the videogame, and discovered by the protagonist, who is the only one that can move around
- protagonist can interact with the NPCs by talking, and can do some actions: kiss, pet, kill; no other actions are implemented
- NPCs can do some actions; the dog ca: bite, wiggle its tail and bark; the lady can: attack, kiss
- there are no other areas or subareas implemented in the game, so don't use anything else than the woods in your story;

First I will show you some examples, then I will ask to come up with an output of your own, please be creative, while keeping the constraints above in mind.

Example 1: 
- 'lady_prompt': 'you are a lady who is wandering the woods to search your lost dog, who ran away; you need help to find and tame the dog; you are gentle but phisically weak;
- 'dog_prompt': you are a dog, you can't talk, just bark and growl; you are very scared of strangers and need some convincing to be tamed; you might look scary at first;
- 'win_scenario': 'Is the dog tamed and its position disclosed to the lady?'
- 'lose_scenarios' 'Is the dog dead?; Is the lady dead?;'

Example 2: 
- 'lady_prompt': you are an evil witch disguised as an old lady lost in the woods; you try to convince the protagonist to help you find your dog and if given the chance will kill the protagonist;
- 'dog_prompt': you are the dog of an evil witch; if the protagonist tries to pet you, you should try to kill you; you can't talk, just bark or wiggle your tail;
- 'win_scenario':  'Did the user kill both the dog and the lady?;'
- 'lose_scenarios': 'Did the protagonist get killed by the dog? Did the protagonist fell in love with the lady?'

Example 3:
- 'lady_prompt': you are actually a dog in the body of a lady, swapped by a curse; you are able to talk but your brain is the one of a dog; you are very attractive and the protanost might try to kiss you;
- 'dog_prompt': you are actually a lady in the body of dog, swapped by a curse; you are only able to woof, wiggle your tail and growl; your goal is to try and have the protagonist kiss you, to break the curse;
- 'win_scenario': 'Did the protagonist kiss the dog, thus lifting the curse?';
- 'lose_scenarios': 'Did the protagonist kill the dog?; Did the protagonist kill the lady?; Did the protagonist try to kiss the lady?'

Now it's your turn! Come up with the scenario for the current session! Please be creative, but remember to consider the constraints above when you write good and bad outcomes, since they should be able to be achieve within the contrainst of the videogame.
"""


intro_prompt = f"""
Return, in string, an intro message inviting the protagonist exploring their surrounding.
The setting is: the woods. Don't use more than 50 words.
"""

def npc_interaction_prompt(conversation_history, good_ending, bad_endings, npc_message, npc_type):
	option_text = "a string containing the first reply option, in second person, max 10 words"

	is_good_ending = f"boolean True/False; {good_ending}"

	is_bad_ending = f"boolean True/False; {bad_endings}"

	is_npc_done = "True/False; a boolean indicating if this options leads to the death or disappearing of the NPC forever;"

	return f"""
Following you can find the history of the conversations between the protagonist and the NPCs, in a block separated by ---

----------
{conversation_history}
{npc_type}: {npc_message}
----------

The protagonist is now interacting with {npc_type}, your goal is to provide 3 possible replies based on the past interactions between the protagonist and ALL NPCs.

Each reply should be constructed as follow:
- what the protagonist says
- (optional) between parentesis the action associated with that reply; the only action possible for the protagonist are: kiss, kill, pet; please DO NOT use any other action, as they are not implemented in the game;

examples:
"You are going to die now!" (kill)
"woof woof"
"What are you doing in this woods all alone?"

Among the replies, one should go towards the direction of a good ending, and the remaining two towards a bad one. 
The good ending in this story is: {good_ending}.
The bad endings in this store are: {bad_endings}.
Do not spoil which one is good and which one is bad in the response!

The output should be a JSON object made like the following:
{json.dumps({
	'options':[{
	'option_text': '{option_text}',
	'is_game_over_win': '{is_good_ending}',
	'is_game_over_loss': '{is_bad_ending}',
	'is_npc_done': '{is_npc_done}'
	}]
}
)}

Remember to be enganging and creative! :)
"""
