#!/usr/local/bin/python

import requests
from pandas import Series
from enum import Enum

import helpers
from constants import *

from stats import Stats
from stats import printStats

playersDidLoadCorrectly = True
players_url = helpers.get_url('commonallplayers', LeagueID=LEAGUE_ID, Season=CURRENT_SEASON, IsOnlyCurrentSeason=0)

try:
	allPlayers = Series(requests.get(players_url, headers=USER_AGENT).json())
except ValueError as e:
	print 'Players could not be loaded.'
	print 'Error:', e.message
	print 'URL:', players_url
	playersDidLoadCorrectly = False

if playersDidLoadCorrectly:
	headers = allPlayers['resultSets'][0]['headers']


def findPlayer(first, last):
	name = last.lower().strip() + ', ' + first.lower().strip()
	for player in allPlayers['resultSets'][0]['rowSet']:
		if name == player[DISPLAY_LAST_COMMA_FIRST].lower():
			return player
	return None

class Player:
	'''
	A class to do things with players
	'''
	def __init__(self, name, season=CURRENT_SEASON):
		'''
		Initialize a Player with the given attributes
		:param last: Last name, capitalization doesn't matter
		:param first: First, same as above
		:param season: The main season we want to work with (some functions may take seasons as a parameter)
		:return: self
		'''
		first, last = name.split()
		self._fullPlayer = findPlayer(first, last)
		if not self._fullPlayer:
			# raise error if we would not find the player
			raise LookupError('Player "' + first + ', ' + last + '" could not be found\n'
				+ 'Note: first name comes before last')
		self._season = season
		self._name = (first.title(), last.title())
		self._initStats()

	# getters
	def playerID(self):
		return self._fullPlayer[PERSON_ID]

	def season(self):
		return self._season

	def name(self):
		# need to use this implementation to ensure proper capitalization / formatting
		last, first = self._fullPlayer[DISPLAY_LAST_COMMA_FIRST]
		return first + ' ' + last[:-1]

	def nameTuple(self):
		return self._name

	def teamCode(self):
		return self._fullPlayer[TEAM_ID]

	def team(self):
		return self._fullPlayer[TEAM_CITY] + ' ' + self._fullPlayer[TEAM_NAME]

	def teamAbbreviation(self):
		return self._fullPlayer[TEAM_ABBREVIATION]

	def stats(self, season=None):
		return self._stats

	def isNameThisPlayer(self, first, last):
		firstN, lastN = self._name[0], self._name[1]
		return first.title() == firstN and last.title() == lastN

	def _initStats(self, season=None, perMode='PerGame'):
		'''
		Constructs a Stats object with a given season
		:param season: 	A valid season string (ex. '2015-16'), default the Player's season
		:param perMode: How the averages are displayed, 'PerGame', 'Per36', etc.
		:return:		***IMPORTANT*** Returns a tuple of a seasonStats list along with a statsHeaders list
		'''
		if not season:
			season = self.season()

		loadSuccess = True

		stats_url = helpers.get_url('playercareerstats', PerMode=perMode, PlayerID=self.playerID())

		try:
			allStats = Series(requests.get(stats_url, headers=USER_AGENT).json())
		except ValueError as e:
			loadSuccess = False
			print 'Could not load stats for player "' + self.name() + '"'
			print 'Error:', e.message
			print 'URL:', stats_url
		if loadSuccess:
			statsHeaders = allStats['resultSets'][0]['headers']
			for obj in allStats['resultSets'][0]['rowSet']:
				if season in obj:
					seasonStats = obj
			self._stats = Stats(Series(dict(zip(statsHeaders, seasonStats)), name=self._name ) )

		else:
			self._stats = None

	def _changePerMode(perMode):
		self._initStats(PerMode=perMode)

	def _changeSeason(newSeason):
		self._initStats(season=newSeason)


####################
# extra functions
####################

def getPlayerInfo(player):
	info = "Name: " + player.name() + '\n'
	info += "Player ID: " + str(player.playerID()) + '\n'
	info += "Team: " + player.team()
	return info

if __name__=='__main__':
	if playersDidLoadCorrectly:
		fullname = 'name'
		while fullname != 'q':
			fullname = raw_input('Name: ')
			try:
				first, last = fullname.split()
			except ValueError:
				print 'Enter a name in the following format: FIRST LAST'
				continue

			try:
				player = Player( (first, last) )
			except LookupError:
				print 'Player could not be found. Try again.'
				continue

			print 'Name:', player.name()
			print 'Season:', player.season()
			printStats(player.stats())
