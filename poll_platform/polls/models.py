from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models


# Атрибуты опроса: название, дата старта, дата окончания, описание.
class Poll(models.Model):
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateField(null=False, auto_now=True)
    finished_at = models.DateField(null=True)
    description = models.TextField()

    class Meta:
        app_label = "polls"

    def __str__(self):
        return f"""poll_title: {self.title},
                   start_date : {self.created_at},
                   end_date : {self.finished_at}
                   description : {self.description}"""


# Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта,
class PollQuestions(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("text", "Text"),
        ("choice", "Choice"),
        ("multiple_choices", "Multiple choices"),
    ]
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField(null=False)
    question_type = models.CharField(
        max_length=16, null=False, choices=QUESTION_TYPE_CHOICES
    )


class PollQuestionChoice(models.Model):
    question = models.ForeignKey(
        PollQuestions, on_delete=models.CASCADE, related_name="choices"
    )
    content = models.TextField(null=False)


class PollAnswer(models.Model):
    answer = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        PollQuestions, on_delete=models.CASCADE, related_name="answer"
    )

    def __str__(self):
        return f"""answer: {self.answer},
                   username : {self.user},
                   question : {self.question}"""