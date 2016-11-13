import pandas as pd
import numpy as np
import transform_functions as tf

RB_df = pd.read_csv('RB Data.csv')
RB_df = RB_df.iloc[:,1:]


RB_features = ['Rush Att', 'Rush Yards', 
			'Rush TD', 'Rec Targets', 
			'Rec Comp', 'Rec Yards', 
			'Rec TD', 'Fantasy PTS']

RB_model_data = tf.transform_data(df,RB_features)