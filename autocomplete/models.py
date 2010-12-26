from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models


class AutocompleteObjectManager(models.Manager):
    def for_object(self, obj):
        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )


class AutocompleteObject(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey()
    sites = models.ManyToManyField(Site, blank=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    data = models.TextField(blank=True)
    
    objects = AutocompleteObjectManager()
    
    class Meta:
        ordering = ('-pub_date',)
    
    def __unicode__(self):
        return '%s: %s' % (self.content_object, self.title)
