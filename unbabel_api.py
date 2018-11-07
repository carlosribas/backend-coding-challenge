import os
from unbabel.api import UnbabelApi
from config import load_dotenv

uapi = UnbabelApi(os.environ['USERNAME'], os.environ['API_KEY'], sandbox=True)
callback_url = 'http://127.0.0.1/unbabel_callback/'
target_language = 'es'


def post_translation(text):
    return uapi.post_translations(text=text, target_language=target_language, callback_url=callback_url)


def get_translation(uid):
    return uapi.get_translation(uid)