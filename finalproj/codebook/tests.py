# TO RUN THE TESTS :
# manage.py test codebook.tests
# Create your tests here.

from django.test import TestCase
from django.test import Client

class Responses_200(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_response_200(self):
        #response_admin = self.client.get('/admin/')
        #self.assertEqual(response_admin.status_code, 200)

        response = self.client.get('/codebook/')
        print "Testing /codebook/ not logged in"
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/codebook/news')
        print "Testing /codebook/news not logged in"
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/codebook/watching')
        print "Testing /codebook/watching not logged in"
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/codebook/following')
        print "Testing /codebook/following not logged in"
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/codebook/saved')
        print "Testing /codebook/saved not logged in"
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/codebook/profile/nshoemaker')
        print "Testing /codebook/profile/nshoemaker not logged in"
        self.assertEqual(response.status_code, 200)