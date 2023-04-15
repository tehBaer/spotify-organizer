import setup
from utils import *
from IPython.display import display
from read import GetSongsFromPlaylist, GetANotInB
import math
import random

sp = setup.setScope('playlistInfo-modify-public')
# 'bea61a6c02774488' = "bea61a6c02774488"


def GeneratePlaylist(outPlaylistName: str, tracks: list, playlistCSV: str, desc=""):
    # TODO: add "tracks" as dataframe(?)
    df = pd.read_csv(playlistCSV)
    if df[df['name'].isin([outPlaylistName])].empty:  # if playlistInfo does not exist
        response = sp.user_playlist_create('bea61a6c02774488', outPlaylistName)
        x = pd.Series([response['name'], response['external_urls']
                      ['spotify'], response['id']], index=['name', 'url', 'id'])

        df.loc[len(df)] = x
        df.to_csv(playlistCSV, index=False)
        print('\nCreating', outPlaylistName, '\n')

        # TODO: add explanation in playlist_changeclear_details()
        sp.playlist_change_details(
            x['id'], description=desc.strip("[]").replace("'", ""))
    else:
        print('\n', outPlaylistName, 'already exists\n')  # if playlistInfo exist
    
    # playListInfo is a row of the playlistInfo's name, url and id
    playlistInfo = df.loc[df['name'] == outPlaylistName].squeeze()
    UpdatePlaylist(playlistInfo, tracks)


def TrackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]




def UpdatePlaylist(playlistInfo: pd.Series, updatedTracks: list):
    
    originalTracks = GetSongsFromPlaylist(playlistInfo)
    # compare updatedTracks to current content of currentracks
    newTracks = GetANotInB(pd.Series(updatedTracks), originalTracks['id'])
    tracksToRemove = GetANotInB(originalTracks['id'], pd.Series(updatedTracks))
    print(tracksToRemove)

    # finds and removes current tracks (API throttles to 100 per call)

    while len(tracksToRemove) > 0: # TODO: only do this for songs to be removed, not everything
        tracks = TrackifyIDs(tracksToRemove)
        print("removing songs")
        next100 = tracks[:100]
        tracks = tracks[100:]
        # sp.user_playlist_add_tracks(playlistInfo['id'], tracks)
        sp.user_playlist_remove_all_occurrences_of_tracks(user = 'bea61a6c02774488', playlist_id=playlistInfo['id'], tracks=next100)
        tracksToRemove = GetANotInB(originalTracks['id'], pd.Series(updatedTracks))

    random.shuffle(newTracks)

    # add tracks
    times = math.ceil(len(newTracks) / 100)
    size2 = len(newTracks)
    for i in range(0, times):
        print("adding " + str(i+1) + "00 of " + str(size2))
        next100 = newTracks[:100]
        newTracks = newTracks[100:]
        sp.user_playlist_add_tracks('bea61a6c02774488', playlistInfo['id'], next100)
        i += 1


def CombinePlaylists(inPlaylistNames: list, outPlaylistName: str):  # TODO: add likevekt
    df = pd.read_csv('filtered/songs_root.csv')
    id_list = df.loc[df['origin'].isin(inPlaylistNames)]['id'].tolist()
    tracks = TrackifyIDs(id_list)
    # TODO: remove duplicates from tracks
    GeneratePlaylist(outPlaylistName, tracks,
                     'generated/generatedPlaylists.csv', str(inPlaylistNames))


def CreateAtomicSupersets():
    CombinePlaylists(['KAYA', 'MYSTIKK', 'RO', 'LETT RO',
                    'LETT MANTRA', 'HENGIVEN RO', 'HENGIVEN'], '🔈 mantric')

    CombinePlaylists(['THROTTLE BACK', 'THROTTLE UP', ':D', 'OMINOUS', 'MINACIOUS',
                    'OVERDRIVE', 'MALICIOUS', 'LONG-HAUL', 'DUNK DUNK DUNK DUNK', 'CREPEZILLA'], '🔈 avionics')


    CombinePlaylists(['ETHNO', 'LATINO MYSTIKK', 'ORGANIC LATINO LAXBEAT', 'ØSTLIG MYSTIKK', 'INDOARAB TRIBAL TECHNO',
                    'SYNESTHESIA', 'SOARING', 'INFECTED', 'SMELT AF', 'LOOPY AF', 'PLAYFUL', 'DANK AF', 'CHILL AF'], '🔈 hominin')

    CombinePlaylists(['THICC HAZE', 'LIGHT HAZE', 'DOPE & MOODY', 'MOODY & CHILL HAZE', 'LIGHT & CHILL HAZE'], '🔈 haze')

liked = pd.read_csv('fetched/songs_liked.csv')
root = pd.read_csv('filtered/songs_root.csv')

missing = pd.read_csv('output/missing.csv')

input = pd.read_csv('filtered/songs_input.csv')
GeneratePlaylist("<missing liked>", TrackifyIDs(missing['id']), 'generated/generatedPlaylists.csv')

# x = GetANotInB(input['id'], root['id'])
# x = GetANotInB(root['id'], input['id'])


# x = GetANotInB(root['id'], missing['id'])

# x.to_csv('output/testing.csv', index=False) # why isnt this typeset