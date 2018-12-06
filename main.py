import spotipy
import spotipy.util
import time
import functions as fn
import personal
username = personal.username





spotify = fn.getSpotifyObj()

def likesFilterAndClear(number):
	likesSongs = fn.getTracksFromPlaylist(spotify,username,'Likes')[:-number]
	likesSongsIds = map(lambda x: x['track']['id'], likesSongs)
	if len(likesSongs) > 0:
		dupSongs = fn.getTracksFromPlaylist(spotify,username,'Country')
		dupSongsIds = map(lambda x: x['track']['id'], dupSongs)
		dups = {}
		for i in range(len(dupSongsIds)):
			if dupSongsIds[i] in dups:
				dups[dupSongsIds[i]].append(i)
			else:
				dups[dupSongsIds[i]] = [i]
		removeList = [i for i in dups if len(dups[i]) >1 ]
		likesSongsIds = [i for i in likesSongsIds if i not in removeList]

		if len(likesSongsIds) > 0:

			fn.addTracksToPlaylist(spotify,username,'Likes Archive', likesSongsIds)
			fn.addTracksToPlaylist(spotify,username,'Country', 
				map(lambda x: x['track']['id'], 
					fn.filterTracksByGenre(spotify,username,likesSongs,['country']
						)))
			fn.removeTracksFromPlaylist(spotify,username,'Likes', likesSongsIds)

def deleteDups(playName):
	dupSongs = fn.getTracksFromPlaylist(spotify,username,playName)
	dupSongsIds = map(lambda x: x['track']['id'], dupSongs)
	dups = {}
	for i in range(len(dupSongsIds)):
		if dupSongsIds[i] in dups:
			dups[dupSongsIds[i]].append(i)
		else:
			dups[dupSongsIds[i]] = [i]
	removeList = [i for i in dups if len(dups[i]) >1 ]
	if removeList ==[]:
		exit() 
	print(removeList)
	cleardupe = fn.getTracksFromPlaylist(spotify,username,'dupes')
	clearerdupe = map(lambda x: x['track']['id'], cleardupe)
	fn.removeTracksFromPlaylist(spotify,username,'dupes', clearerdupe)
	fn.addTracksToPlaylist(spotify,username,'dupes', removeList)
	fn.removeTracksFromPlaylist(spotify,username,playName, removeList)
	fn.addTracksToPlaylist(spotify,username,playName, removeList)
	params =[]
	for i in dups:
		if len(dups[i]) > 1:
			for j in dups[i][1:]:
				params.append({'uri':i , 'positions':[j]})
	params = newlist = sorted(params, key=lambda x: x['positions'][0]) 
	params = list(reversed(params))
	while len(params) != 0:
		print params[:1]
		##
		try:
			spotify.user_playlist_remove_specific_occurrences_of_tracks(username, fn.getPlaylistId(spotify, username, 'Country') , params[:1])
		except:
			print('can you pls stop showing tracks that dont exist in here spotify love you <3 ')
			break
		del params[:50]



likesFilterAndClear(40)