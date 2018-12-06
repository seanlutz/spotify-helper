import spotipy
import spotipy.util
import time
import io
import personal
username = personal.username



def returnListApiCall(function, arg, numberPerCall):
	resultList = []
	ans = []
	doWhile = True
	off = 0
	while(doWhile):
		ans = function(username,arg,offset = off)
		resultList = resultList + ans['items']
		off += numberPerCall 
		doWhile = not (len(ans['items']) == 0)
	return resultList



def listApiCallReturnList(function, args, numberPerCall):
	start = 0
	end = 0
	resultList = []
	keyName = ""
	while(end <= len(args)):
		end += numberPerCall
		# print(end)
		callResult = function(args[start:end])
		if resultList == []:
			resultList = callResult
			keyName = list(resultList.keys())[0]
		else: 
			for item in callResult[keyName]:
				resultList[keyName].append(item)
		start += numberPerCall
	return resultList

def listApiCallNoReturn(function, playlist, args,  numberPerCall):
	start = 0
	end = 0
	keyName = ""
	print(type(args))
	while(end < len(args)):
		end += numberPerCall
		# print(end)
		print(username)
		print(playlist)
		print(args)
		print(args[start:end])
		print()
		callResult = function(username,playlist, args[start:end])
		start += numberPerCall

def getSpotifyObj():

	SPOTIPY_CLIENT_ID = personal.SPOTIPY_CLIENT_ID
	SPOTIPY_CLIENT_SECRET =personal.SPOTIPY_CLIENT_SECRET
	SPOTIPY_REDIRECT_URI ='http://127.0.0.1'
	scope = 'playlist-modify-private user-read-private playlist-modify-public'
	token = spotipy.util.prompt_for_user_token(username,
										   scope,
										   client_id=SPOTIPY_CLIENT_ID ,
										   client_secret=SPOTIPY_CLIENT_SECRET,
										   redirect_uri=SPOTIPY_REDIRECT_URI)
	if token:
		return spotipy.Spotify(token)

	else:
		print(":(")

def getPlaylistId(spotify, username, playlistName):
	playlists = spotify.user_playlists(username)
	chosenPlaylistID = ''
	for i in playlists['items']:
		if i['name'] == playlistName:
			return i['id']



def getArtistIDsFromPlaylist(spotify,username,playlistName):
	chosenPlaylistTracks = getTracksFromPlaylist(spotify,username,playlistName)
	# chosenPlaylistTracks = spotify.user_playlist_tracks(username,chosenPlaylistID,offset = 1000)
	artistIDs = []
	file = io.open('artistIDs.txt', 'w')
	for i in chosenPlaylistTracks:
		artistIDs.append(i['track']['artists'][0]['id'])
		file.write(u"{}\n".format(i['track']['artists'][0]['id']))
	file.close()
	return artistIDs

def getTracksFromPlaylist(spotify,username,playlistName):
	chosenPlaylistID = getPlaylistId(spotify, username, playlistName)
	return returnListApiCall(spotify.user_playlist_tracks, chosenPlaylistID, 99)



#genres == list of genres to test for 
def filterTracksByGenre(spotify,username,tracks,genres):
	artistIDs = list(map(lambda i:i['track']['artists'][0]['id'], tracks))
	artistsInfo = listApiCallReturnList(spotify.artists, artistIDs, 50) 
	# print("there are {} artists here in the original".format(len(artistsInfo['artists'])))
	genreArtistIds = []

	for artist in artistsInfo['artists']:
		found = False
		for genreString in artist['genres']:
			if found:
				break
			for targetGenre in genres:
				if targetGenre in genreString:
					genreArtistIds.append(artist['id'])
					found = True
					break
	return list(filter(lambda track: track['track']['artists'][0]['id'] in genreArtistIds, tracks ))

def removeTracksFromPlaylist(spotify,username,fromPlaylistName, tracks):
	listApiCallNoReturn(spotify.user_playlist_remove_all_occurrences_of_tracks, getPlaylistId(spotify, username, fromPlaylistName), tracks, 50)
def addTracksToPlaylist(spotify,username,toPlaylistName, tracks):
	listApiCallNoReturn(spotify.user_playlist_add_tracks,
	 getPlaylistId(spotify, username, toPlaylistName), tracks, 49)
def uselessWrapper():
	return spotify.user_playlist_remove_specific_occurrences_of_tracks(spotify,username,'test123', params[:50])