from django.contrib import admin
from .models import Student, Test, Question, Answer


# A class that is used to display the answers in the admin page.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'student', 'answer_text']
    ordering = ['id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            student = Student.objects.get(user__username=request.user)
            return qs.filter(student=student)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Question)
