from django.conf import settings

from completion import constants
from completion.backends.base import BaseBackend

from pysolr import Solr, Results


class SolrAutocomplete(BaseBackend):
    def __init__(self, connection_string=constants.SOLR_CONNECTION):
        self.connection_string = connection_string
        self.client = self.get_connection()
    
    def flush(self):
        self.client.delete(q='*:*', commit=True)
        self.client.optimize()
    
    def get_connection(self):
        return Solr(self.connection_string)
    
    def generate_unique_id(self, obj):
        return '%s:%s' % (str(obj._meta), obj.pk)
    
    def store_object(self, obj, data):
        data.update(
            id=self.generate_unique_id(obj),
            django_ct=str(obj._meta),
            django_id=obj.pk
        )
        self.client.add([data], commit=True)
    
    def remove_object(self, obj, data):
        self.client.delete(id=self.generate_unique_id(obj), commit=True)
    
    def phrase_to_query(self, phrase):
        return 'title_ngram:%s sites:%s' % (phrase, settings.SITE_ID)
    
    def suggest(self, phrase, limit):
        if not phrase:
            return []
        
        results = self.client.search(
            self.phrase_to_query(phrase),
            rows=limit or constants.DEFAULT_RESULTS
        )
        return map(lambda r: r['data'], results)
