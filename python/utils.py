import pandas as pd
import json

def formatAndFramify(inputList: str, playlist_name=' ') -> pd.DataFrame:
    output = []
    for element in inputList:
        track = element['track']
        output.append(
            [track['name'],
            track['artists'][0]['name'],# TODO: inkluder alle artister i samme celel

            track['id']
            , playlist_name
            ])
    return pd.DataFrame(output, columns=['title', 'artist', 'id', 'origin'])

def formatPlaylists(playlistList: list) -> pd.DataFrame:
    output = []
    for playlist in playlistList:
        output.append([playlist['name'], playlist['external_urls']['spotify'], playlist['id']])
    return output

def exportJSON(inputDict, filename): #helper function for coding
    x=json.dumps(inputDict)
    with open(filename, 'w') as outfile:
        outfile.write(x)
