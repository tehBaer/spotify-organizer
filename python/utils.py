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


def exportJSON(inputDict, filename):
    x=json.dumps(inputDict)
    with open(filename, 'w') as outfile:
        outfile.write(x)
    # return x