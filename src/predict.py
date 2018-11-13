# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    predict.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pleroux <pleroux@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/13 14:55:47 by pleroux           #+#    #+#              #
#    Updated: 2018/11/13 16:01:28 by pleroux          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.sql.sqlPredict import sql as sqlPredict
from src.pipeline import stats_pipeline
from urllib.parse import unquote
import datetime
import pickle
from sqlalchemy import create_engine
import requests as req
import pandas as pd
import numpy as np
from src.url_engine import URL_ENGINE
from flask_restful import Resource
from flask import request


def get_data_prediction(date, winner, looser, url_engine=URL_ENGINE):
    engine = create_engine(URL_ENGINE)

    with engine.connect() as conn, conn.begin():
        return pd.read_sql(sqlPredict.format(date=date, winner=winner, looser=looser), conn)

def load_model(name, path='models/'):
    file = open(path + '/' + name, 'rb')
    obj = pickle.load(file)
    file.close()
    return obj

class predict(Resource):
    def __init__(self, path='playground/models/'):
        self.model = load_model("rnd_search_co", path)

    def post(self):
        if not request.form['home'] or not request.form['away']:
            return {"message": "Error: No data home or away player"}
        prediction_data = get_data_prediction(
                datetime.datetime.now().strftime("%Y-%m-%d"),
                unquote(request.form['home']),
                unquote(request.form['away']))
        prediction_data.insert(prediction_data.shape[1], "result", 
                np.random.randint(2, size=prediction_data.shape[0]))

        X_pred = stats_pipeline.fit_transform(prediction_data)
        pred = self.model.predict_proba(X_pred)
        if prediction_data["result"][0] == 0:
            return {
                    "message": "ok",
                    "home": round(pred[0][0] * 100, 1),
                    "away": round(pred[0][1] * 100, 1)
                    }
        return {
                "message": "ok",
                "home": round(pred[0][1] * 100, 1),
                "away": round(pred[0][0] * 100, 1)
                }

