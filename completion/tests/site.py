import datetime

from django.contrib.auth.models import User, Group

from completion.backends.base import BaseBackend
from completion.models import AutocompleteObject
from completion.sites import AutocompleteProvider, AutocompleteSite
from completion.tests.base import AutocompleteTestCase
from completion.tests.models import Blog, BlogProvider
from completion.utils import clean_phrase, partial_complete, create_key


class DummyBackend(BaseBackend):
    """
    A test-only backend, titles are not broken up into bits to be searched for
    partial matches.  Just an in-memory dictionary of {title: provider data}
    """
    def __init__(self):
        self._index = {}
    
    def store_object(self, obj, data):
        self._index[data['title']] = data
    
    def remove_object(self, obj, data):
        if data['title'] in self._index:
            del(self._index[data['title']])
    
    def suggest(self, phrase, limit):
        if phrase in self._index:
            return [self._index[phrase]['data']]
        return []
    
    def flush(self):
        self._index = {}


test_site = AutocompleteSite(DummyBackend())
test_site.register(Blog, BlogProvider)


class SiteTestCase(AutocompleteTestCase):
    def test_registration(self):
        # make sure our registry is populated with the test provider
        self.assertEqual(len(test_site._providers), 1)
        self.assertTrue(Blog in test_site._providers)
        self.assertTrue(isinstance(test_site._providers[Blog], BlogProvider))
    
        # make sure removing works
        test_site.unregister(Blog)
        self.assertEqual(len(test_site._providers), 0)
        
        # should no-op
        test_site.unregister(Blog)
        
        # register & then double-register -> dictionary so just reg'd once
        test_site.register(Blog, BlogProvider)
        test_site.register(Blog, BlogProvider)
        self.assertEqual(len(test_site._providers), 1)
    
    def test_get_provider(self):
        provider = test_site.get_provider(self.blog_tp)
        self.assertTrue(isinstance(provider, BlogProvider))
        
        self.assertRaises(TypeError, test_site.get_provider, Group)
    
    def test_storing_objects(self):
        test_site.flush()
        self.assertEqual(test_site.backend._index, {})
        
        test_site.store_object(self.blog_tp)
        self.assertEqual(test_site.backend._index, {
            'testing python': {
                'data': '{"stored_title": "testing python"}',
                'pub_date': datetime.datetime(2010, 1, 1),
                'sites': [1], 
                'title': 'testing python'
            }
        })
    
    def test_removing_objects(self):
        test_site.flush()
        test_site.store_providers()
        
        test_site.remove_object(self.blog_tp)
        test_site.remove_object(self.blog_tpc)
        test_site.remove_object(self.blog_wtp)
        
        self.assertEqual(test_site.backend._index, {
            'unit tests with python': {
                'data': '{"stored_title": "unit tests with python"}', 
                'pub_date': datetime.datetime(2010, 1, 1), 
                'sites': [1], 
                'title': 'unit tests with python'
            }
        })
    
    def test_storing_providers(self):
        test_site.store_providers()
        
        self.assertEqual(test_site.backend._index, {
            'testing python': {
                'data': '{"stored_title": "testing python"}',
                'pub_date': datetime.datetime(2010, 1, 1, 0, 0),
                'sites': [1],
                'title': 'testing python'
            },
            'testing python code': {
                'data': '{"stored_title": "testing python code"}',
                'pub_date': datetime.datetime(2010, 1, 1, 0, 0),
                'sites': [1],
                'title': 'testing python code'
            },
            'unit tests with python': {
                'data': '{"stored_title": "unit tests with python"}',
                'pub_date': datetime.datetime(2010, 1, 1, 0, 0),
                'sites': [1],
                'title': 'unit tests with python'
            },
            'web testing python code': {
                'data': '{"stored_title": "web testing python code"}',
                'pub_date': datetime.datetime(2010, 1, 1, 0, 0),
                'sites': [1],
                'title': 'web testing python code'
            }
        })
    
    def test_suggest(self):
        test_site.flush()
        test_site.store_providers()
        
        results = test_site.suggest('web testing python code')
        self.assertEqual(results, [{'stored_title': 'web testing python code'}])
        
        results = test_site.suggest('testing python', 2)
        self.assertEqual(results, [{'stored_title': 'testing python'}])
        
        results = test_site.suggest('testing python', 0)
        self.assertEqual(results, [])
        
        results = test_site.suggest('another unpublished')
        self.assertEqual(results, [])
