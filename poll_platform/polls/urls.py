from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from polls.views import (
    QuestionCreateView,
    PollCreateView,
    PollActionsView,
    QuestionActionsView,
    PollPassView,
    PollResultsView,
    LoginPlatformView,
)

urlpatterns = [
    path("auth/", LoginPlatformView.as_view(), name="LoginPlatformView"),
    path("polls/", PollCreateView.as_view(), name="PollCreateView"),
    path("polls/<int:pk>", PollActionsView.as_view(), name="PollActionsView"),
    path("questions/", QuestionCreateView.as_view(), name="QuestionCreateView"),
    path(
        "questions/<int:pk>", QuestionActionsView.as_view(), name="QuestionActionsView"
    ),
    path("polls/<int:pk>/pass/", PollPassView.as_view(), name="PollPassView"),
    path("polls_results/", PollResultsView.as_view(), name="PollResultsView"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
