import setup
from utils import *
from IPython.display import display
from read import *

sp = setup.setScope('playlist-modify-public')

# lag suberset av URSUS, AVIONICS etc
# lag superset av MYSTIKK + SMELT AF + OMINOUS

def generatePlaylist(playlistName: str, tracks: list, playlistOverview: str): # add "tracks" dataframe
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
    playlist_row = df.loc[df['name']==playlistName].squeeze()
    addTracks('bjorntehbear', playlist_row, tracks)



def trackifyIDs(id_list: list) -> list:
    return ["spotify:track:" + track for track in id_list]


def addTracks(username: str, playlistRow:pd.Series, trackList:list):
    
    # find and remove current tracks
    currentTracks = getSongsFromPlaylist(playlistRow)
    xy = trackifyIDs(currentTracks['id'])
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlistRow['id'], xy)
        
    # TODO for each 100 tracks
        # add them to the playlist
    
    sp.user_playlist_add_tracks(username, playlistRow['id'], trackList)


def combinePlaylists(playlistNames: list, playlistName:str):
    df=pd.read_csv('exports/playlistSongs.csv')
    id_list=df.loc[df['origin'].isin(playlistNames)]['id'].tolist()
    tracks=trackifyIDs(id_list)
    generatePlaylist(playlistName, tracks, 'generated/generatedPlaylists.csv')

combinePlaylists(['MYSTIKK', 'RO'], '🔈 mystikk ro')

