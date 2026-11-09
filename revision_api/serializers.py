from rest_framework import serializers
from .models import RevisionSession


class RevisionSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RevisionSession
        fields = '__all__'