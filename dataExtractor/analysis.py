
from features import get_playlist_data
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

#creating dataframe of music data playlist
playlist_id='3kFuz3maIU15tZxlbfpGJW'
#mention the current access token
access_token='BQD0AdXHZ9QKF3VOVY0PHr_svlJuBcxU6YIOEC6KKIQPo_3MQqRILSMuFzR7r2DktD5FABUYiR-jGM0b9eu6VIEKoG-Y-Nk-lWkwYXlO99B4KrtIVwI'
music_df=get_playlist_data(playlist_id, access_token)

print(music_df)

#checking for null values
print(music_df.isnull().sum())

data=music_df

#calculating weighted popularity based on release date
def weighted_popularity(release_date):
    release_date=datetime.strptime(release_date, '%Y%M%D')
    
    time_span=datetime.now()-release_date
    
    weight=1/(time_span.days+1)
    
    return weight

#normalizing using minmax scaling
scaler=MinMaxScaler()
music_features=data[['Danceability','Energy','Key','Loudness','Mode','Speechiness','Acousticness',
                     'Instrumentalness','Liveness','Valence','Tempo']].values
music_features_scaled=scaler.fit_transform(music_features)



def content_recommendations(input_song_name,num_recs=10,alpha=0.5):
   if input_song_name not in music_df['Track name'].values:
       print("{} not found in music dataset. Please provide valid track name".format(input_song_name))
       return
   
   input_song_index=music_df[music_df['Track name']==input_song_name].index[0]
   
   similarity_score=cosine_similarity([music_features_scaled[input_song_index]],music_features_scaled)
   
   similar_song_indices=similarity_score.argsort()[0][::-1][1:num_recs+1]
   
   content_based_recs=music_df.iloc[similar_song_indices][['Track name','Artists','Album Name','Release date','Popularity']]
   print(content_based_recs.dtypes)
   return content_based_recs

def hybrid_recommendations(input_song_name,num_recs=10,alpha=0.5):
    if input_song_name not in music_df['Track name'].values:
        print("{} not in music dataframe. Please enter a valid song name".format(input_song_name))
        return
    
    content_based_rec=content_recommendations(input_song_name,num_recs)
    
    popularity_score=music_df.loc[music_df["Track name"]==input_song_name,'Popularity'].values[0]
    weighted_popularity_score=popularity_score*weighted_popularity(music_df.loc[music_df['Track name']==input_song_name,'Release date'].values[0])
    
    #combining content-based and popularity-based recs
    hybrid_recs=content_based_rec
    hybrid_recs['Track name']:input_song_name
    hybrid_recs['Artists']:music_df.loc[music_df['Track name']==input_song_name,'Artists'].values[0]
    hybrid_recs['Album Name']:music_df.loc[music_df['Track name']==input_song_name,'Album Name'].values[0]
    hybrid_recs['Release date']:music_df.loc[music_df['Track name']==input_song_name,'Release date'].values[0]
    hybrid_recs['Popularity']:weighted_popularity_score
    
        
    
    hybrid_recs=hybrid_recs.sort_values(by='Popularity',ascending=False)
    hybrid_recs=hybrid_recs[hybrid_recs['Track name']!=input_song_name]
    
    return hybrid_recs

input_song_name='Lose Yourself'
recommendations=hybrid_recommendations(input_song_name,num_recs=7)
print("Hybrid recommended songs for '{}'".format(input_song_name))
print(recommendations)
    