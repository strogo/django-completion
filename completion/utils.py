import re

from django.conf import settings
from django.utils.importlib import import_module

from completion.constants import *


def clean_phrase(phrase):
    """
    Lower-case and strip articles from a phrase
    """
    phrase = phrase.lower()
    return [w for w in phrase.split() if w not in AUTOCOMPLETE_ARTICLES]

def partial_complete(phrase):
    """
    Break apart a phrase into several chunks using max_words as a guide
    
    The quick brown fox jumped --> quick brown fox, brown fox jumped
    """
    words = clean_phrase(phrase)
    chunks = len(words) - MAX_WORDS + 1
    chunks = chunks < 1 and 1 or chunks
    
    for i in range(chunks):
        yield ' '.join(words[i:i + MAX_WORDS])

def create_key(phrase):
    """
    Clean up a phrase making it suitable for use as a key
    
    The quick brown fox jumped --> quickbrownfox
    """
    key = ' '.join(clean_phrase(phrase)[:MAX_WORDS])
    return re.sub('[^a-z0-9_-]', '', key)

def get_backend():
    mod, klass = settings.AUTOCOMPLETE_BACKEND.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, klass)
