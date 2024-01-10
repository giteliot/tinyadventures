import json

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
Then write down the story from the point of view from the NPC.
Then add an outcome that will be considered the win condition for the player.
Then write all the scenario that will instead will result in a loss.

When writing the stories consider that in the videogame the characters will be still, and discovered by the protagonist, who is the one that can move around.
The protagonist can interact with the NPCs by talking, and can do some actions: kiss, pet, kill. 

First I will show you some examples, then I will ask to come up with an output of your own, please be creative, while keeping the constraints above in mind.

Example 1: 
- 'lady_prompt': 'you are a lady who is wandering the woods to search your lost dog, who ran away; you need help to find and tame the dog; you are gentle but phisically weak;
- 'dog_prompt': you are a dog, you can't talk, just bark and growl; you are very scared of strangers and need some convincing to be tamed; you might look scary at first;
- 'win_scenario': 'the dog is tamed and then its position is discoled to the lady'
- 'lose_scenarios' 'the dog dies or runs away; the lady dies or runs away;'

Example 2: 
- 'lady_prompt': you are an evil witch disguised as an old lady lost in the woods; you try to convince the protagonist to help you find your dog and if given the chance will kill the protagonist;
- 'dog_prompt': you are the dog of an evil witch; if the protagonist tries to pet you, you should try to kill you; you can't talk, just bark or wiggle your tail;
- 'win_scenario':  'he user kills both the lady and the dog, or flees;'
- 'lose_scenarios'

Example 3:
- 'lady_prompt': you are actually a dog in the body of a lady, swapped by a curse; you are able to talk but your brain is the one of a dog; you are very attractive and the protanost might try to kiss you;
- 'dog_prompt': you are actually a lady in the body of dog, swapped by a curse; you are only able to woof, wiggle your tail and growl; your goal is to try and have the protagonist kiss you, to break the curse;
- 'win_scenario': the protagonist kisses the dog and breaks the curse;
- 'lose_scenarios': the protagonist kills either the dog or the lady, or try to kiss the lady;

Now it's your turn! Come up with the scenario for the current session! Please be creative, but remember to consider the constraints above when you write good and bad outcomes, since they should be able to be achieve within the contrainst of the videogame.
"""


intro_prompt = f"""
Return, in string, an intro message inviting the protagonist exploring their surrounding.
The setting is: the woods. Don't use more than 50 words.
"""

def npc_interaction_prompt(conversation_history, good_ending, bad_endings, npc_message, npc_type):
	return f"""
Following you can find the history of the conversations between the protagonist and the NPCs, in a block separated by ---

----------
{conversation_history}
{npc_type}: {npc_message}
----------

The protagonist is now interacting with {npc_type}, your goal is to provide 3 possible replies based on the past interactions between the protagonist and ALL NPCs.

Each reply should be constructed as follow:
- what the protagonist says
- (optional) between parentesis the action associated with that reply

examples:
"You are going to do now!" (kill)
"Mmh I like your body" (kiss)
"What are you doing in this woods all alone?"

Among the replies, one should go towards the direction of a good ending, and the remaining two towards a bad one. 
The good ending in this story is: {good_ending}.
The bad endings in this store are: {bad_endings}.
Do not spoil which one is good and which one is bad in the response!

The output should be a JSON object made like the following:
{json.dumps({
	'options':[{
	'option_text': 'a string containing the first reply option, in second person, max 10 words',
	'is_game_over': '-1, 0, 1; -1 if the game is lost (this options verifies one of the bad endings, so the game is over and lost); 1 if the game is won (this options leads to one the good ending); 0 if the game should continue;',
	'is_npc_done': 'True/False; a boolean indicating if this options leads to the death or disappearing of the NPC'
	},
	{
	'option_text': 'a string containing the first reply option, in second person, max 10 words',
	'is_game_over': '-1, 0, 1; -1 if the game is lost (this options verifies one of the bad endings, so the game is over and lost); 1 if the game is won (this options leads to one the good ending); 0 if the game should continue;',
	'is_npc_done': 'True/False; a boolean indicating if this options leads to the death or disappearing of the NPC'
	},
	{
	'option_text': 'a string containing the first reply option, in second person, max 10 words',
	'is_game_over': '-1, 0, 1; -1 if the game is lost (this options verifies one of the bad endings, so the game is over and lost); 1 if the game is won (this options leads to one the good ending); 0 if the game should continue;',
	'is_npc_done': 'True/False; a boolean indicating if this options leads to the death or disappearing of the NPC'
	}]
	}
)}

Remember to be enganging and creative! :)
"""
