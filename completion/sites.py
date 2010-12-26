from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.utils import simplejson as json

from completion.utils import get_backend


class AutocompleteProvider(object):
    def __init__(self, model):
        self.model = model
    
    def get_title(self, obj):
        """
        The title of the object, which will support autocompletion
        """
        raise NotImplementedError
    
    def get_sites(self, obj):
        """
        Ideally, return a list of primary keys, however a list or queryset of
        Site objects will be converted automatically
        """
        return [settings.SITE_ID]
    
    def get_pub_date(self, obj):
        """
        Used for ordering
        """
        raise NotImplementedError
    
    def get_data(self, obj):
        """
        Any arbitrary data to go along with this object, i.e. the object's
        absolute URL, which can be stored to avoid a db hit
        """
        return {}
    
    def get_queryset(self):
        return self.model._default_manager.all()
    
    def object_to_dictionary(self, obj):
        sites = self.get_sites(obj)
        if isinstance(sites, QuerySet):
            sites = list(sites.values_list('pk', flat=True))
        elif isinstance(sites, (list, tuple)) and len(sites):
            if isinstance(sites[0], Site):
                sites = [site.pk for site in sites]
        
        return {
            'title': self.get_title(obj),
            'sites': sites,
            'pub_date': self.get_pub_date(obj),
            'data': self.get_data(obj)
        }


class AutocompleteSite(object):
    def __init__(self, backend):
        self._providers = {}
        self.backend = backend
    
    def register(self, model_class, provider):
        self._providers[model_class] = provider(model_class)
    
    def unregister(self, model_class):
        if model_class in self._providers:
            del(self._providers[model_class])
    
    def get_provider(self, obj):
        try:
            return self._providers[type(obj)]
        except KeyError:
            raise TypeError("Don't know what do with %s" % obj.__name__)
    
    def flush(self):
        self.backend.flush()
    
    def prepare_object(self, provider, obj):
        obj_dict = provider.object_to_dictionary(obj)
        obj_dict['data'] = self.serialize_data(obj_dict['data'])
        return obj_dict
    
    def _store(self, provider, obj):
        obj_dict = self.prepare_object(provider, obj)
        self.backend.store_object(obj, obj_dict)
    
    def store_providers(self):
        self.flush()
        for provider in self._providers.values():
            self.store_provider_queryset(provider)
    
    def store_provider_queryset(self, provider):
        for obj in provider.get_queryset().iterator():
            self._store(provider, obj)
    
    def store_object(self, obj):
        provider = self.get_provider(obj)
        self._store(provider, obj)
    
    def remove_object(self, obj):
        provider = self.get_provider(obj)
        obj_dict = self.prepare_object(provider, obj)
        self.backend.remove_object(obj, obj_dict)
    
    def suggest(self, text, limit=None):
        # pass limit to the backend in case it can optimize
        result_set = self.backend.suggest(text, limit)
        if limit is not None:
            result_set = result_set[:limit]
        return map(self.deserialize_data, result_set)
    
    def serialize_data(self, data_dict):
        return json.dumps(data_dict)
    
    def deserialize_data(self, raw):
        return json.loads(raw)


backend_class = get_backend()
backend = backend_class()
site = AutocompleteSite(backend)
