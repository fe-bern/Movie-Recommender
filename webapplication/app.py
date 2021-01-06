'''
This is the main function for the movie recommender.
'''

from flask import Flask, render_template, request
from simple_recommendation import get_recommendations

app = Flask(__name__)

# @app.route says whatever function is written underneath, we want to 'route'
# the output to '/'
@app.route("/")
@app.route("/index")
def index():
    '''
    This function is for rendering the index.html.
    '''
    return render_template("index.html")


@app.route("/movies")
def movies():
    '''
    Routing to the movies page.
    '''
    num = 3
    return render_template("movies.html", num_html=num)


@app.route("/results")
def results():
    '''
    Getting user input and in right format for function get_recommendations.
    '''
    user_input = dict(request.args)
    user_movies = list(user_input.values())[::2]
    user_ratings = list(user_input.values())[1::2]
    user_movies.pop()
    user_movies = [int(x) for x in user_movies]
    user_ratings = [float(x) for x in user_ratings]
    new_user = dict(zip(user_movies, user_ratings))

    #movies_list = recommender.nmf(user_movies, user_ratings)
    movie_list = get_recommendations(new_user)
    return render_template("results.html", top_choice=movie_list)

@app.route("/result_error")
def result_error():
    '''
    Showing a error message when no input is given.
    '''
    return render_template("result_error.html")
