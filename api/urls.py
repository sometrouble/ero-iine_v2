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
def page_top():
    eroiine_dict = get_eroiines_from_db()
    return jsonify(eroiine_dict)

@api.route('/auth/twitter', methods=['GET'])
def page_auth_twitter():
    auth = get_auth_twitter()
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

@api.route('/auth/twitter/save_data', methods=['GET'])
def page_save_tokens():
    hashed_id = save_token_twitter()
    save_eroiines_to_db(hashed_id)
    return redirect('/')

def get_eroiines_from_db() -> dict:
    """get all-eroiines from database.
    Returns:
        dict: ero-iine with tweet-id as key.
    """
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

def get_auth_twitter() -> tweepy.OAuthHandler:
    """auth twitter with saved tokens.
    Returns:
        tweepy.OAuthHandler:
    """
    return tweepy.OAuthHandler(SETTINGS['TWITTER_API_KEY'], SETTINGS['TWITTER_API_SECRET_KEY'])

def get_auth_twitter_consumer(hashed_twitter_id: str) -> tweepy.OAuthHandler:
    """auth twitter with saved tokens.
    Args:
        hashed_twitter_id(str):
    Returns:
        tweepy.OAuthHandler:
    """
    user = user_db_session.query(User.token, User.token_secret).filter(User.hashed_user_id == hashed_twitter_id).one()
    auth = get_auth_twitter()
    auth.set_access_token(user.token, user.token_secret)
    twitter_api = tweepy.API(auth)
    return twitter_api

def get_eroiines_from_twitter():
    pass

def save_eroiines_to_db(hashed_twitter_id: str):
    """save eroiines from user-twitter-favolites.
    """
    twitter_api = get_auth_twitter_consumer(hashed_twitter_id)
    exist_keys = [key[0] for key in tweet_db_session.query(Tweet.tweet_id).all()]

    fav_list = []
    for fav in twitter_api.favorites():
        t = fav._json
        if is_img_tweet(t):
            media = t['entities']['media']
            image_urls = [media[i]['media_url'] if len(media) > i else None for i in range(4)]
            if t['id'] not in exist_keys:
                tweet = Tweet(t['id'], t['user']['id'], t['text'], image_urls)
                fav_list.append(tweet)

    if len(fav_list) > 0:
        tweet_db_session.add_all(fav_list)
        tweet_db_session.commit()

def is_img_tweet(tweet: dict):
    """determine img tweet.
    Returns:
        bool:
    """
    media = tweet['entities']['media']
    if len(media) > 0:
        if media[0]['type'] == 'photo':
            return True
    return False

def hash_twitter_id(twitter_id: int):
    """for cookie injection(wip)
    Returns:
        str: sha256-hex-hashed twitter_id
    """
    return hashlib.sha256(str(twitter_id).encode()).hexdigest()

def save_token_twitter():
    """save auth-tokens
    Returns:
        str: hashed twitter id
    """
    token = session.pop('request_token', None)
    verifier = request.args.get('oauth_verifier')
    if token is None or verifier is None:
        return False

    auth = get_auth_twitter()
    auth.request_token = token
    auth.get_access_token(verifier)

    consumer_key = auth.access_token
    consumer_key_secret = auth.access_token_secret

    try:
        auth = get_auth_twitter()
        auth.set_access_token(consumer_key, consumer_key_secret)
        twitter_api = tweepy.API(auth)

        user = twitter_api.me()

        hashed_id = hash_twitter_id(user.id)

        exist_users = [user[0] for user in user_db_session.query(User.hashed_user_id).all()]

        if hashed_id not in exist_users:
            user_db_session.add(User(hashed_id, consumer_key, consumer_key_secret))
            user_db_session.commit()

        return hashed_id

    except Exception:
        raise cannotAuthTwitterException
