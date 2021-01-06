'''
Function which is called in app.py for getting results.
'''

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv



def get_recommendations(new_user):
    '''
    Function for getting recommendation.
    '''
    # Setting up enginge to Postgres
    username = os.getenv('USERNAME_WEB_APP')
    password = os.getenv('PASSWORD_WEB_APP')
    host = os.getenv('HOST_WEB_APP')
    conns = f"postgres://{username}:{password}@{host}:5432/db_movies"
    engine = create_engine(conns, encoding="latin1", echo=False)

    # Loading Data and cleaning
    query_ratings = "SELECT * FROM ratings;"
    df_ratings = pd.read_sql(query_ratings, engine)

    df_ratings.drop(["index", "timestamp"], axis=1, inplace=True)
    df_ratings.set_index("userId", inplace=True)
    df_ratings.rating = df_ratings.rating.astype("int")

    # Calculating Cosine Similarity
    matrix = pd.pivot_table(
        df_ratings, values="rating", index="userId", columns="movieId"
    )
    matrix = matrix.fillna(0)
    cosim = pd.DataFrame(
        cosine_similarity(matrix).round(3), index=matrix.index, columns=matrix.index
    )

    # Adding user input
    # new_user = {1: 5.0, 2: 4.0, 3: 2.0}
    matrix = matrix.append(new_user, ignore_index=True)
    matrix = matrix.fillna(0)
    cosim = pd.DataFrame(
        cosine_similarity(matrix), index=matrix.index, columns=matrix.index
    )

    # Getting recommendation from similar user
    recent_user = cosim.tail(1)
    to_drop = int(recent_user.index.values)
    dropped = cosim.drop(to_drop, axis=1)
    best_match = dropped.columns[np.argmax(dropped.tail(1))]
    recommendations = matrix.loc[best_match]
    recos = recommendations.sort_values(ascending=False).head(10).index.tolist()

    # Loading titles
    query_best_match = f"SELECT * FROM movies WHERE movieid={recos[0]} OR movieid={recos[1]} OR movieid={recos[2]}"
    df_movies_best_match = pd.read_sql(query_best_match, engine)
    title_recos = df_movies_best_match["title"].tolist()
    return title_recos
