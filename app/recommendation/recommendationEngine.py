import pandas as pd
import numpy as np

async def recommendation_processor(InputVector: dict):
    s

async def user_preference(track_histories: dict):
    # Clean data
    for track in track_histories:
        track.pop('_id', None)
        track.pop('album_name', None)
        track.pop('song_name', None)
        track.pop('artist_name', None)
        track.pop('user_id', None)
        track.pop('played_at', None)

    # Convert to a dataframe
    features = pd.DataFrame(track_histories)

    # Calculate mean
    preference_profile = features.mean()

    return preference_profile.to_dict()