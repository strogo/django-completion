from django.test import TestCase

from completion.tests.models import Blog


class AutocompleteTestCase(TestCase):
    fixtures = ['completion_testdata.json']
    
    def setUp(self):
        self.blog_tp = Blog.objects.get(pk=1)
        self.blog_tpc = Blog.objects.get(pk=2)
        self.blog_wtp = Blog.objects.get(pk=3)
        self.blog_utp = Blog.objects.get(pk=4)
        self.blog_unpub = Blog.objects.get(pk=5)
