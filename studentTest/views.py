from rest_framework import status
from rest_framework import serializers
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, AnswerSerializer

from .models import Question, Answer


# Create your views here.


# The LoginView class is a subclass of APIView, which is a subclass of View
class LoginView(APIView):
    STATUS_OK = status.HTTP_200_OK
    STATUS_BAD_REQUEST = status.HTTP_400_BAD_REQUEST

    def post(self, request):
        """
        If the serializer is valid, return the validated data. If the serializer is not valid, return a
        message with the error

        :param request: The request object
        :return: The validated data.
        """
        serializer = LoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=self.STATUS_OK)

        except serializers.ValidationError as error:
            if 'password' in error.detail:
                message = 'Debe proporcionar tanto el nombre de usuario como la contraseña.'
            elif 'non_field_errors' in error.detail:
                message = 'Las credenciales ingresadas son incorrectas.'
            else:
                message = error.detail

            return Response({'detail': message}, status=self.STATUS_BAD_REQUEST)

        except Exception as error:
            return Response({'detail': str(error)}, status=self.STATUS_BAD_REQUEST)


# It's a view that receives a POST request with a JSON body containing a question id and an answer
# text, and it returns a JSON response with a message and a list of questions
class AnswerView(APIView):
    permission_classes = [IsAuthenticated]
    STATUS_CREATED = status.HTTP_201_CREATED
    STATUS_BAD_REQUEST = status.HTTP_400_BAD_REQUEST

    def post(self, request):
        """
        It takes a request, validates it, saves it, and returns a response

        :param request: The request object
        :return: A list of dictionaries.
        """
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'detail': 'Respuesta registrada correctamente.'}, status=self.STATUS_CREATED)
        except serializers.ValidationError as validation_error:
            if 'question' in validation_error.detail:
                questions = self._get_questions_list()
                return Response({
                    'detail': 'La pregunta proporcionada no existe.',
                    'questions_available': questions
                }, status=self.STATUS_BAD_REQUEST)
            else:
                return Response({'detail': validation_error.detail}, status=self.STATUS_BAD_REQUEST)

        except Exception as exception:
            return Response({'detail': str(exception)}, status=self.STATUS_BAD_REQUEST)

    def _get_questions_list(self):
        questions = Question.objects.all().values('id', 'question_text')
        return [{'id': q['id'], 'text': q['question_text']} for q in questions]
