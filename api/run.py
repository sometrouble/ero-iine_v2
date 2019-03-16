import yaml
import tweepy
from pathlib import Path
from flask import Flask, jsonify, redirect, session, request

api = Flask(__name__)
api.secret_key = 'hoge'

API_ROOT = Path(__file__).parent
PROJECT_ROOT = API_ROOT.parent

SETTINGS_DIR = Path(PROJECT_ROOT / 'settings')
SETTINGS_CONFIG_FILE = Path(SETTINGS_DIR / 'config.yaml')

SETTINGS = yaml.load(SETTINGS_CONFIG_FILE.read_text(), Loader=yaml.SafeLoader)

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

    return api.user_timeline(count=20)[0].text

if __name__ == '__main__':
    api.run(host=SETTINGS['FLASK_URL'], port=SETTINGS['FLASK_PORT'])
