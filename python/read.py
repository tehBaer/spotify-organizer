import setup
from utils import *
from IPython.display import display

sp = setup.setScope('user-library-read')

def getLikedTracks(limit_step=50) -> list:
    tracks = []
    for offset in range(0, 100, limit_step):
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

def getSongsFromMultiplePlaylists(inputfile: str) -> pd.DataFrame:
    df=pd.read_csv(inputfile)
    newDF = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = getSongsFromPlaylist(row)
        for song in songs:
            newDF.loc[len(newDF)] = song
    # newDF.to_csv(songsFileName, index=False)
    return newDF

def getDuplicates(inputFile: str) -> pd.DataFrame:
    df = pd.read_csv(inputFile)
    title = df["title"] # can also use id for "true" duplicates
    return df[title.isin(title[title.duplicated()])].sort_values("title")

def getSongsInCommon(fileA: str, fileB: str) -> pd.DataFrame:
    dfa = pd.read_csv(fileA)
    dfb = pd.read_csv(fileB)

    inner = dfa.loc[dfa['title'].isin(dfb['title'])]
    inner2 = dfb.loc[dfb['title'].isin(dfa['title'])]

    return pd.concat([inner, inner2]).sort_values(by=['title'])
    
def getRootPlaylists():
    df = pd.read_csv('exports/playlistSongs.csv')
    return df[df.origin.str.isalpha()]

def updateAndImport():
    writeCSVFromList(getLikedTracks(), "likedSongs.csv")
    updatePlaylistCSV('playlists/inputPlaylists.csv')
    updatePlaylistCSV('playlists/playlists.csv')
    getSongsFromMultiplePlaylists('playlists/inputPlaylists.csv').to_csv('exports/inputSongs.csv')
    getSongsFromMultiplePlaylists('playlists/playlists.csv').to_csv('exports/playlistSongs.csv')

def analyze():
    getRootPlaylists().to_csv('filtered/root.csv', index=False)
    getDuplicates('filtered/root.csv').to_csv('filtered/root_duplicates.csv', index=False)
    getSongsInCommon('filtered/root.csv', 'exports/inputSongs.csv').to_csv('output/alreadySaved.csv', index=False)

# writeCSVFromList(getLikedTracks(), "likedSongs.csv")


pd.DataFrame(getLikedTracks(), columns=['title', 'artist', 'id', 'origin']).to_csv("likedSongs.csv", index=False)