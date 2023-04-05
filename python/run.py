from read import fetchAndFilter, analyze, getMissingLiked
from write import generatePlaylist, trackifyIDs, createAtomicSupersets, combinePlaylists
import pandas as pd
from setup import setScope

sp = setScope('user-library-read playlist-read-private playlist-modify-public')

### READ

# fetchAndFilter()
# analyze()
# getMissingLiked().to_csv('output/missing.csv', index=False)
# print("DONE")

"""Sonic Riots og Eoth var på 'missing liked'"""


##### WRITE
missingDF = pd.read_csv('output/missing.csv')
generatePlaylist("<missing liked>", trackifyIDs(missingDF['id']), 'generated/generatedPlaylists.csv')

# createAtomicSupersets();

# combinePlaylists(['DOPE & MOODY', 'MOODY & CHILL HAZE', 'LIGHT & CHILL HAZE'], '🔈 HERO REALMS 2')