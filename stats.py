#!/usr/local/bin/python

# Stats class, just holds the basic 9-cat stats (for now)

import pandas as pd

# note that this happens to be nicely ordered
VALID_STATS = ['FGM', 'FGA', 'FG_PCT', 'FTM', 'FTA',
	'FT_PCT', 'FG3M', 'REB', 'AST', 'STL', 'BLK' ,'TOV', 'PTS']


class Stats:
	'''
	Class that holds a set of 9-cat stats
	'''
	def __init__(self, stats=pd.Series(), name=None):
		'''
		:stats: parameter is a pandas.Series
		'''
		# initialize an empty stats

		if len(stats) == 0:
			# if default argument, make an empty self._stats Series
			keys = VALID_STATS
			values = [0] * len(keys)
			self._stats = pd.Series( dict(zip(keys, values)) )
		elif type(stats) != pd.Series:
			raise TypeError('stats parameter needs to be a panda.Series')
		else:
			self._stats = stats
		self._pruneStats()

	def __add__(self, other):
		# utilize pandas.Series built-in add functionality
		newStats = self.stats() + other.stats()

		FGM = 'FGM'
		FGA = 'FGA'
		FG_PCT = 'FG_PCT'

		FTM = 'FTM'
		FTA = 'FTA'
		FT_PCT = 'FT_PCT'

		# have to handle the percentages correctly, can't just add them up
		totFGM = self._stats[FGM] + other._stats[FGM]
		totFGA = self._stats[FGA] + other._stats[FGA]
		rawFG_PCT = float(totFGM) / float(totFGA)
		convertedFG_PCT = float( "{0:.3f}".format(rawFG_PCT) )
		newStats[FG_PCT] = convertedFG_PCT

		totFTM = self._stats[FTM] + other._stats[FTM]
		totFTA = self._stats[FTA] + other._stats[FTA]
		rawFT_PCT = float(totFTM) / float(totFTA)
		convertedFT_PCT = float( "{0:.3f}".format(rawFT_PCT) )
		newStats[FT_PCT] = convertedFT_PCT

		return Stats(pd.Series(newStats))

	def get(self, stat):
		if stat.upper() not in VALID_STATS:
			print 'Unable to find given stat.'
			return None
		else:
			return self._stats[stat.upper()]

	def orderedStats(self):
		'''
		- Returns a zipped up (and ordered) list of ordered stats
		- Uses standard Fantasy ESPN ordering
		- Useful for printing, among other things
		Format:
		[
			(header, stat),
			...
		]
		'''
		headers = []
		stats = []

		for stat in VALID_STATS:
			headers.append(stat)
			stats.append(self._stats[stat])

		return zip(headers, stats)

	# getters
	def stats(self):
		return self._stats

	def _pruneStats(self):
		'''
		Gets rid of all non-9-cat stats
		'''
		for header in self._stats.keys():
			if header not in VALID_STATS:
				del self._stats[header]

def printStats(stats):
	for header, stat in stats.orderedStats():
		print header + ': ' + str(stat)

if __name__=='__main__':
	from player import Player
	player = Player('Harden', 'James')
	print player._stats.stats()
	printStats(player.stats())

	# playerName1 = raw_input('First player name: ')
	# playerName2 = raw_input('Second player name: ')

	# first, last = playerName1.split()
	# player1 = Player(last, first)

	# first, last = playerName2.split()
	# player2 = Player(last, first)

	# print

	# print 'Stats for ' + player1.name() + ':'
	# printStats(player1.stats())
	# print

	# print 'Stats for ' + player2.name() + ':'
	# printStats(player2.stats())
	# print

	# print 'Combined Stats:'
	# printStats(player1.stats() + player2.stats())
	# print