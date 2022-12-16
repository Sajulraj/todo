
from rest_framework import serializers
from django.contrib.auth.models import User

from todolist.models import Todos

class TodoSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Todos
        fields=["id",
        "task_name",
        "user",
        "status"
        ]

    def create(self, validated_data):
        usr=self.context.get("user")
        return Todos.objects.create(**validated_data,user=usr)
#reg serializer 

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

