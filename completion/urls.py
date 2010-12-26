from django.conf.urls.defaults import *


urlpatterns = patterns('completion.views',
    url(r'^$', 'autocomplete', name='autocomplete'),
)
