import datetime

from django.db import models

from completion.sites import AutocompleteProvider


class Blog(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    content = models.TextField()
    published = models.BooleanField(default=True)


class BlogProvider(AutocompleteProvider):
    def get_title(self, obj):
        return obj.title
    
    def get_pub_date(self, obj):
        return datetime.datetime(2010, 1, 1)
    
    def get_data(self, obj):
        return {'stored_title': obj.title}
    
    def get_queryset(self):
        return self.model._default_manager.filter(published=True)
