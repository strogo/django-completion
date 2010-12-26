from django.http import HttpResponse
from django.utils import simplejson as json

from completion import constants, site


def autocomplete(request, num_results=constants.DEFAULT_RESULTS):
    q = request.GET.get('q')
    results = []
    if q:
        results = site.suggest(q, num_results)
    return HttpResponse(json.dumps(results), mimetype='application/json')
