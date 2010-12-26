class BaseBackend(object):
    """
    Specify the interface for Autocomplete providers
    """
    def flush(self):
        raise NotImplementedError
    
    def store_object(self, obj, data):
        raise NotImplementedError
    
    def remove_object(self, obj, data):
        raise NotImplementedError
    
    def suggest(self, phrase, limit):
        raise NotImplementedError
