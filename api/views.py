from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.views import APIView
from .models import Task
from rest_framework import status


class TodoView(APIView):

	def get(self, request, *args, **kwargs):
		try:
			tasks = Task.objects.all()
			serializer = TaskSerializer(tasks, many=True)
			return Response({
				'status': 'success',
				'data': serializer.data
			}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({
				"Error":str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def post(self, request, *args, **kwargs):
		try:
			data = request.data
			serializer = TaskSerializer(data=data)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response({
					'status': 'success',
					'data': serializer.data
				}, status=status.HTTP_201_CREATED)
			else:
				return Response({
					'status': 'error',
					'data': serializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				"Error":str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def patch(self, request, *args, **kwargs):
		try:
			data = request.data
			id = data.get('id')

			try:
				task = Task.objects.get(id = id)
			except Task.DoesNotExist:
				return Response({
					'status': 'error',
					'data': 'Task not found'
				}, status=status.HTTP_400_BAD_REQUEST)

			serializer = TaskSerializer(task, data=data, partial=True)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response({
					'status': 'success',
					'data': serializer.data
				}, status=status.HTTP_200_OK)
			else:
				return Response({
					'status': 'error',
					'data': serializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				"Error":str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def put(self, request, *args, **kwargs):
		try:
			data = request.data
			id = data.get('id')

			try:
				task = Task.objects.get(id=id)
			except Task.DoesNotExist:
				return Response({
					'status': 'error',
					'data': 'Task not found'
				}, status=status.HTTP_400_BAD_REQUEST)

			serializer = TaskSerializer(task, data=data)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response({
					'status': 'success',
					'data': serializer.data
				}, status=status.HTTP_200_OK)
			else:
				return Response({
					'status': 'error',
					'data': serializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				"Error":str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def delete(self, request, *args, **kwargs):
		try:
			id = request.data
			task = Task.objects.get(id=id)
			task.delete()
		except Exception as e:
			return Response({
				"Error":str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')
