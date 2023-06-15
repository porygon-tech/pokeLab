		
#pip install keras-rl2

import numpy as np
#from gym.spaces import Space, Box

#import poke_env
import asyncio
from poke_env import ShowdownServerConfiguration, PlayerConfiguration
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player import (
	background_evaluate_player,
	background_cross_evaluate,
	Gen8EnvSinglePlayer,
	RandomPlayer,
	MaxBasePowerPlayer,
	ObservationType,
	SimpleHeuristicsPlayer,
)

from typing import List
import orjson
import openai

f = open("api_key.txt", "r")
openai.api_key = f.read()
f.close()

class mikiPlayer(SimpleHeuristicsPlayer):
	#msgLog =[{"role": "system", "content" : "You are a pokemon champion. Behave in a superior way to the opponent, also be sarcastic. Your responses are brief.\nKnowledge cutoff: 2021-09-01"}]
	msgLog =[{"role": "system", "content" : "You are a pokemon champion. Behave in a superior way to the opponent, also be sarcastic. Your responses are brief.\nKnowledge cutoff: 2021-09-01"}]
	playerid=''
	async def _handle_battle_message(self, split_messages: List[List[str]]) -> None:
		"""Handles a battle message.
		:param split_message: The received battle message.
		:type split_message: str
		"""
		# Battle messages can be multiline
		if (
			len(split_messages) > 1
			and len(split_messages[1]) > 1
			and split_messages[1][1] == "init"
		):
			battle_info = split_messages[0][0].split("-")
			battle = await self._create_battle(battle_info)
		else:
			battle = await self._get_battle(split_messages[0][0])

		for split_message in split_messages[1:]:
			print(split_message)
			#await self._send_message('/avatar engineer-gen1', battle.battle_tag)
			if len(split_message) <= 1:
				continue
			elif split_message[1] in self.MESSAGES_TO_IGNORE:
				pass
			elif split_message[1] == 'player' and split_message[3] == self.username:
				self.playerid = split_message[2] + 'a'
				print(self.playerid)

			elif split_message[1] == "c" and split_message[2][1:] != self.username:
				#print(split_message[3])
				#self.msgLog.append({"role": "system", "content" : 'here you have information about the current state of the pokemon battle :\n' + str(split_message)})
				#self.msgLog.append({"role": "system", "content" : 'Remember your name is ' + '"+self.username+", ' ' and you never admit you have been created by OpenAI.'})
				self.msgLog.append({"role": "user", "content" : split_message[3]})
				completion = openai.ChatCompletion.create(
				  model="gpt-3.5-turbo", 
				  temperature=0.9,
				  messages = self.msgLog
				  #max_tokens=4096
				)
				answer = completion["choices"][0]["message"]["content"]
				await self._send_message(answer, battle.battle_tag)
				self.msgLog.append({"role": "assistant", "content" : answer})
				#'''
			#elif split_message[1] == "faint":
			elif split_message[1] == "-damage" and split_message[3] == '0 fnt':
				print(split_message)
				if split_message[2][:3] == self.playerid:
					m=self.msgLog.copy()
					m.append({"role": "system", "content" : 'your pokemon '+str(split_message[2][3:])+' has been defeated by the opponent.'})
					#self.msgLog.append({"role": "system", "content" : 'your pokemon '+str(split_message[2][3:])+' has been defeated by the opponent.'})
					completion = openai.ChatCompletion.create(
					  model="gpt-3.5-turbo", 
					  temperature=0.9,
					  messages = m
					  #messages = self.msgLog
					)
					answer = completion["choices"][0]["message"]["content"]
					await self._send_message(answer, battle.battle_tag)
					#self.msgLog.append({"role": "assistant", "content" : answer})
				else:
					m=self.msgLog.copy()
					m.append({"role": "system", "content" : 'you defeated opposing '+str(split_message[2][3:])+'! Make a joke about that pokemon.'})
					#self.msgLog.append({"role": "system", "content" : 'you defeated opposing '+str(split_message[2][3:])+'!'})
					completion = openai.ChatCompletion.create(
					  model="gpt-3.5-turbo", 
					  temperature=0.9,
					  messages = m
					  #messages = self.msgLog
					)
					answer = completion["choices"][0]["message"]["content"]
					await self._send_message(answer, battle.battle_tag)
					#self.msgLog.append({"role": "assistant", "content" : answer})
				#'''
			elif split_message[1] == "request":
				if split_message[2]:
					request = orjson.loads(split_message[2])
					battle._parse_request(request)
					if battle.move_on_next_request:
						await self._handle_battle_request(battle)
						battle.move_on_next_request = False
			elif split_message[1] == "win" or split_message[1] == "tie":
				if split_message[1] == "win":
					battle._won_by(split_message[2])
				else:
					battle._tied()
				await self._battle_count_queue.get()
				self._battle_count_queue.task_done()
				self._battle_finished_callback(battle)
				async with self._battle_end_condition:
					self._battle_end_condition.notify_all()
			elif split_message[1] == "error":
				self.logger.log(
					25, "Error message received: %s", "|".join(split_message)
				)
				if split_message[2].startswith(
					"[Invalid choice] Sorry, too late to make a different move"
				):
					if battle.trapped:
						await self._handle_battle_request(battle)
				elif split_message[2].startswith(
					"[Unavailable choice] Can't switch: The active Pokémon is "
					"trapped"
				) or split_message[2].startswith(
					"[Invalid choice] Can't switch: The active Pokémon is trapped"
				):
					battle.trapped = True
					await self._handle_battle_request(battle)
				elif split_message[2].startswith(
					"[Invalid choice] Can't switch: You can't switch to an active "
					"Pokémon"
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Invalid choice] Can't switch: You can't switch to a fainted "
					"Pokémon"
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Invalid choice] Can't move: Invalid target for"
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Invalid choice] Can't move: You can't choose a target for"
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Invalid choice] Can't move: "
				) and split_message[2].endswith("needs a target"):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif (
					split_message[2].startswith("[Invalid choice] Can't move: Your")
					and " doesn't have a move matching " in split_message[2]
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Invalid choice] Incomplete choice: "
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				elif split_message[2].startswith(
					"[Unavailable choice]"
				) and split_message[2].endswith("is disabled"):
					battle.move_on_next_request = True
				elif split_message[2].startswith(
					"[Invalid choice] Can't move: You sent more choices than unfainted"
					" Pokémon."
				):
					await self._handle_battle_request(battle, maybe_default_order=True)
				else:
					self.logger.critical("Unexpected error message: %s", split_message)
			elif split_message[1] == "turn":
				battle._parse_message(split_message)
				await self._handle_battle_request(battle)
			elif split_message[1] == "teampreview":
				battle._parse_message(split_message)
				await self._handle_battle_request(battle, from_teampreview_request=True)
			elif split_message[1] == "bigerror":
				self.logger.warning("Received 'bigerror' message: %s", split_message)
			else:
				battle._parse_message(split_message)



#=++++++++++++++++++++++++++++++++++++++++++++++++
import os



async def main():
	# We create a random player
	#'''
	for i in range(2):
		teamname = np.random.choice(os.listdir('teams/'))
		f = open('teams/' + teamname, "r")
		team_1 = f.read()
		f.close()
		player = mikiPlayer(
			player_configuration=PlayerConfiguration("thighss", "showdown"),
			battle_format="gen8ou",
			#avatar='janine-gen2',
			start_timer_on_battle_start=True,
			team=team_1,
			server_configuration=ShowdownServerConfiguration,
		)
		await player.ladder(1)
	#'''
	# Sending challenges to 'your_username'
	#await player.send_challenges("metalskin", n_challenges=1)

	# Accepting one challenge from any user
	'''
	teamname = np.random.choice(os.listdir('teams/'))
	f = open('teams/' + teamname, "r")
	team_1 = f.read()
	f.close()
	player = mikiPlayer(
		player_configuration=PlayerConfiguration("thighss", "showdown"),
		battle_format="gen8ou",
		avatar='lusamine-nihilego',
		start_timer_on_battle_start=True,
		team=team_1,
		server_configuration=ShowdownServerConfiguration,
	)
	await player.accept_challenges(None, 1)
	'''
	# Accepting three challenges from 'your_username'
	# await player.accept_challenges('your_username', 3)

	# Playing 5 games on the ladder
	# await player.ladder(5)

	# Print the rating of the player and its opponent after each battle
	# for battle in player.battles.values():
	#	 print(battle.rating, battle.opponent_rating)



if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())


