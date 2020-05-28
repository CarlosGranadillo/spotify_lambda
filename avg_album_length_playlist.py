import spotipy
import pandas as pd
import matplotlib.pyplot as plt

from tools.playlists import get_artists_from_playlist

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())


RapCaviar = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'
MikesPlaylist = 'spotify:playlist:15hANlFzdsdscdnOzy87pp'
DriveHood = 'spotify:playlist:1uM1laLmdeCMRQoYC1gybB'


# artists = {'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x': 'Kanye West',
#            'spotify:artist:3TVXtAsR1Inumwj472S9r4': 'Drake'}
# artists = {'spotify:artist:2AfU5LYBVCiCtuCCfM7uVX': 'Kota The Friend',
#            'spotify:artist:6fxyWrfmjcbj5d12gXeiNV': 'Denzel Curry'}

artists = get_artists_from_playlist(RapCaviar)

# artists = {'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x': 'Kanye West'}
#
# artists = {'spotify:artist:3TVXtAsR1Inumwj472S9r4': 'Drake'}

final_data_dictionary = {'Year Released': [],
                         'Album Length': [],
                         'Album Name': []}

# For every artist we're looking for
for artist in artists.keys():
    artists_albums = spotify.artist_albums(artist, album_type='album', limit=50)
    # For all of their albums
    for album in artists_albums['items']:
        if 'GB' in artists_albums['items'][0]['available_markets']:
            album_data = spotify.album(album['uri'])
            # For every song in the album
            album_length_ms = 0
            for song in album_data['tracks']['items']:
                # TODO consider album popularity
                album_length_ms = song['duration_ms'] + album_length_ms
            final_data_dictionary['Album Length'].append(album_length_ms)
            final_data_dictionary['Year Released'].append(album_data['release_date'][:4])
            final_data_dictionary['Album Name'].append(album_data['name'])

print(final_data_dictionary['Album Length'])
print(final_data_dictionary['Year Released'])
print(final_data_dictionary['Album Name'])

df = pd.DataFrame(data=final_data_dictionary)
df = df.set_index('Year Released')
df = df.drop_duplicates(subset='Album Name')
df = df.mean(level=0) # Average of album length by index
df = df.sort_index()
df['Album Length'] = df['Album Length']*0.0000002777778
chart = df.plot(use_index=True, y='Album Length', kind='bar', legend=False)
chart.set_ylabel("Average Album Length (hours)")
chart.set_xlabel("Year Released")
plt.show()

