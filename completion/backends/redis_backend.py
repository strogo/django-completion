import re

from django.conf import settings

from completion.backends.base import BaseBackend
from completion.constants import MIN_LENGTH, REDIS_CONNECTION
from completion.utils import clean_phrase, create_key, partial_complete

from redis import Redis


class RedisAutocomplete(BaseBackend):
    """
    Pretty proof-of-concept-y -- autocomplete across partial matches of a title
    string.  Does not handle siteification, pub_date filtering.
    
    Check out:
    http://antirez.com/post/autocomplete-with-redis.html
    http://stackoverflow.com/questions/1958005/redis-autocomplete/1966188#1966188
    """
    def __init__(self, connection=REDIS_CONNECTION, prefix='autocomplete:',
                 terminator='^'):
        host, port, db = connection.split(':') # host:port:db
        self.host = host
        self.port = int(port)
        self.db = int(db)
        
        self.prefix = prefix
        self.terminator = terminator
        
        self.client = self.get_connection()
    
    def get_connection(self):
        return Redis(host=self.host, port=self.port, db=self.db)
    
    def flush(self):
        self.client.flushdb()
    
    def autocomplete_keys(self, title):
        key = create_key(title)
        
        current_key = key[:MIN_LENGTH]
        for char in key[MIN_LENGTH:]:
            yield (current_key, char, ord(char))
            current_key += char
        
        yield (current_key, self.terminator, 0)
    
    def store_object(self, obj, data):
        """
        Given a title & some data that needs to be stored, make it available
        for autocomplete via the suggest() method
        """
        title = data['title']
        for partial_title in partial_complete(title):
            for (key, value, score) in self.autocomplete_keys(partial_title):
                self.client.zadd('%s%s' % (self.prefix, key), value, score)
            
            self.client.sadd(key, data['data'])
    
    def remove_object(self, obj, data):
        title = data['title']
        keys = []
        for partial_title in partial_complete(title):
            partial_key = create_key(partial_title)
            self.client.srem(partial_key, data)
            key = '%s%s' % (self.prefix, partial_key)
            self.client.zrem(key, '^')
    
    def suggest(self, phrase, limit):
        """
        Wrap our search & results with prefixing
        """
        phrase = create_key(phrase)
        results = self._suggest('%s%s' % (self.prefix, phrase), limit)
        prefix_len = len(self.prefix)
        cleaned_keys = map(lambda x: x[prefix_len:], results)
        
        data = []
        for key in cleaned_keys:
            data.extend(self.client.smembers(key))
        
        return data
    
    def _suggest(self, text, limit):
        """
        At the expense of key memory, depth-first search all results
        """
        w = []
        
        for char in self.client.zrange(text, 0, -1):
            if char == self.terminator:
                w.append(text)
            else:
                w.extend(self._suggest(text + char, limit))
            
            if limit and len(w) >= limit:
                return w[:limit]
        
        return w
