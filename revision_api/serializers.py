from rest_framework import serializers
from .models import RevisionSession, Question


# Serializer for Revision Session
class RevisionSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RevisionSession
        fields = '__all__'


# Serializer for Questions
class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'