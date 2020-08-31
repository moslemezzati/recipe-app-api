from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='moslem@gmail.com', password='password'):
  """Create a simple user"""
  return get_user_model().objects.create_user(email,password)

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

  def test_tag_str(self):
    """Test the tag string representation"""
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='Vegan'
    ) 

    self.assertEqual(str(tag), tag.name)