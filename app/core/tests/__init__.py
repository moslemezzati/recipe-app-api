from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

  def test_create_user_with_email_successful(self):
    """Test creating a new user with an email is successfult"""
    email = 'test@gmail.com'
    password = '2123123'
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )
    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
  
  def test_new_user_email_normalized(self):
    """Test the email for a new user is normalized"""
    email = 'test@GMAIL.com'
    user = get_user_model().objects.create_user(email, 'a;slkdfj;')

    self.assertEqual(user.email, email.lower())
  
  def test_new_user_invalid_email(self):
    """Test creating user with no email raises error"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'askdjf')

  def test_create_superuser(self):
    """Test creating superuser"""
    user = get_user_model().objects.create_superuser(
      'moslem@gmail.com', 
      'lksadfjlas'
      )
    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)