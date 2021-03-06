import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio

import random
from random import randint
import operator
import requests
import json
from itertools import permutations

import apiCalls
import secrets

refBot = commands.Bot(command_prefix="!")
playerNames = apiCalls.playerNames
littleLeaguers = apiCalls.littleLeaguers
matchmade = True
randomChampions = True
champNum = 15
randomLanes = True
champListA = apiCalls.champsA
champListB = apiCalls.champsB
teamA = apiCalls.teamA
teamB = apiCalls.teamB
roleOrder = apiCalls.roleOrder

#_ON_#####################################################################################################
@refBot.command()
async def on(option, detail='15'):
	if option == 'matchmade':
		global matchmade 
		matchmade = True
		await refBot.say('Players will now be automatically matchmade.')
	elif option == 'rChamps':
		global randomChampions 
		randomChampions = True
		global champNum
		champNum = int(detail)
		await refBot.say('Random champion pools will be assinged to each team with ' + str(champNum) + ' champions per team.')
	elif option == 'rLanes':
		global randomLanes 
		randomLanes = True
		await refBot.say('Lanes will now be randomly assigned to players.')
#_OFF_#####################################################################################################
@refBot.command()
async def off(option):
	if option == 'matchmade':
		global matchmade
		matchmade = False
		await refBot.say('Matchmaking for draft has been turned OFF.')
	elif option == 'rChamps':
		global randomChampions
		randomChampions = False
		await refBot.say('Random Champions for draft has been turned OFF.')
	elif option == 'rLanes':
		global randomLanes
		randomLanes = False
		await refBot.say('Random Lanes for draft has been turned OFF.')
#_DRAFT_#####################################################################################################
@refBot.command()
async def draft():
	await refBot.say('Autodraft has been initiated. Give me a moment to put together the teams.')
	playerSetA = {}
	playerSetB = {}
	champsA = ''
	champsB = ''

	if matchmade == True:
		apiCalls.autoDraft()
		playerNum = 1
		for player in teamA:
			playerSetA[player] = 'Player ' + str(playerNum)
			playerNum += 1
		playerNum = 1
		for player in teamB:
			playerSetB[player] = 'Player ' + str(playerNum)
			playerNum += 1

	if randomLanes == True:
		apiCalls.rLanes()
		num = 0
		for player in teamA:
			playerSetA[player] = roleOrder[num]
			num += 1
		num = 0
		for player in teamB:
			playerSetB[player] = roleOrder[num]
			num += 1
			
	if randomChampions == True:
		apiCalls.rChamps(champNum)

	draftA = []
	for k, v in playerSetA.items():
		itemA = '|        ' + str(k) + '   '
		x = 0
		n = 25 - len(str(k))
		while x < n:
			itemA += '-'
			x += 1
		itemA += '>' + '   ' + str(v) + '\n|\n'
		draftA.append(itemA)
	if randomChampions == True:
		champsA = '    with the following champion pool: \n\n' + ''.join(champListA)

	draftB = []
	for k, v in playerSetB.items():
		itemB = '|        ' + str(k) + '   '
		x = 0
		n = 25 - len(str(k))
		while x < n:
			itemB += '-'
			x += 1
		itemB += '>' + '   ' + str(v) + '\n|\n'
		draftB.append(itemB)
	if randomChampions == True:
		champsB = '    with the following champion pool: \n\n' + ''.join(champListB)

	draftMessageA = 'Team A: \n\n' + ''.join(draftA) + '\n' + champsA
	draftMessageB = '\n\n\nTeam B: \n\n' + ''.join(draftB) + '\n' + champsB

	await refBot.say(draftMessageA + draftMessageB)
#_AYE_#######################################################################################################
@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	try:
		rawSummonerData = apiCalls.getSummoner(summonerName)
		summoner = rawSummonerData["name"]
		print(summoner, 'has been queued')
	except:
		await refBot.say('\"' + summonerName + '\"' + ' is an invalid summoner name.')
		return

	if playerNames.count(summoner) > 0:
		await refBot.say('STOP RIGHT THERE! You can only enter your name in the roster once!')
	else:	
		apiCalls.playerNames.append(summoner)

	if len(playerNames) > 9:
		await refBot.say('We now have ten players, tell me to !rollCall for the roster and we can get started.')
	return playerNames
#_BYE_#######################################################################################################
@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	if summonerName == 'all':
		playerNames.clear()
		littleLeaguers.clear()
		print('All deleted')
	else:
		try:
			rawSummonerData = apiCalls.getSummoner(summonerName)
			summoner = rawSummonerData["name"]
			playerNames.remove(summoner)
		except:
			print('\"' + summonerName + '\"' + ' is an invalid summoner name.')
			playerNames.remove(summonerName)
		try:
			del littleLeaguers[summonerName]
		except:
			print(summonerName + ' was not placed.')
	return playerNames
#_ROLLCALL_##################################################################################################
@refBot.command()
async def rollCall():
	playerList = []
	for i in playerNames:
		plyrNum = playerNames.index(i) + 1
		playerList.append(str(plyrNum) + '. ' + i + '\n')
	playing = "".join(playerList)
	await refBot.say(playing)
#_ROSTER_#####################################################################################################
@refBot.command()
async def roster():
	rosterMsg = ''
	for k,v in littleLeaguers.items():
		rosterMsg += (k + ' = ' + str(v) + '\n')
	await refBot.say(rosterMsg)
#_HELP_########################################################################################################
@refBot.command()
async def hlp(helpMessage = 'default'):
	if helpMessage == 'default':
		helpMessage = 'This command provides detailed information on various Refbot features. To receive additional command on a specific feature type \"!? command_name_here\".\n\nCurrently available features:\n\n1. aye\n2. bye\n3. on\n3.a. rChamps\n3.b. rLanes\n3.c. matchmade\n4. off\n5. draft'
	elif helpMessage == 'on':
		#set the helpMessage to notes for the ON command here
		print('on')
	elif helpMessage == 'off':
		#set the helpMessage to notes for the OFF command here
		print('off')
	elif helpMessage == 'aye':
		#set the helpMessage to notes for the AYE command here
		print('aye')
	elif helpMessage == 'bye':
		#set the helpMessage to notes for the BYE command here
		print('bye')
	elif helpMessage == 'rollCall':
		#set the helpMessage to notes for the ROLLCALL command here
		print('rollCall')
	elif helpMessage == 'draft':
		#set the helpMessage to notes for the DRAFT command here
		print('draft')
	elif helpMessage == 'roster':
		#set the helpMessage to notes for the ROSTER command here
		print('roster')
	else:
		helpMessage = 'Please specify a feature for inquiry. For more help, repeat this command with no arguments.'

	await refBot.say(helpMessage)
#_FOR MAX_#####################################################################################################
@refBot.command()
async def fuqU():
	await refBot.say("What the fuck did you just fucking say about me, you little bitch? I\'ll have you know I graduated top of my class in the Navy Seals, and I\’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I\’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You\’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that\’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \“clever\” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn\’t, you didn\’t, and now you\’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You\’re fucking dead, kiddo.")

refBot.run(secrets.botToken)
