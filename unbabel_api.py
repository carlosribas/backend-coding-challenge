import os
from unbabel.api import UnbabelApi
from config import load_dotenv

uapi = UnbabelApi(os.environ['USERNAME'], os.environ['API_KEY'], sandbox=True)


def post_translation(text):
    """HTTP request to the translation endpoint.

    :param text: text to be translated
    :return: dict with the uid
    """
    return uapi.post_translations(
        text=text,
        source_language='en',
        target_language='es'
    )


def get_translation(uid):
    """Check the translation status.

    :param uid: uid from the text to be translated
    :return: dict with status and translatedText (if the translation is completed)
    """
    return uapi.get_translation(uid)
