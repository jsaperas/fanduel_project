import pandas as pd
import numpy as np

def x_game_average(metric, x):
    return metric.shift(1).rolling(window=x,min_periods=x).mean()

def transform_data(df, features, game_window = [3,5,10]):
    
    df = df.sort_values(['Name','Year','Week'],ascending=[1,1,1])

    #All transformed dataframes are going to be appended to model_data
    model_data = pd.DataFrame()
    
    #Iterate over each player and create the metrics
    list_of_players = df['Name'].unique()
    for player in list_of_players:
        sub_df = df[df['Name'] == player]
        
        for w in game_window:
            for feature in features: 
                metric_name = feature + '_' + str(w) + '_gm'
                sub_df[metric_name] = x_game_average(sub_df[feature],w)
        model_data = model_data.append(sub_df, ignore_index=True)
    
    return model_data