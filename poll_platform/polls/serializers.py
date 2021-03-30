from rest_framework import serializers

from polls.models import Poll, PollQuestions, PollQuestionChoice, PollAnswer


class AuthenticateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PollChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestionChoice
        fields = "__all__"


class PollQuestionSerializer(serializers.ModelSerializer):
    choices = PollChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = PollQuestions
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    questions = PollQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"


class PollAnswerSerializer(serializers.ModelSerializer):
    poll_id = serializers.IntegerField()
    poll_name = serializers.CharField()
    question_text = serializers.CharField()
    question_type = serializers.CharField()

    class Meta:
        model = PollAnswer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestions
        fields = "__all__"


class AnswerPostSerializer(serializers.Serializer):
    answers = serializers.DictField()
