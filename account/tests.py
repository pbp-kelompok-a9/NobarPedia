from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Profile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Unit Tests ---

class AccountTestCase(TestCase):
    
    def setUp(self):
        # Set up a normal and admin user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin_user = User.objects.create_user(username='testadmin', password='password123')
        # Add admin permissions
        self.admin_user.user_permissions.add(
            Permission.objects.get(codename='view_user'), 
            Permission.objects.get(codename='change_user'), 
            Permission.objects.get(codename='delete_user')
        )
        # Create profiles 
        Profile.objects.create(user=self.user)
        Profile.objects.create(user=self.admin_user)

    def test_profile_model_str(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_login_page_exists(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_page_exists(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_admin_dashboard_permissions(self):
        # Test unauthenticated access (redirects to login)
        response = self.client.get(reverse('account:account_admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account:login'), response.url)
        
        # Test non-admin access (redirects to homepage)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('account:account_admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage:show_homepage'))
        
        # Test admin access (status code 200)
        self.client.login(username='testadmin', password='password123')
        response = self.client.get(reverse('account:account_admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_admin_dashboard.html')

    def test_nonexistent_page(self):
        response = self.client.get('/account/nonexistent-page-123/')
        self.assertEqual(response.status_code, 404)