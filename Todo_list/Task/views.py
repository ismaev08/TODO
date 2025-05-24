
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from django.db import transaction
from rest_framework import static

from .serializer import *


class TaskListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        title = serializer.validated_data['title']

        with transaction.atomic():
            task = Task.objects.create(title=title)
            task.save()
            return Response(data=TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
