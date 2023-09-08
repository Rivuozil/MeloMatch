import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_playlist_data(playlist_id,access_token):
    
    path_dir="D:/"
    df_name="apiProject/dataExtractor/{}_music_data.csv".format(playlist_id)
    sp=spotipy.Spotify(auth=access_token)
    
    playlist_tracks=sp.playlist_tracks(playlist_id,fields='items(track(id,name,artists,album(id,name)))')
    
    music_data=[]
    
    #playlist_name=sp.playlist(playlist_id,fields=)
    
    for track_info in playlist_tracks['items']:
        track=track_info['track']
        track_name=track['name']
        track_id=track['id']
        album_id=track['album']['id']
        album_name=track['album']['name']
        artists=",".join([artist['name']for artist in track['artists']])
        
        
        audio_features=sp.audio_features(track_id)[0] if track_id!='Not available' else None
        
        #getting album release date
        try:
            album_info=sp.album(album_id) if album_id!='Not available' else None
            release_date=album_info['release_date'] if album_info else None
        except:
            release_date=None
            
        #getting track popularity
        try:
            track_info=sp.track(track_id) if track_id!='Not available' else None
            popularity=track_info['popularity'] if track_info else None
        except:
            popularity=None
            
        #adding extra information to track data
        track_data={
            'Track name': track_name,
            'Artists':artists,
            'Album Name':album_name,
            'Album ID':album_id,
            'Track ID':track_id,
            'Popularity':popularity,
            'Release date':release_date,
            'Duration (ms)':audio_features['duration_ms'] if audio_features else None,
            'Explicit': track_info.get('explicit',None),
            'External urls':track_info['external_urls'].get('spotify',None),
            'Danceability':audio_features['danceability']if audio_features else None,
            'Energy':audio_features['energy']if audio_features else None,
            'Key':audio_features['key']if audio_features else None,
            'Loudness':audio_features['loudness']if audio_features else None,
            'Speechiness':audio_features['speechiness']if audio_features else None,
            'Mode':audio_features['mode']if audio_features else None,
            'Acousticness':audio_features['acousticness']if audio_features else None,
            'Instrumentalness':audio_features['instrumentalness']if audio_features else None,
            'Liveness':audio_features['liveness']if audio_features else None,
            'Valence':audio_features['valence']if audio_features else None,
            'Tempo':audio_features['tempo']if audio_features else None,
            
        }
        
        music_data.append(track_data)
        
    df=pd.DataFrame(music_data)
    df.to_csv(os.path.join(path_dir,df_name))
    return df
        
        