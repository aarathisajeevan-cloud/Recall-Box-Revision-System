from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import RevisionSession
from .serializers import RevisionSessionSerializer


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
# Create your views here.
