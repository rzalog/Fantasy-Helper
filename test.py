import requests
from pandas import Series
from enum import Enum

import helpers
from constants import *

url = helpers.get_url('commonallplayers', LeagueID=LEAGUE_ID, Season=CURRENT_SEASON, IsOnlyCurrentSeason=0)
all_players = Series(requests.get(url).json())
headers = all_players['resultSets'][0]['headers']

'''
Headers:
headers: [
1	"PERSON_ID",
2	"DISPLAY_LAST_COMMA_FIRST",
3	"ROSTERSTATUS",
4	"FROM_YEAR",
5	"TO_YEAR",
6	"PLAYERCODE",
7	"TEAM_ID",
8	"TEAM_CITY",
9	"TEAM_NAME",
10	"TEAM_ABBREVIATION",
11	"TEAM_CODE",
12	"GAMES_PLAYED_FLAG"
]
'''
# headers, hard-coded since idk how to use enums
PERSON_ID = 0
DISPLAY_LAST_COMMA_FIRST = 1
ROSTER_STATUS = 2
FROM_YEAR = 3
TO_YEAR = 4
PLAYERCODE = 5
TEAM_ID = 6
TEAM_CITY = 7
TEAM_NAME = 8
TEAM_ABBREVIATION = 9
TEAM_CODE = 10
GAMES_PLAYED_FLAG = 11


def findPlayer(last, first):
	name = last.title().strip() + ', ' + first.title().strip()
	for player in all_players['resultSets'][0]['rowSet']:
		if name in player:
			return player
	return None

class Player:
	'''
	A class to do things with players
	'''
	def __init__(self, last, first, season=CURRENT_SEASON):
		'''
		Initialize a Player with the given attributes
		:param last: Last name, capitalization doesn't matter
		:param first: First, same as above
		:param season: The main season we want to work with (some functions may take seasons as a paramter)
		:return: self
		'''
		self._fullPlayer = findPlayer(last, first)
		if not self._fullPlayer:
			# raise error if we would not find the player
			raise LookupError('Player "' + last + ', ' + first + '" could not be found')
		self._season = season
		self._name = first + ' ' + last

	# getters
	def playerID(self):
		return self._fullPlayer[headers.PERSON_ID]

	def season(self):
		return self._season

	def name(self):
		return self._name

	def teamCode(self):
		return self._fullPlayer[headers.TEAM_ID]

	def team(self):
		return self._fullPlayer[headers.TEAM_CITY] + ' ' + self._fullPlayer[headers.TEAM_NAME]

	def teamAbbreviation(self):
		return self._fullPlayer[headers.TEAM_ABBREVIATION]

	def giveInfo(self):
		info = "Name: " + self.name()
		info += "Player ID: " + self.playerID()
		info += "Team: " + self.team()




if __name__=='__main__':
	sc = Player('curry', 'Stephen')
	print sc.giveInfo()