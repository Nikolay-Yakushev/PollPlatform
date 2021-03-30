from django.shortcuts import render

# Create your views here.
# Получение списка доступных опросов API for users/admins

# создание опроса Api for Admins
import random
from collections import defaultdict

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from polls.models import Poll, PollAnswer, PollQuestions
from polls.permissions import ActionsAdminPermission
from polls.serializers import (
    PollSerializer,
    PollAnswerSerializer,
    QuestionSerializer,
    AuthenticateUserSerializer,
    AnswerPostSerializer,
)


# Authentication for Users
class LoginPlatformView(APIView):
    serializer_class = AuthenticateUserSerializer

    queryset = User.objects

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = dict(status_logged=True)
        if request.user.is_authenticated:
            return Response(data=content, status=status.HTTP_200_OK)
        user = authenticate(request, **serializer.validated_data)
        if user:
            login(request, user)
            return Response(data=content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Poll for IsAdminUsers only
class PollCreateView(ListCreateAPIView):
    queryset = Poll.objects
    serializer_class = PollSerializer
    permission_classes = [ActionsAdminPermission]


#  Edit Polls
class PollActionsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.prefetch_related("questions")
    serializer_class = PollSerializer
    permission_classes = [ActionsAdminPermission]


# Создать Question for Admins
class QuestionCreateView(generics.CreateAPIView):
    queryset = PollQuestions.objects
    serializer_class = QuestionSerializer
    permission_classes = [ActionsAdminPermission]


class QuestionActionsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollQuestions.objects
    serializer_class = QuestionSerializer
    permission_classes = [ActionsAdminPermission]


# Passing Poll use this view :Api for users/admins
class PollPassView(RetrieveAPIView):
    queryset = Poll.objects.prefetch_related("questions")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AnswerPostSerializer
        elif self.request.method == "GET":
            return PollSerializer

    def get(self, request, *args, **kwargs):
        has_answered = Poll.objects.filter(
            Q(questions__answer__user=request.user) & Q(id=kwargs["pk"])
        ).exists()
        if has_answered:
            """Check if user has already answered poll"""
            response = reverse("PollResultsView")
            return HttpResponseRedirect(response)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kswargs):
        user_data = request.data
        serializer = AnswerPostSerializer(data=user_data)
        serializer.is_valid()
        user = request.user
        if not user.is_authenticated:
            number_ident = str(random.randint(100000, 999999))

            user = User.objects.create_user(
                username="anonym -" + number_ident,
                email=f"anonym@{number_ident}.com",
                password=number_ident,
            )
            login(self.request, user)
        for question_id, question_answer in user_data["answers"].items():
            PollAnswer.objects.create(
                user=user, question_id=question_id, answer=question_answer
            )
        return Response(status.HTTP_201_CREATED)


# получение списка ответов на вопросы
class PollResultsView(ListAPIView):
    queryset = PollAnswer.objects
    serializer_class = PollAnswerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.filter(user=self.request.user)
            .select_related("question")
            .annotate(
                poll_id=F("question__poll_id"),
                poll_name=F("question__poll__title"),
                question_text=F("question__question_text"),
                question_type=F("question__question_type"),
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        result = defaultdict(list)
        for item in serializer.data:
            result[
                "poll_id: "
                + str(item["poll_id"])
                + ""
                + "; Poll title: "
                + item["poll_name"]
            ].append(item)
        return Response(result)
