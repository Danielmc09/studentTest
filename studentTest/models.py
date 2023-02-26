from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group, Permission


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def set_user_staff(sender, instance, created, **kwargs):
    if created:
        permission = Permission.objects.get(codename='view_answer')
        instance.is_staff = True
        instance.is_active = True
        instance.user_permissions.add(permission)
        instance.save()


class Test(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.answer_text
