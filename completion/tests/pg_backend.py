from completion.backends.postgres_backend import PostgresAutocomplete
from completion.models import AutocompleteObject
from completion.tests.base import AutocompleteTestCase
from completion.tests.models import Blog, BlogProvider
from completion.sites import AutocompleteSite


test_site = AutocompleteSite(PostgresAutocomplete())
test_site.register(Blog, BlogProvider)


class PGBackendTestCase(AutocompleteTestCase):
    def test_storing_providers(self):
        self.assertEqual(AutocompleteObject.objects.count(), 0)
        
        test_site.store_providers()
        self.assertEqual(AutocompleteObject.objects.count(), 6)
        
        titles = AutocompleteObject.objects.values_list('title', flat=True)
        self.assertEqual(sorted(titles), [
            'testingpython',
            'testingpythoncode',
            'testingpythoncode',
            'testswithpython',
            'unittestswith',
            'webtestingpython',
        ])
    
    def test_storing_objects(self):
        test_site.store_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 1)
        
        test_site.store_object(self.blog_tpc)
        self.assertEqual(AutocompleteObject.objects.count(), 2)
        
        test_site.store_object(self.blog_tp) # storing again does not produce dupe
        self.assertEqual(AutocompleteObject.objects.count(), 2)
        
        test_site.store_object(self.blog_wtp)
        self.assertEqual(AutocompleteObject.objects.count(), 4)
    
    def test_removing_objects(self):
        test_site.store_providers()
        
        test_site.remove_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 5)
        
        test_site.remove_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 5)
        
        test_site.remove_object(self.blog_tpc)
        self.assertEqual(AutocompleteObject.objects.count(), 4)
    
    def test_suggest(self):
        test_site.store_providers()
        
        results = test_site.suggest('testing python')
        self.assertEqual(results, [
            {'stored_title': 'testing python'},
            {'stored_title': 'testing python code'},
            {'stored_title': 'web testing python code'},
        ])
        
        results = test_site.suggest('unit')
        self.assertEqual(results, [{'stored_title': 'unit tests with python'}])
        
        results = test_site.suggest('')
        self.assertEqual(results, [])
        
        results = test_site.suggest('another')
        self.assertEqual(results, [])
