from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import RevisionSession
from .serializers import RevisionSessionSerializer
from .models import Question
from .serializers import QuestionSerializer


@api_view(['POST'])
def start_revision_session(request):

    data = request.data

    serializer = RevisionSessionSerializer(data=data)

    if serializer.is_valid():
        session = serializer.save()

        return Response(
            {
                "message": "Revision session started successfully",
                "session": RevisionSessionSerializer(session).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def save_questions(request):

    questions_data = request.data.get('questions', [])

    if not questions_data:
        return Response(
            {"error": "No questions provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = QuestionSerializer(
        data=questions_data,
        many=True
    )

    if serializer.is_valid():

        with transaction.atomic():
            saved_questions = serializer.save()

        return Response(
            {
                "message": "Questions saved successfully",
                "total_questions": len(saved_questions),
                "questions": QuestionSerializer(
                    saved_questions,
                    many=True
                ).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )