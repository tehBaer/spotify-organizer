import pandas as pd
import json


# def formatTracks(inputDict):
#     output = []
#     for idx, item in enumerate(inputDict['items']):
#         track = item['track']
#         output.append(
#             [track['name'],
#             # TODO: inkluder eventuelle andre artister
#             track['artists'][0]['name'],
#             track['id']])
#     return output

def formatList(input, playlist_name=' '):
    output = []
    for element in input:
        track = element['track']
        output.append(
            [track['name'],
            # TODO: inkluder eventuelle andre artister
            track['artists'][0]['name'],
            track['id']
            , playlist_name
            ])
    return output

def exportCSV(inputList, fileName):
    df = pd.DataFrame(inputList)#, columns=['Title', 'Creator', 'id'])
    df.to_csv('exports/' + fileName + '.csv')


def exportJSON(inputDict, filename):
    x=json.dumps(inputDict)
    with open(filename, 'w') as outfile:
        outfile.write(x)
    # return x