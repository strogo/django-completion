from django.conf.urls.defaults import *


urlpatterns = patterns('completion.views',
    url(r'^$', 'completion', name='completion'),
)
