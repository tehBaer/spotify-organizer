import setup
from utils import *

sp = setup.setScope('user-library-read playlist-read-private')
username = "bjorntehbear"

def FetchAllPlaylists(amount: int) -> pd.DataFrame:
    print("\nFetching playlists: ")
    playlists=[]
    for offset in range(0, amount, 50):
        print(offset)
        response = sp.current_user_playlists(50, offset)['items']
        playlists.extend(formatPlaylists(response))
    print("Playlists fetched. ")
    return pd.DataFrame(playlists, columns=['name', 'url', 'id'])

def FetchLikedTracks(amount=10000) -> pd.DataFrame:
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


def GetSongsFromPlaylist(playlist_row: pd.Series) -> pd.DataFrame:
    # print(playlist_row)
    print("Extracting songs from ", playlist_row['name'])
    # rawList = sp.user_playlist('bjorntehbear', playlist_id=playlist_row['id'], fields='tracks')[ 
    #     'tracks']['items']
    results = sp.user_playlist_tracks(username,playlist_row['id'])
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
        print("Extracing more songs")
    
    songList = formatAndFramify(tracks, playlist_row['name'])
    return songList

# def GetSongsFromPlaylist(username: str, playlist_row: pd.Series) -> pd.DataFrame:
#     # print(playlist_row)
#     print("Extracting songs from ", playlist_row['name'])
#     # TODO: rawlist only returns 100, FIX!!!!!
#     rawList = sp.user_playlist('bjorntehbear', playlist_id=playlist_row['id'], fields='tracks')[ 
#         'tracks']['items']
#     songList = formatAndFramify(rawList, playlist_row['name'])
#     return songList



def FetchSongsFromMultiplePlaylists(playlistOverviewFile: str) -> pd.DataFrame:
    df = pd.read_csv(playlistOverviewFile)
    allSongs = pd.DataFrame(columns=['title', 'artist', 'id', 'origin'])
    for i, row in df.iterrows():
        songs = GetSongsFromPlaylist(row)
        allSongs = pd.concat([allSongs, songs], ignore_index=True)
        # print("?")
        # print(i)
    return allSongs


def GetRootPlaylists() -> pd.DataFrame:
    df = pd.read_csv('fetched/playlists_all.csv')
    startIndex = df.index[df['name']=="__start__"].tolist()[0]
    stopIndex = df.index[df['name']=="__stop__"].tolist()[0]
    return df[startIndex+1:stopIndex]

def GetAtomicPlaylists():
    df = pd.read_csv('filtered/playlists_root.csv')
    return df[df.name.str[0].str.isalpha()]

def GetInputPlaylists():
    df = pd.read_csv('fetched/playlists_all.csv')
    return df[df.name.str[0] == "["]

def GetDuplicates(songFile: str) -> pd.DataFrame:
    df = pd.read_csv(songFile)
    title = df["title"]  # can also use id for "true" duplicates
    return df[title.isin(title[title.duplicated()])].sort_values("title")

def GetANotInB(aTracks: pd.Series, bTracks: pd.Series) -> pd.Series:
    # returns tracks from aTracks that are not in bTracks
    print(aTracks)
    print(bTracks)
    x = ~aTracks.isin(bTracks)
    return aTracks[x]




def GetSongsInCommon(fileA: str, fileB: str) -> pd.DataFrame:
    dfa = pd.read_csv(fileA)
    dfb = pd.read_csv(fileB)

    inner = dfa.loc[dfa['title'].isin(dfb['title'])]
    inner2 = dfb.loc[dfb['title'].isin(dfa['title'])]

    return pd.concat([inner, inner2]).sort_values(by=['title'])


def GetMissingLiked():
    liked = pd.read_csv('fetched/songs_liked.csv')
    atmoified = pd.read_csv('filtered/songs_atomic.csv')
    inputSongs = pd.read_csv('filtered/songs_input.csv')

    missing1 = liked.loc[~liked['title'].isin(atmoified['title'])]
    missing = missing1.loc[~missing1['title'].isin(inputSongs['title'])] # Funker denne?
    # TODO check if Pink Floyd
    return missing


def FetchAndFilter():
    print("A")
    FetchAllPlaylists(1000).to_csv('fetched/playlists_all.csv', index=False)

    print("B")
    GetRootPlaylists().to_csv('filtered/playlists_root.csv', index=False)
    print("C")
    GetAtomicPlaylists().to_csv('filtered/playlists_atomic.csv', index=False)
    print("D")
    GetInputPlaylists().to_csv('filtered/playlists_input.csv', index=False)

    print("E")
    FetchLikedTracks().to_csv("fetched/songs_liked.csv", index=False)

    print("F")
    FetchSongsFromMultiplePlaylists(
        'filtered/playlists_root.csv').to_csv('filtered/songs_root.csv', index=False)

    # TODO: ineffektivt. De to neste burde filtrere, ikke fetche alle sangene på nytt
    print("G")
    FetchSongsFromMultiplePlaylists(
        'filtered/playlists_atomic.csv').to_csv('filtered/songs_atomic.csv', index=False)

    print("H")
    FetchSongsFromMultiplePlaylists(
        'filtered/playlists_input.csv').to_csv('filtered/songs_input.csv', index=False)

def Analyze():
    GetDuplicates(
        'filtered/songs_atomic.csv').to_csv('output/songs_atomic_duplicates.csv', index=False)
    GetSongsInCommon('filtered/songs_atomic.csv',
                     'filtered/songs_input.csv').to_csv('output/alreadySaved.csv', index=False)
    GetMissingLiked().to_csv('output/missing.csv', index=False)


