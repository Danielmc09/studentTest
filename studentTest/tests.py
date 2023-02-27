from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from model_bakery import baker

from .models import Question, Answer


# Create your tests here.


# It tests the login endpoint with valid and invalid credentials, and with missing fields
class LoginTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', first_name='Test',
                                             last_name='User')

    def test_login_valid_credentials(self):
        """
        It tests the login with valid credentials.
        """
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        """
        It tests the login with invalid credentials.
        """
        data = {'username': 'test_user', 'password': 'incorrect_password'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Las credenciales ingresadas son incorrectas.')

    def test_login_missing_fields(self):
        """
        It tests the login endpoint.
        """
        data = {'username': 'test_user'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Debe proporcionar tanto el nombre de usuario como la contraseña.')


# It tests the answer view.
class AnswerViewTestCase(APITestCase):
    def setUp(self):
        self.url = '/answer/'
        self.student = baker.make('Student')
        self.token = AccessToken.for_user(self.student.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_post_with_valid_data(self):
        """
        It creates a question and then creates an answer for that question.
        """
        question = baker.make('Question')
        data = {'question': question.id, 'answer_text': 'Answer text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)

    def test_post_with_invalid_question(self):
        """
        It tests the post method of the AnswerViewSet class.
        """
        data = {'question': 100, 'answer_text': 'Answer text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'La pregunta proporcionada no existe.')

    def test_post_with_answered_question(self):
        """
        It tests that a student can't answer the same question twice.
        """
        question = baker.make('Question')
        baker.make('Answer', question=question, student=self.student)
        data = {'question': question.id, 'answer_text': 'Answer text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ya has respondido esta pregunta antes.', response.data['detail']['non_field_errors'])


