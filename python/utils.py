import pandas as pd
import json

def formatList(inputList: str, playlist_name=' ') -> list:
    output = []
    for element in inputList:
        track = element['track']
        output.append(
            [track['name'],
            # TODO: inkluder eventuelle andre artister
            track['artists'][0]['name'],
            track['id']
            , playlist_name
            ])
    return output


def exportJSON(inputDict, filename):
    x=json.dumps(inputDict)
    with open(filename, 'w') as outfile:
        outfile.write(x)
    # return x