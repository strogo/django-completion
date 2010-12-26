from django.conf.urls.defaults import *


urlpatterns = patterns('autocomplete.views',
    url(r'^$', 'autocomplete', name='autocomplete'),
)
