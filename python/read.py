import setup
from utils import *
from IPython.display import display


sp = setup.setScope('user-library-read')


def getLikedTracks(limit_step=50):
    tracks = []
    for offset in range(0, 10000, limit_step):
        print(offset)
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )

        if len(response['items']) == 0:
            return formatList(tracks)

        tracks.extend(response['items'])
    return formatList(tracks)


def updatePlaylistCSV(filename):
    df = pd.read_csv(filename)  # Must not contain empty rows
    df['id'] = df.url.apply(lambda x: setup.extract_id(x))
    df['name'] = df.id.apply(lambda x: (sp.user_playlist(
        'bjorntehbear', fields='name', playlist_id=str(x)))['name'])
    df.to_csv(filename, index=False)


def getSongsFromPlaylist(pl_row):
    rawList=sp.user_playlist('bjorntehbear', pl_row['id'], fields='tracks')['tracks']['items']
    songList=formatList(rawList, pl_row['name'])
    return songList


def exportAllSongs(inputfile, songsFileName):
    df=pd.read_csv(inputfile)
    newDF = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = getSongsFromPlaylist(row)
        for song in songs:
            newDF.loc[len(newDF)] = song
    newDF.to_csv(songsFileName, index=False)

def updateAndImport():
    exportCSV(getLikedTracks(), "liked")
    updatePlaylistCSV('inputPlaylists.csv')
    exportAllSongs('inputPlaylists.csv', 'exports/inputsongs.csv')
    updatePlaylistCSV('Playlists.csv')
    exportAllSongs('Playlists.csv', 'exports/playlistSongs.csv')

def duplicates():
    df = pd.read_csv('exports/playlistSongs.csv')
    title = df["title"]
    x = df[title.isin(title[title.duplicated()])].sort_values("title")
    x.to_csv('duplicates.csv')



duplicates()