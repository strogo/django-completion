from django.conf import settings


def def_to(setting, default):
    return getattr(settings, setting, default)


# articles to strip when handling a phrase for autocomplete
AUTOCOMPLETE_ARTICLES = def_to('AUTOCOMPLETE_ARTICLES', ['a', 'an', 'the'])

# maximum number of words to generate keys on (Redis & Postgres)
MAX_WORDS = def_to('AUTOCOMPLETE_MAX_WORDS', 3)

# minimum length of phrase for autocompletion
MIN_LENGTH = def_to('AUTOCOMPLETE_MIN_LENGTH', 3)

# default results to return
DEFAULT_RESULTS = def_to('AUTOCOMPLETE_DEFAULT_RESULTS', 10)


# connection settings

# host:port:db, i.e. localhost:6379:0
REDIS_CONNECTION = def_to('AUTOCOMPLETE_REDIS_CONNECTION', None)

# url, i.e. http://localhost:8080/solr/autocomplete-core/
SOLR_CONNECTION = def_to('AUTOCOMPLETE_SOLR_CONNECTION', None)

# test-only settings
SOLR_TEST_CONNECTION = def_to('AUTOCOMPLETE_SOLR_TEST_CONNECTION', None)
