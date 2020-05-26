from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.tests.helpers import create_user, DEFAULT_PASSWORD


class AccountTests(APITestCase):
    def test_create_url(self):
        """
        Ensure authenticated users can create URLs
        """
        user = create_user()
        url = reverse('url-list')
        self.client.login(username=user.username, password=DEFAULT_PASSWORD)
        data = dict(target='https://wfl.es')
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
 
    def test_anon_cant_create_url(self):
        """
        Ensure unauthenticated users can't create URLs
        """
        user = create_user()
        url = reverse('url-list')
        data = dict(target='https://wfl.es')
        resp = self.client.post(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_urls_cant_be_modified(self):
        """
        Ensure created URLS cant be changed
        """
        user = create_user()
        url = reverse('url-list')
        self.client.login(username=user.username, password=DEFAULT_PASSWORD)
        data = dict(target='https://wfl.es')
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        url = reverse('url-detail', args=(resp.json()['slug'],))
        data = dict(target='https://google.com')
        resp = self.client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_url_clicks_endpoint(self):
        """
        Ensure the url click-list is working for a given URL
        """
        user = create_user()
        url = reverse('url-list')
        self.client.login(username=user.username, password=DEFAULT_PASSWORD)
        data = dict(target='https://wfl.es')
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        url = reverse('click-list', args=(resp.json()['slug'],))
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 0)


    def test_url_redirect_must_create_a_click_object(self):
        """
        Ensure that a click object is created whened there is a URL redirect
        """
        user = create_user()
        url = reverse('url-list')
        self.client.login(username=user.username, password=DEFAULT_PASSWORD)
        data = dict(target='https://wfl.es')
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        slug = resp.json()['slug']

        url = reverse('redirect', args=(slug,))
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        
        url = reverse('click-list', args=(slug,))
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 1)