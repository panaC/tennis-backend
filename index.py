# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    index.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pleroux <pleroux@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/13 10:40:23 by pleroux           #+#    #+#              #
#    Updated: 2018/11/13 11:05:06 by pleroux          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import pickle
from  sqlalchemy import create_engine
#import psycopg2 as pg
import requests as req
import pandas as pd
import numpy as np
import datetime
from urllib.parse import unquote
import sys

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

URL_ENGINE = 'postgresql://dataset:dataset1747@35.204.62.91:5432/dataset-dump1'

def get_data_prediction(date, winner, looser, url_engine=URL_ENGINE):
    engine = create_engine(URL_ENGINE)

    URL = "https://raw.githubusercontent.com/panaC/tennis-dataset/master/app/dataset/prediction.sql"
    with engine.connect() as conn, conn.begin():
        return pd.read_sql(req.get(URL).text.format(date=date, winner=winner, looser=looser), conn)

PATH = sys.argv[1] + '/' or 'models/'

def load_model(name, path=PATH):
    file = open(path + name, 'rb')
    obj = pickle.load(file)
    file.close()
    return obj

###################
######
###################

from sklearn.base import BaseEstimator, TransformerMixin

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

from sklearn.pipeline import Pipeline

stats_pipeline = Pipeline([
        ("select_stats", DataFrameSelector(stats_col)),
        ("reverse", reverseStats()),
    ])

###################
######
###################

class predict(Resource):
    def __init__(self):
        self.model = load_model("rnd_search_co")

    def post(self):
        if not request.form['home'] or not request.form['away']:
            return {"message": "Error: No data home or away player"}
        prediction_data = get_data_prediction(datetime.datetime.now().strftime("%Y-%m-%d"), unquote(request.form['home']), unquote(request.form['away']))
        prediction_data.insert(prediction_data.shape[1], "result", np.random.randint(2, size=prediction_data.shape[0]))

        X_pred = stats_pipeline.fit_transform(prediction_data)
        pred = self.model.predict_proba(X_pred)
        if prediction_data["result"][0] == 0:
            return {"message": "ok", "home": round(pred[0][0] * 100, 1), "away": round(pred[0][1] * 100, 1)}
        return {"message": "ok", "home": round(pred[0][1] * 100, 1), "away": round(pred[0][0] * 100, 1)}

api.add_resource(predict, '/api/predict')

if __name__ == '__main__':
    app.run(debug=True)
