import constants

def get_url(endpoint, **params):
	'''
	Generate a URL from given endpoint and params
	Format: 'stats.nba.com/stats/{endpoint}/?{params}'
	See https://github.com/seemethere/nba_py/wiki/stats.nba.com-Endpoint-Documentation
	for more on possible endpoints and params
	:param endpoint:	The endpoint
	:param params:		The params
	:return: URL as a string
	'''
	url = constants.BASE_URL
	url += endpoint
	url += '/?'
	for param in params.keys():
		url += param + '=' + str(params[param]) + '&'
	return url[:-1]		# get rid of the final &, to make it look pretty



if __name__=='__main__':
	print get_url('commonallplayers', LeagueID='00', Season='2015-16', IsOnlyCurrentSeason='1')