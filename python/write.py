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
    row = df.loc[df['name']==playlistName]
    sp.user_playlist_replace_tracks('bjorntehbear', row['id'][0], tracks) # why [0]?





df=pd.read_csv('exports/playlistSongs.csv')
# id_list=df.loc[df['origin']=='MYSTIKK']['id'].tolist()
id_list=df.loc[df['origin'].isin(['MYSTIKK', 'RO'])]['id'].tolist()

tracks=(["spotify:track:" + track for track in id_list])

generatePlaylist('🔈 smelt mystikk', tracks, 'generated/generatedPlaylists.csv')


