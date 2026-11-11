from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import RevisionSession
from .serializers import (RevisionSessionSerializer,QuestionSerializer,AnswerAttemptSerializer)
from .models import Question


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

import re


@api_view(['GET'])
def get_questions(request):

    topic_id = request.query_params.get('topic_id')

    if not topic_id:
        return Response(
            {"error": "Topic ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    questions = Question.objects.filter(
        topic_id=topic_id,
        is_active=True
    ).order_by('question_id')

    unique_questions = []
    seen_questions = set()

    for question in questions:

        # Normalize question text
        normalized_text = re.sub(
            r'\s+',
            ' ',
            question.question_text.lower().strip()
        )

        # Remove punctuation for comparison
        normalized_text = re.sub(
            r'[^\w\s]',
            '',
            normalized_text
        )

        if normalized_text not in seen_questions:

            seen_questions.add(normalized_text)
            unique_questions.append(question)

    serializer = QuestionSerializer(
        unique_questions,
        many=True
    )

    return Response({
        "total_questions": len(unique_questions),
        "questions": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_answer_attempt(request):

    data = request.data.copy()

    session_id = data.get('session')
    question_id = data.get('question')
    selected_answer = data.get('selected_answer', '').strip()
    time_taken = data.get('time_taken')

    if not session_id or not question_id or not selected_answer:
        return Response(
            {"error": "Required answer details are missing"},
            status=status.HTTP_400_BAD_REQUEST
        )

    question = Question.objects.filter(
        question_id=question_id,
        is_active=True
    ).first()

    if not question:
        return Response(
            {"error": "Question not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    correct_answer = question.correct_answer.strip().upper()[0]
    selected = selected_answer.upper()[0]

    data['is_correct'] = selected == correct_answer

    serializer = AnswerAttemptSerializer(data=data)

    if serializer.is_valid():
        attempt = serializer.save()

        return Response(
            {
                "message": "Answer saved successfully",
                "is_correct": attempt.is_correct,
                "attempt": AnswerAttemptSerializer(attempt).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )