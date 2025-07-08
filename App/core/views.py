from flask import Blueprint, make_response, render_template, jsonify #added jsonify
from App.functions.streamer import AWS_RDB


core = Blueprint('core', __name__)

@core.route('/reddit_line_data', methods = ['GET','POST'])
def reddit_line_data():

    db = AWS_RDB()
 
    db_data = db.reddit_query_half_hour()

    resp = make_response(db_data)
    resp.mimetype = 'application/json'
    return resp

@core.route('/reddit_pie_data')
def reddit_pie_data():

    db = AWS_RDB()

    db_data = db.reddit_query_pie_data()

    resp = make_response(db_data)
    resp.mimetype = 'application/json'
    return resp

@core.route('/reddit_total')
def reddit_total():

    db = AWS_RDB()

    db_data = db.reddit_query_pie_data()

    dat = str(sum(db_data['count']))

    resp = make_response(dat)
    resp.mimetype = 'application/json'
    return resp

@core.route('/twitter_line_data')
def twitter_line_data():

    db = AWS_RDB()

    db_data = db.twitter_query_half_data()

    resp = make_response(db_data)

    resp.mimetype = 'application/json'
    return resp

@core.route('/twitter_total')
def twitter_total():

    db = AWS_RDB()

    db_data = db.twitter_total_query()

    total = db_data['count']

    #resp = make_response(total)

    #resp.mimetype = 'application/json'
    #return resp
    return jsonify({"count":total})

@core.route('/twitter_sentiment')
def twitter_sentiment():

    db = AWS_RDB()

    db_data = db.twitter_sentiment_query()

    resp = make_response(db_data)

    resp.mimetype = 'application/json'
    return resp

@core.route('/twitter_median_sentiment')
def twitter_median_sentiment():

    db = AWS_RDB()

    db_data = db.twitter_median_query()

    data = str(db_data['median'])

    resp = make_response(data)

    resp.mimetype = 'application/json'
    return resp


@core.route('/', methods = ['GET', 'POST'])
def index():

    return render_template('index.html')

@core.route('/maintenance')
def maintenance():

    return render_template('maintenance.html')

