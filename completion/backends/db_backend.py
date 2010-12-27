from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from completion.backends.base import BaseBackend
from completion.models import AutocompleteObject
from completion.utils import clean_phrase, create_key, partial_complete


class DatabaseAutocomplete(BaseBackend):
    def flush(self):
        AutocompleteObject.objects.all().delete()
    
    def store_object(self, obj, data):
        """
        Given a title & some data that needs to be stored, make it available
        for autocomplete via the suggest() method
        """
        self.remove_object(obj, data)
        
        title = data['title']
        for partial_title in partial_complete(title):
            key = create_key(partial_title)
            obj = AutocompleteObject(
                title=key,
                object_id=obj.pk,
                content_type=ContentType.objects.get_for_model(obj),
                pub_date=data['pub_date'],
                data=data['data']
            )
            obj.save()
            obj.sites = data['sites']
    
    def remove_object(self, obj, data):
        AutocompleteObject.objects.for_object(obj).delete()
    
    def suggest(self, phrase, limit):
        phrase = create_key(phrase)
        if not phrase:
            return []
        
        qs = AutocompleteObject.objects.filter(
            title__startswith=phrase,
            sites__pk__exact=settings.SITE_ID
        ).values_list('data', flat=True)
        
        if limit is not None:
            qs = qs[:limit]
            
        return qs
