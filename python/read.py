import setup
from utils import *
from IPython.display import display

sp = setup.setScope('user-library-read playlist-read-private')

def fetchAllPlaylists(amount: int):
    print("\nFetching playlists: ")
    playlists=[]
    for offset in range(0, amount, 50):
        print(offset)
        response = sp.current_user_playlists(50, offset)['items']
        playlists.extend(formatPlaylists(response))
    print("Playlists fetched. ")
    return pd.DataFrame(playlists, columns=['name', 'url', 'id'])

def fetchLikedTracks(amount=10000) -> pd.DataFrame:
    print("\nFetching liked tracks: ")

    limit_step = 50
    tracks = []
    for offset in range(0, amount, limit_step):
        print(offset)
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )

        if len(response['items']) == 0:
            print("Liked tracks fetched. ")
            return formatAndFramify(tracks)

        tracks.extend(response['items'])
    print("Liked tracks fetched. ")

    return formatAndFramify(tracks)


def getSongsFromPlaylist(playlist_row: pd.Series) -> pd.DataFrame:
    print("Extracting songs from ", playlist_row['name'])
    rawList = sp.user_playlist('bjorntehbear', playlist_row['id'], fields='tracks')[
        'tracks']['items']
    songList = formatAndFramify(rawList, playlist_row['name'])
    return songList


def fetchSongsFromMultiplePlaylists(playlistOverviewFile: str) -> pd.DataFrame:
    df = pd.read_csv(playlistOverviewFile)
    allSongs = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = getSongsFromPlaylist(row)
        allSongs = pd.concat([allSongs, songs], ignore_index=True)
        print("?")
        print(i)
    return allSongs


def getDuplicates(songFile: str) -> pd.DataFrame:
    df = pd.read_csv(songFile)
    title = df["title"]  # can also use id for "true" duplicates
    return df[title.isin(title[title.duplicated()])].sort_values("title")

def getRootPlaylists() -> pd.DataFrame:
    df = pd.read_csv('exports/playlistLibrary.csv')
    startIndex = df.index[df['name']=="__start__"].tolist()[0]
    stopIndex = df.index[df['name']=="__stop__"].tolist()[0]
    return df[startIndex+1:stopIndex]

def getAtomicPlaylists():
    df = pd.read_csv('exports/playlistSongs.csv')
    return df[df.origin.str[0].str.isalpha()]


def getSongsInCommon(fileA: str, fileB: str) -> pd.DataFrame:
    dfa = pd.read_csv(fileA)
    dfb = pd.read_csv(fileB)

    inner = dfa.loc[dfa['title'].isin(dfb['title'])]
    inner2 = dfb.loc[dfb['title'].isin(dfa['title'])]

    return pd.concat([inner, inner2]).sort_values(by=['title'])


def getMissingLiked():
    liked = pd.read_csv('exports/likedSongs.csv')
    atmoified = pd.read_csv('filtered/atomic.csv')
    missing = liked.loc[~liked['title'].isin(atmoified['title'])]
    return missing


def fetchAndFilter():
    fetchAllPlaylists(1000).to_csv('exports/playlistLibrary.csv', index=False)
    getRootPlaylists().to_csv('filtered/root.csv', index=False)
    getAtomicPlaylists().to_csv('filtered/atomic.csv', index=False)

    fetchLikedTracks().to_csv("exports/likedSongs.csv", index=False)

    fetchSongsFromMultiplePlaylists(
        'playlists/inputPlaylists.csv').to_csv('exports/inputSongs.csv', index=False)
    fetchSongsFromMultiplePlaylists(
        'playlists/playlists.csv').to_csv('exports/playlistSongs.csv', index=False)

def analyze():
    getDuplicates(
        'filtered/atomic.csv').to_csv('filtered/atomic_duplicates.csv', index=False)
    getSongsInCommon('filtered/atomic.csv',
                     'exports/inputSongs.csv').to_csv('output/alreadySaved.csv', index=False)
    getMissingLiked().to_csv('output/missing.csv', index=False)

# fetchAllPlaylists(1000).to_csv('exports/playlistLibrary.csv', index=False)

getRootPlaylists().to_csv("testing.csv", index=False)