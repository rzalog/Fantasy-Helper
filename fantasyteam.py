#!/usr/local/bin/python

# contains the class for fantasy team

import pandas as pd
from pandas import DataFrame as df

from player import Player
from stats import Stats
from stats import printStats

class FantasyTeam:
	'''
	A class that is able to hold a bunch of
	fantasy players, and then do stuff with
	all their stats
	'''
	def __init__(self, teamName):
		self._name = teamName.title()
		self._players = []
		self._stats = df()
		self._totalStats = Stats()

	def addPlayerByName(self, name):
		player = Player(name)
		self._addPlayer(player)

	def name(self):
		return self._name

	def allStats(self):
		return self._stats

	def totalStats(self):
		return self._totalStats

	def _addPlayer(self, player):
		self._players.append(player)
		self._totalStats += player.stats()
		self._stats = self._stats.append(player.stats().stats())

	def _getPlayerStats(self, name):
		first, last = name.split()
		return self._players[(first,last)].stats()

if __name__=='__main__':
	name = raw_input('Enter your team name: ')
	team = FantasyTeam(name)
	playerName = 'name'
	playerName = raw_input('Enter a player name (q to stop): ')
	while playerName != 'q':
		try:
			team.addPlayerByName(playerName)
		except (LookupError, ValueError):
			print 'Player name "' + playerName + '" could not be found.'
			playerName = raw_input('Enter new name: ')
			continue
		playerName = raw_input('Enter new name: ')
	print
	print 'Here is your final team:'
	print 'Team:', team.name()
	print 'Team stats:'
	print team.allStats()
	print
	printStats(team.totalStats())

