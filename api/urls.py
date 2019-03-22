import hashlib

import tweepy
from flask import jsonify, redirect, session, request

from main import api
from settings import SETTINGS

from database import tweet_db_session, user_db_session
from models.eroiine import Tweet
from models.user import User

from exception import cannotAuthTwitterException

@api.route('/')
def main():
    eroiine_dict = get_eroiines_from_db()
    return jsonify(eroiine_dict)

@api.route('/auth/twitter', methods=['GET'])
def auth_twitter():
    auth = get_auth_twitter()
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

def get_eroiines_from_db():
    response = {}
    for t in tweet_db_session.query(Tweet).all():
        response[t.tweet_id] = {
            'user_id': t.user_id,
            'text': t.tweet_text,
            'image_url1': t.image_url_1,
            'image_url2': t.image_url_2,
            'image_url3': t.image_url_3,
            'image_url4': t.image_url_4,
        }

    return response

def get_auth_twitter():
    return tweepy.OAuthHandler(SETTINGS['TWITTER_API_KEY'], SETTINGS['TWITTER_API_SECRET_KEY'])

def get_auth_twitter_consumer(hashed_tweet_id):
    consumer_key = 
    consumer_secret = 
    return tweepy.OAuthHandler(consumer_key, consumer_secret)

def get_eroiines_from_twitter():
    pass

def save_eroiines_to_db():
    twitter_api = tweepy.API(get_auth_twitter())
    exist_keys = [key.tweet_id for key in tweet_db_session.query(Tweet).all()]

    fav_list = []
    for fav in twitter_api.favorites():
        t = fav._json
        media = t['entities']['media']
        image_urls = [media[i]['media_url'] if len(media) > i else None for i in range(4)]
        print(image_urls)
        if t['id'] not in exist_keys:
            tweet = Tweet(t['id'], t['user']['id'], t['text'], image_urls)
            fav_list.append(tweet)

    tweet_db_session.add_all(fav_list)
    tweet_db_session.commit()

def hash_twitter_id(twitter_id: int):
    return hashlib.sha256(twitter_id.encode()).hexdigest()

def save_token_twitter():
    try:
        token = session.pop('request_token', None)
        verifier = request.args.get('oauth_verifier')
        if token is None or verifier is None:
            return False

        auth = get_auth_twitter()
        auth.get_access_token(verifier)

        consumer_key = auth.access_token
        consumer_key_secret = auth.access_token_secret

        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(consumer_key, consumer_key_secret)
        twitter_api = tweepy.API(auth)

        user = twitter_api.me()

        hashed_id = hash_twitter_id(user.id)
        user_db_session.add(User(hashed_id, consumer_key, consumer_key_secret))
        user_db.session.commit()

    except Exception:
        raise cannotAuthTwitterException
