import setup
from utils import *
from IPython.display import display

sp = setup.setScope('playlist-modify-public')

# lag suberset av URSUS, AVIONICS etc
# lag superset av MYSTIKK + SMELT AF + OMINOUS


def generatePlaylist(playlistName: str, playlistOverview: str): # add "tracks" dataframe
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
        row['id']



generatePlaylist('🔈 smelt mystikk', 'generated/playlistOverview.csv')


