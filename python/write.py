import setup
from utils import *
from IPython.display import display
from read import *
import math

sp = setup.setScope('playlist-modify-public')

# lag suberset av URSUS, AVIONICS etc
# lag superset av MYSTIKK + SMELT AF + OMINOUS


# add "tracks" dataframe
def generatePlaylist(playlistName: str, tracks: list, playlistOverview: str):
    df = pd.read_csv(playlistOverview)
    if df[df['name'].isin([playlistName])].empty:  # if playlist does not exist
        response = sp.user_playlist_create('bjorntehbear', playlistName)
        x = pd.Series([response['name'], response['external_urls']
                      ['spotify'], response['id']], index=['name', 'url', 'id'])

        df.loc[len(df)] = x
        df.to_csv(playlistOverview, index=False)
        print('\nCreating', playlistName, '\n')
    else:
        print('\n', playlistName, 'already exists\n')  # if playlist exist
    playlist_row = df.loc[df['name'] == playlistName].squeeze()
    addTracks('bjorntehbear', playlist_row, tracks)


def trackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]


def addTracks(username: str, playlistRow: pd.Series, trackList: list):
    # finds and removes current tracks
    currentTracks = getSongsFromPlaylist(playlistRow)
    tracks = trackifyIDs(currentTracks['id'])


    sp.user_playlist_remove_all_occurrences_of_tracks(
        username, playlistRow['id'], tracks)

    fre = len(trackList)
    # print('\n\n\n', fre, '\n\n\n')
    times = math.ceil(fre / 100)
    for i in range(0, times):
        next100 = trackList[:100]
        trackList = trackList[100:]
        sp.user_playlist_add_tracks(username, playlistRow['id'], next100)
        i += 1


    # TODO for each 100 tracks
        # add them to the playlist


def combinePlaylists(playlistNames: list, playlistName: str):
    df = pd.read_csv('exports/playlistSongs.csv')
    id_list = df.loc[df['origin'].isin(playlistNames)]['id'].tolist()
    tracks = trackifyIDs(id_list)
    generatePlaylist(playlistName, tracks, 'generated/generatedPlaylists.csv')


combinePlaylists(['MYSTIKK', 'OMINOUS'], '🔈 mystikk ominous')
