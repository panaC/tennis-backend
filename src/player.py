# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    player.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pleroux <pleroux@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/13 16:06:46 by pleroux           #+#    #+#              #
#    Updated: 2018/11/13 16:48:51 by pleroux          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.sql.sqlPlayer import sql as sqlPlayer
from sqlalchemy import create_engine
from src.url_engine import URL_ENGINE
from flask_restful import Resource
from flask import request
import pandas as pd

def get_player(player):
    engine = create_engine(URL_ENGINE)

    with engine.connect() as conn, conn.begin():
        return pd.read_sql(sqlPlayer.format(player=player), conn)

class player(Resource):
    def post(self):
        if not request.form['player']:
            return {"message": "Error: No player provided"}
        return {
                "message": "ok",
                "data": get_player(request.form['player']).to_dict()["player"]
                }

