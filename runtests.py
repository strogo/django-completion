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
            'autocomplete.tests',
            'autocomplete',
        ],
        AUTOCOMPLETE_BACKEND='autocomplete.backends.postgres_backend.PostgresAutocomplete',
        AUTOCOMPLETE_REDIS_CONNECTION='localhost:6379:0',
        AUTOCOMPLETE_SOLR_CONNECTION='http://localhost:8999/solr/autocomplete-test/',
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['autocomplete']
    ac_dir = os.path.join(os.path.dirname(__file__), 'autocomplete')
    sys.path.insert(0, ac_dir)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
