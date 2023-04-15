import setup
from utils import *
from IPython.display import display
from read import getSongsFromPlaylist
import math
import random

sp = setup.setScope('playlist-modify-public')


def GeneratePlaylist(playlistName: str, tracks: list, playlistOverview: str, desc=""):
    # TODO: add "tracks" as dataframe(?)
    df = pd.read_csv(playlistOverview)
    if df[df['name'].isin([playlistName])].empty:  # if playlist does not exist
        response = sp.user_playlist_create('bjorntehbear', playlistName)
        x = pd.Series([response['name'], response['external_urls']
                      ['spotify'], response['id']], index=['name', 'url', 'id'])

        df.loc[len(df)] = x
        df.to_csv(playlistOverview, index=False)
        print('\nCreating', playlistName, '\n')

        # TODO: add explanation in playlist_changeclear_details()
        sp.playlist_change_details(
            x['id'], description=desc.strip("[]").replace("'", ""))
    else:
        print('\n', playlistName, 'already exists\n')  # if playlist exist
    playlist_row = df.loc[df['name'] == playlistName].squeeze()
    AddTracks('bjorntehbear', playlist_row, tracks)


def TrackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]


def AddTracks(username: str, playlist: pd.Series, tracksToAdd: list):
    random.shuffle(tracksToAdd)
    # finds and removes current tracks (API throttles to 100 per call)
    currentTracks = getSongsFromPlaylist(playlist)
    i=1
    while len(currentTracks) > 0: # TODO: only do this for songs to be removed, not everything
        tracks = TrackifyIDs(currentTracks['id'])
        print("removing " + str(i+1) + "00 songs")
        i+=1
        next100 = tracks[:100]
        tracks = tracks[100:]
        # sp.user_playlist_add_tracks(username, playlist['id'], tracks)
        sp.user_playlist_remove_all_occurrences_of_tracks(
            username, playlist['id'], next100)
        currentTracks = getSongsFromPlaylist(playlist)

    # add tracks
    times = math.ceil(len(tracksToAdd) / 100)
    size2 = len(tracksToAdd)
    for i in range(0, times):
        print("adding " + str(i+1) + "00 of " + str(size2))
        next100 = tracksToAdd[:100]
        tracksToAdd = tracksToAdd[100:]
        sp.user_playlist_add_tracks(username, playlist['id'], next100)
        i += 1


def CombinePlaylists(playlistNames: list, playlistName: str):  # TODO: add likevekt
    df = pd.read_csv('filtered/songs_root.csv')
    id_list = df.loc[df['origin'].isin(playlistNames)]['id'].tolist()
    tracks = TrackifyIDs(id_list)
    # TODO: remove duplicates from tracks
    GeneratePlaylist(playlistName, tracks,
                     'generated/generatedPlaylists.csv', str(playlistNames))


def createAtomicSupersets():
    CombinePlaylists(['KAYA', 'MYSTIKK', 'RO', 'LETT RO',
                    'LETT MANTRA', 'HENGIVEN RO', 'HENGIVEN'], '🔈 mantric')

    CombinePlaylists(['THROTTLE BACK', 'THROTTLE UP', ':D', 'OMINOUS', 'MINACIOUS',
                    'OVERDRIVE', 'MALICIOUS', 'LONG-HAUL', 'DUNK DUNK DUNK DUNK', 'CREPEZILLA'], '🔈 avionics')


    CombinePlaylists(['ETHNO', 'LATINO MYSTIKK', 'ORGANIC LATINO LAXBEAT', 'ØSTLIG MYSTIKK', 'INDOARAB TRIBAL TECHNO',
                    'SYNESTHESIA', 'SOARING', 'INFECTED', 'SMELT AF', 'LOOPY AF', 'PLAYFUL', 'DANK AF', 'CHILL AF'], '🔈 hominin')

    CombinePlaylists(['THICC HAZE', 'LIGHT HAZE', 'DOPE & MOODY', 'MOODY & CHILL HAZE', 'LIGHT & CHILL HAZE'], '🔈 haze')

# missingDF = pd.read_csv('output/missing.csv')
# GeneratePlaylist("<missing liked>", TrackifyIDs(missingDF['id']), 'generated/generatedPlaylists.csv')