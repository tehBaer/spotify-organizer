import setup
from utils import *
from IPython.display import display
from read import GetSongsFromPlaylist, GetANotInB, FetchAndFilter, Analyze
import math
import random

sp = setup.setScope('playlist-modify-public')
username = 'bjorntehbear'


def GeneratePlaylist(outPlaylistName: str, tracks: list, playlistCSV: str, desc=""):
    # TODO: add "tracks" as dataframe(?)
    df = pd.read_csv(playlistCSV)
    if df[df['name'].isin([outPlaylistName])].empty:  # if playlistInfo does not exist
        response = sp.user_playlist_create(username, outPlaylistName)
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
    playlist_row = df.loc[df['name'] == outPlaylistName].squeeze()
    UpdatePlaylist('bjorntehbear', playlist_row, tracks)


def TrackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]




def UpdatePlaylist(username: str, playlistInfo: pd.Series, updatedTracks: list):
    
    originalTracks = GetSongsFromPlaylist(playlistInfo) # only outputs 100
    print("number of original tracks", len(originalTracks))

    print("number of updated tracks", len(updatedTracks))

    newTracks = GetANotInB(pd.Series(updatedTracks), pd.Series(TrackifyIDs(originalTracks['id'])))
    print("new tracks to add: ", len(newTracks))
    # display(originalTracks)

    # tracksToRemove = GetANotInB(originalTracks['id'], pd.Series(updatedTracks))
    # print("tracks to remove: ", len(tracksToRemove))

    # trackIDsToRemove = TrackifyIDs(tracksToRemove)
    # while len(trackIDsToRemove) > 0: # TODO: only do this for songs to be removed, not everything
    #     next100 = trackIDsToRemove[:100]
    #     print("removing ", len(next100),  "songs")
    #     sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id=playlistInfo['id'], tracks=next100)
    #     trackIDsToRemove = trackIDsToRemove[100:]

    random.shuffle(newTracks)

    # add tracks
    times = math.ceil(len(newTracks) / 100)
    size2 = len(newTracks)
    for i in range(0, times):
        print("adding " + str(i+1) + "00 of " + str(size2))
        next100 = newTracks[:100]
        newTracks = newTracks[100:]
        sp.user_playlist_add_tracks(username, playlistInfo['id'], next100)
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


# FetchAndFilter()
# Analyze()

# liked = pd.read_csv('fetched/songs_liked.csv')
# root = pd.read_csv('filtered/songs_root.csv')
# atomic = pd.read_csv('filtered/songs_atomic.csv')
# missing = pd.read_csv('output/missing.csv')
# GeneratePlaylist("<missing liked>", TrackifyIDs(missing['id']), 'generated/generatedPlaylists.csv')

df = pd.read_csv('filtered/songs_root.csv')
new_id_list = df.loc[df['origin'].isin(['new'])]['id'].tolist()
print(new_id_list)
GeneratePlaylist("oldAndNew", TrackifyIDs(new_id_list), 'generated/generatedPlaylists.csv')


# input = pd.read_csv('filtered/songs_input.csv')

# x = GetANotInB(input['id'], atomic['id'])
# x = GetANotInB(atomic['id'], input['id'])


# x = GetANotInB(atomic['id'], missing['id'])

# x.to_csv('output/testing.csv', index=False) # why isnt this typeset