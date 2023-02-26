from django.urls import path
from .views import LoginView, AnswerView

app_name = 'student_test'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('answer/', AnswerView.as_view(), name='answer'),
]
