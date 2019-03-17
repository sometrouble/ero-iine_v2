import tweepy
from flask import jsonify, redirect, session, request

from main import api
from settings import SETTINGS

from database import db_session
from models.eroiine import Tweet

@api.route('/')
def main():
    timeline = get_user_timeline()
    return jsonify(timeline)
    # return jsonify({'message': 'hello ero-iine'})

@api.route('/auth/twitter', methods=['GET'])
def auth_twitter():
    auth = tweepy.OAuthHandler(SETTINGS['TWITTER_API_KEY'], SETTINGS['TWITTER_API_SECRET_KEY'])
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

def get_user_timeline():
    token = session.pop('request_token', None)
    verifier = request.args.get('oauth_verifier')
    if token is None or verifier is None:
        return False

    auth = tweepy.OAuthHandler(SETTINGS['TWITTER_API_KEY'], SETTINGS['TWITTER_API_SECRET_KEY'])
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except Exception:
        return {}

    api = tweepy.API(auth)

    exist_keys = [key.tweet_id for key in db_session.query(Tweet).all()]

    fav_list = []
    for fav in api.favorites():
        t = fav._json
        media = t['entities']['media']
        image_urls = [media[i]['media_url'] if len(media) > i else None for i in range(4)]
        print(image_urls)
        if t['id'] not in exist_keys:
            tweet = Tweet(t['id'], t['user']['id'], t['text'], image_urls)
            fav_list.append(tweet)

    db_session.add_all(fav_list)
    db_session.commit()

    response = {}
    for t in db_session.query(Tweet).all():
        response[t.tweet_id] = {
            'user_id': t.user_id,
            'text': t.tweet_text,
            'image_url1': t.image_url_1,
            'image_url2': t.image_url_2,
            'image_url3': t.image_url_3,
            'image_url4': t.image_url_4,
        }

    return response
