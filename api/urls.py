import tweepy
from flask import jsonify, redirect, session, request

from main import api
from settings import SETTINGS

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

    return api.favorites()[0].text
