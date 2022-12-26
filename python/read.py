import setup
from utils import *
from IPython.display import display

sp = setup.setScope('user-library-read')

def getLikedTracks(limit_step=50) -> list:
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


def updatePlaylistCSV(filename: str):
    df = pd.read_csv(filename)  # Must not contain empty rows
    df['id'] = df.url.apply(lambda x: setup.extract_id(x))
    df['name'] = df.id.apply(lambda x: (sp.user_playlist(
        'bjorntehbear', fields='name', playlist_id=str(x)))['name'])
    df.to_csv(filename, index=False)

def getSongsFromPlaylist(playlist_row: pd.Series) -> list:
    rawList=sp.user_playlist('bjorntehbear', playlist_row['id'], fields='tracks')['tracks']['items']
    songList=formatList(rawList, playlist_row['name'])
    print("Extracting songs from ", playlist_row['name'])
    return songList

def exportAllSongs(inputfile: str, songsFileName: str):
    df=pd.read_csv(inputfile)
    newDF = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = getSongsFromPlaylist(row)
        for song in songs:
            newDF.loc[len(newDF)] = song
    newDF.to_csv(songsFileName, index=False)

def updateAndImport():
    writeCSV(getLikedTracks(), "liked.csv")
    updatePlaylistCSV('playlists/inputPlaylists.csv')
    updatePlaylistCSV('playlists/playlists.csv')
    exportAllSongs('playlists/inputPlaylists.csv', 'exports/inputsongs.csv')
    exportAllSongs('playlists/playlists.csv', 'exports/playlistSongs.csv')

def writeDuplicates(inputFile: str, outputFile: str):
    df = pd.read_csv(inputFile)
    title = df["title"] # can also use id for "true" duplicates
    x = df[title.isin(title[title.duplicated()])].sort_values("title")
    x.to_csv(outputFile)


# writeDuplicates()

df = pd.read_csv('exports/playlistSongs.csv')
rslt_df = df[df.origin.str.isalpha()]



rslt_df.to_csv('filtered/root.csv')
writeDuplicates('filtered/root.csv', 'filtered/root_duplicates.csv')