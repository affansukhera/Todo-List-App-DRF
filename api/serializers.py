from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

	class Meta:
		model = Task
		fields = ["id",'title', 'completed']

		extra_kwargs = {
			'id': {
				'required': False,
				'read_only':True,
			}
		}