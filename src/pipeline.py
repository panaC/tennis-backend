# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    pipeline.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pleroux <pleroux@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/13 14:37:50 by pleroux           #+#    #+#              #
#    Updated: 2018/11/13 14:38:46 by pleroux          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# A class to select numerical or categorical columns
# since Scikit-Learn doesn't handle DataFrames yet
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names]

class reverseStats(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        ## while on each row : if result = 1 nothing else opponent each value in each collumn
        def wh(a):
            if (a["result"] == 0):
                a = a.apply(lambda x: x * -1)
            return a

        X = X.fillna(0)
        X = X.apply(wh, axis=1)
        X = X.drop("result", axis=1)
        return X

stats_col = ["serve_rating_1year", "aces_1year", "double_faults_1year", "first_serve_1year", "first_serve_point_won_1year",
       "second_serve_point_won_1year", "bp_saved_1year", "service_game_played_1year", "return_rating_1year",
       "first_serve_return_point_won_1year", "bp_converted_1year", "return_games_played_1year", "service_point_won_1year",
       "return_point_won_1year", "total_point_won_1year", "serve_rating_20years",
       "aces_20years", "double_faults_20years", "first_serve_20years", "first_serve_point_won_20years", "second_serve_point_won_20years",
       "bp_saved_20years", "service_game_played_20years", "return_rating_20years", "first_serve_return_point_won_20years",
       "bp_converted_20years", "return_games_played_20years", "service_point_won_20years", "return_point_won_20years",
       "total_point_won_20years", "h2h", "minutes_loser_winner", "result"]

stats_pipeline = Pipeline([
        ("select_stats", DataFrameSelector(stats_col)),
        ("reverse", reverseStats()),
    ])


