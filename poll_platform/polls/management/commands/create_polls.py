from django.core.management.base import BaseCommand
from polls.models import *

POLLS_TITLES_DESCR = [
    dict(
        title="Президенты США",
        description="Опрос посвященный президентам США",
        questions=[
            {"question_text": "Как звали 44 президента США", "question_type": "text"},
            {
                "question_text": "Как звали первого президента США",
                "question_type": "choice",
                "choices": [
                    "Авраам Линкольн",
                    "Барак Обама",
                    "Рональд Рейган",
                    "Джордж Вашингтон",
                ],
            },
            {
                "question_text": "Кто из президентов США жил в 20 веке",
                "question_type": "multiple_choice",
                "choices": [
                    "Франклин Рузвельт",
                    "Рональд Рейган",
                    "Гарри Трумэн",
                    "Джон Тайлер",
                    "Джеймс Монро",
                ],
            },
        ],
    ),
    dict(
        title="Космос",
        description="Опрос посвященный достижениям человечества в космосе",
        questions=[
            {
                "question_text": "Как звали 2-го человека полетевшего в космос",
                "question_type": "choice",
                "choices": [
                    "Авраам Линкольн",
                    "Рональд Рейган",
                    "Герман Титов",
                    "Нил Армстронг",
                ],
            },
            {
                "question_text": "Самый мощный космический телескоп",
                "question_type": "text",
            },
            {
                "question_text": "Ракетоносители доставляющие комсмонатов на МКС",
                "question_type": "multiple choice",
                "choices": ["Союз", "Crew dragon", "Буран", "Одуванчик"],
            },
        ],
    ),
    dict(
        title="Россия",
        description="Опрос посвященный современной России",
        questions=[
            {
                "question_text": "Как звали 1-го председателя правителсьва России",
                "question_type": "text",
            }
        ],
    ),
]


class Command(BaseCommand):
    help = "Create Polls objects"

    def handle(self, *args, **options):
        for data in POLLS_TITLES_DESCR:
            questions = data.pop("questions")
            poll = Poll.objects.create(**data)
            for quest_data in questions:
                choices = quest_data.pop("choices", None)
                question = PollQuestions.objects.create(**quest_data, poll=poll)
                if choices:
                    for choice_content in choices:
                        PollQuestionChoice.objects.create(
                            content=choice_content, question=question
                        )
