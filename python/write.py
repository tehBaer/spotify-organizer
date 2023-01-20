import setup
from utils import *
from IPython.display import display
# from read import *
import read
import math
import random

sp = setup.setScope('playlist-modify-public')


def generatePlaylist(playlistName: str, tracks: list, playlistOverview: str, desc=""):
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
    addTracks('bjorntehbear', playlist_row, tracks)


def trackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]


def addTracks(username: str, playlistRow: pd.Series, trackList: list):
    random.shuffle(trackList)

    # API caps at 100 at a time
    # finds and removes current tracks
    currentTracks = read.getSongsFromPlaylist(playlistRow)
    i=1
    while len(currentTracks) > 0:
        tracks = trackifyIDs(currentTracks['id'])
        print("removing " + str(i+1) + "00 songs")
        i+=1
        next100 = tracks[:100]
        tracks = tracks[100:]
        # sp.user_playlist_add_tracks(username, playlistRow['id'], tracks)
        sp.user_playlist_remove_all_occurrences_of_tracks(
            username, playlistRow['id'], next100)
        currentTracks = read.getSongsFromPlaylist(playlistRow)

    # add tracks
    times = math.ceil(len(trackList) / 100)
    size2 = len(trackList)
    for i in range(0, times):
        print("adding " + str(i+1) + "00 of " + str(size2))
        next100 = trackList[:100]
        trackList = trackList[100:]
        sp.user_playlist_add_tracks(username, playlistRow['id'], next100)
        i += 1


def combinePlaylists(playlistNames: list, playlistName: str):  # TODO: add likevekt
    df = pd.read_csv('filtered/songs_root.csv')
    id_list = df.loc[df['origin'].isin(playlistNames)]['id'].tolist()
    tracks = trackifyIDs(id_list)
    # TODO: remove duplicates from tracks
    generatePlaylist(playlistName, tracks,
                     'generated/generatedPlaylists.csv', str(playlistNames))


def createAtomicSupersets():
    combinePlaylists(['KAYA', 'MYSTIKK', 'RO', 'LETT RO',
                    'LETT MANTRA', 'HENGIVEN RO', 'HENGIVEN'], '🔈 mantric')

    combinePlaylists(['THROTTLE BACK', 'THROTTLE UP', ':D', 'OMINOUS', 'MINACIOUS',
                    'OVERDRIVE', 'MALICIOUS', 'LONG-HAUL', 'DUNK DUNK DUNK DUNK', 'CREPEZILLA'], '🔈 avionics')


    combinePlaylists(['ETHNO', 'LATINO MYSTIKK', 'ORGANIC LATINO LAXBEAT', 'ØSTLIG MYSTIKK', 'INDOARAB TRIBAL TECHNO',
                    'SYNESTHESIA', 'SOARING', 'INFECTED', 'SMELT AF', 'LOOPY AF', 'PLAYFUL', 'DANK AF', 'CHILL AF'], '🔈 hominin')

    combinePlaylists(['THICC HAZE', 'LIGHT HAZE', 'DOPE & MOODY', 'MOODY & CHILL HAZE', 'LIGHT & CHILL HAZE'], '🔈 haze')

missingDF = pd.read_csv('output/missing.csv')
generatePlaylist("<missing liked>", trackifyIDs(missingDF['id']), 'generated/generatedPlaylists.csv')

# combinePlaylists(['DOPE & MOODY', 'MOODY & CHILL HAZE', 'LIGHT & CHILL HAZE'], '🔈 HERO REALMS 2')