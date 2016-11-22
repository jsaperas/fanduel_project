## Overview

I can see a lot of ways to model this problem and perhaps it is worth discussing.  The simplest way is to fit a machine learning model and predict total points.  This is quick and easy to do.  The second way is to build a model for each category (or a subset of categories) and then add them up.  This takes more work but my initial guess is it will be more accurate.


### Model types
I think another potential interesting thing is to model ones probability of playing a game. Maybe it is my lack of understanding of basketball but do we always know when players will play? When people are questionable, we can estimate the probability they will play and then multiply that by their expected points given they play.

This leads to another type of model where we can estimate both a players number of minutes using a model, and then estimate their expected rate of scoring and then multiply those.  This is good for bench players which may play a lot in a particular game.

Looking at the breakdown from our data, we see that 67% of players played in a game, 18% did not play at all, 15% were inactive (injury?) and under 1% were either suspended, did not dress, or werent with team.

We also want to see the effect of coming back from injury and do some analysis on that so we know how to value these players and what a team change does to players.

Also wondering if injuries are predictable.


### Modeling 
So far, the GBM outperforms the average model by 8% using MAE.  We would like to test other metrics that may make more sense like GINI, lift, and MAE using the average as the benchmark.
