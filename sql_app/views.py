from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Persona
from .serializers import PersonaSerializer
import threading
from django.db import connection


class ReadAll(APIView):
    def get(self, request):
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data)


class Create(APIView):
    def post(self, request, format=None):
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class mi_vista(APIView):
    def get(self, request, command):    
        if command:
            with connection.cursor() as cursor:
                cursor.execute(command)
                resultados = cursor.fetchall()
                return Response(str(resultados), status=status.HTTP_200_OK)  # Devolver los resultados como una respuesta HTTP con estado 200 OK
        return Response('No se proporcionó un comando SQL válido', status=status.HTTP_400_BAD_REQUEST)