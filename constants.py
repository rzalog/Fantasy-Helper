BASE_URL = 'http://stats.nba.com/stats/'
USER_AGENT = {'User-agent': 'Chrome/6.0.472.63'}

LEAGUE_ID = '00'
CURRENT_SEASON = '2015-16'
DEFAULT_SEASON_TYPE = 'Regular+Season'

##############
# PLAYER STATS HEADERS
##############
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
