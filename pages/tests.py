from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def test_url_exist_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'HomePage')
        self.assertTemplateUsed(response, 'home.html')
        
class AboutPageTest(TestCase):
    def test_url_exist_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_aboutpage_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AboutPage')
        self.assertTemplateUsed(response, 'about.html')
        
        