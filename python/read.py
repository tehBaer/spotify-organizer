import setup
from utils import *
from IPython.display import display

sp = setup.setScope('user-library-read playlist-read-private')

def fetchPlaylists(amount: int):
    playlists=[]
    for offset in range(0, amount, 50):
        response = sp.current_user_playlists(50, offset)['items']
        playlists.extend(formatPlaylists(response))
    return pd.DataFrame(playlists, columns=['name', 'url', 'id'])

def getLikedTracks(amount=10000) -> pd.DataFrame:
    limit_step = 50
    tracks = []
    for offset in range(0, amount, limit_step):
        print(offset)
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )

        if len(response['items']) == 0:
            return formatAndFramify(tracks)

        tracks.extend(response['items'])
    return formatAndFramify(tracks)


def getSongsFromPlaylist(playlist_row: pd.Series) -> pd.DataFrame:
    rawList = sp.user_playlist('bjorntehbear', playlist_row['id'], fields='tracks')[
        'tracks']['items']
    songList = formatAndFramify(rawList, playlist_row['name'])
    print("Extracting songs from ", playlist_row['name'])
    return songList


def getSongsFromMultiplePlaylists(playlistOverviewFile: str) -> pd.DataFrame:
    df = pd.read_csv(playlistOverviewFile)
    allSongs = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = getSongsFromPlaylist(row)
        allSongs = pd.concat([allSongs, songs], ignore_index=True)
        # print(i)
    return allSongs


def getDuplicates(songFile: str) -> pd.DataFrame:
    df = pd.read_csv(songFile)
    title = df["title"]  # can also use id for "true" duplicates
    return df[title.isin(title[title.duplicated()])].sort_values("title")


def getRootPlaylists():
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
    rooted = pd.read_csv('filtered/root.csv')
    missing = liked.loc[~liked['title'].isin(rooted['title'])]
    return missing


def updateAndImport():
    getLikedTracks().to_csv("exports/likedSongs.csv", index=False)
    getSongsFromMultiplePlaylists(
        'playlists/inputPlaylists.csv').to_csv('exports/inputSongs.csv', index=False)
    getSongsFromMultiplePlaylists(
        'playlists/playlists.csv').to_csv('exports/playlistSongs.csv', index=False)


def analyze():
    getRootPlaylists().to_csv('filtered/root.csv', index=False)
    getDuplicates(
        'filtered/root.csv').to_csv('filtered/root_duplicates.csv', index=False)
    getSongsInCommon('filtered/root.csv',
                     'exports/inputSongs.csv').to_csv('output/alreadySaved.csv', index=False)
    getMissingLiked().to_csv('output/missing.csv', index=False)


x = fetchPlaylists(1000)
