from multiprocessing import context
from pickle import FALSE
from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from todolist.models import Todos
from todolist.serializer import TodoSerializer,RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
# Create your views here.

class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializers=TodoSerializer(qs,many=True)
        return Response(data=serializers.data)
    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        m_id=kw.get("pk")
        qs=Todos.objects.get(id=m_id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*args,**kw):
        m_id=kw.get("pk")
        Todos.objects.get(id=m_id).delete()
        return Response(data="deleted")
    def update(self,request,*args,**kw):
        m_id=kw.get("pk")
        obj=Todos.objects.get(id=m_id)[0]
        serializer=TodoSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        
from .custompermission import IsOwnwerPermission
class Todomodelviewset(ModelViewSet):
        
        authentication_classes=[authentication.BasicAuthentication]
        permission_classes=[IsOwnwerPermission]

        serializer_class=TodoSerializer
        queryset=Todos.objects.all()
        

        def get_queryset(self):
            return Todos.objects.filter(user=self.request.user)

        def create(self,request,*args,**kw):
            serializer=TodoSerializer(data=request.data,context={"user":request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.data)
        
        # def perform_create(self, serializer):
        #     serializer.save(user=self.request.user)

        # def create(self,request,*args,**kw):
        #     serializer=TodoSerializer(data=request.data)
        #     if serializer.is_valid():
        #         Todos.objects.create(**serializer.validated_data,user=request.user)
        #         return Response(data=serializer.data)
        #     else:
        #         return Response(data=serializer.data)
        

        # def list(self,request,*args,**kw):
        #     qs=Todos.objects.filter(user=request.user)
        #     serializers=TodoSerializer(qs,many=True)
        #     return Response(data=serializers.data)

        @action(methods=["GET"],detail=False)
        def pending_todos(self,request,*args,**kw):
            qs=Todos.objects.filter(status=False,user=request.user)
            serializer=TodoSerializer(qs,many=True)
            return Response(data=serializer.data)

        @action(methods=["GET"],detail=False)
        def completed_todos(self,request,*args,**kw):
            qs=Todos.objects.filter(status=True)
            serializer=TodoSerializer(qs,many=True)
            return Response(data=serializer.data)

        @action(methods=["POST"],detail=True)
        def mark_as_done(self,request,*args,**kw):
            m_id=kw.get("pk")
            qs=Todos.objects.get(id=m_id)
            qs.status=True
            qs.save()
            serializer=TodoSerializer(qs,many=False)
            return Response(data=serializer.data)


class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


    # def create(self, request, *args, **kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
        