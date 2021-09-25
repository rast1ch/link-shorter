import json
from django.test import TestCase
import uuid
from .models import Link
from .views import rand_slug
from rest_framework.test import APIClient

class ApiViewTestCase(TestCase):
    def setUp(self):
        self.object = Link.objects.create(tocken=uuid.uuid4(),
                                          url_tocken=rand_slug(Link),
                                          link_to='https://stackoverflow.com/questions/24904362/how-to-write-unit-tests-for-django-rest-framework-apis')
        self.object.save()
        self.cli = APIClient() #requests generator
        return super().setUp()
        
    def test_link_list_get(self):
        r = self.cli.get(f'http://127.0.0.1:8000/api/info/{self.object.tocken}')
        self.assertEqual(200, r.status_code)
    
    def test_link_list_delete(self):
        r = self.cli.delete(f'http://127.0.0.1:8000/api/info/{self.object.tocken}')
        self.assertEqual(204, r.status_code)

    def test_update_link_put(self):
        r = self.cli.put(f'http://127.0.0.1:8000/api/update/{self.object.tocken}',
                         json.dumps({"link_to":"https://github.com/rast1ch/link-shorter"}),
                         content_type='application/json')
        self.assertEqual(200, r.status_code)

    def test_create_link_post(self):
        r = self.cli.post('http://127.0.0.1:8000/api/create',
                          data=json.dumps({"link_to":"https://github.com/rast1ch/link-shorter"}),
                          content_type='application/json')
        self.assertEqual(301, r.status_code)