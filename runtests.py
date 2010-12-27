#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        SITE_ID=1,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'completion.tests',
            'completion',
        ],
        AUTOCOMPLETE_BACKEND='completion.backends.db_backend.DatabaseAutocomplete',
        AUTOCOMPLETE_REDIS_CONNECTION='localhost:6379:0',
        AUTOCOMPLETE_SOLR_CONNECTION='http://localhost:8999/solr/autocomplete-test/',
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['completion']
    ac_dir = os.path.join(os.path.dirname(__file__), 'completion')
    sys.path.insert(0, ac_dir)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
