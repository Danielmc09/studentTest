from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, Answer, Question


# It takes a username and password, authenticates the user, and returns a JWT token
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        The function validates the username and password, authenticates the user, generates a JWT token,
        adds custom data to the token, and returns the token and custom data in a dictionary

        :param data: The data that was passed to the serializer
        :return: The return_data dictionary is being returned.
        """
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Debe proporcionar tanto el nombre de usuario como la contraseña.')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Las credenciales ingresadas son incorrectas.')

        if not user.is_active:
            raise serializers.ValidationError('El usuario está desactivado.')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return_data = {
            'username': username,
            'access': access_token,
            'message': 'Inicio de sesión exitoso.'
        }

        return return_data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer_text',)

    def validate_question(self, value):
        """
        If the question with the ID in the request doesn't exist, raise a validation error

        :param value: The value that is being validated
        :return: The question object.
        """
        try:
            question = Question.objects.get(pk=value.id)
        except Question.DoesNotExist:
            raise serializers.ValidationError(
                f'La pregunta con ID {value.id} no existe.'
            )

        return question

    def validate(self, data):
        """
        If the user is not a student, or if the student has already answered the question, then the
        serializer will raise a validation error

        :param data: The validated data from the serializer
        :return: The answer to the question.
        """
        user = self.context['request'].user

        student = Student.objects.get(user__username=user)
        if not student:
            raise serializers.ValidationError('Debe autenticarse como un estudiante para enviar respuestas.')

        if Answer.objects.filter(question=data['question'], student=student).exists():
            raise serializers.ValidationError('Ya has respondido esta pregunta antes.')

        return data

    def create(self, validated_data):
        """
        The function takes the validated data from the serializer and creates an answer object with the
        student field set to the student object associated with the user who made the request

        :param validated_data: The validated data from the serializer
        :return: The answer is being returned.
        """
        user = self.context['request'].user
        student = user.student

        answer = Answer(student=student, **validated_data)
        answer.save()

        return answer
