from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Persona
from .serializers import PersonaSerializer
import threading
from django.db import connection, OperationalError


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
            try:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    columns = [col[0] for col in cursor.description]  # Obtener los nombres de las columnas
                    resultados = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                    return Response(resultados, status=status.HTTP_200_OK)  # Devolver los resultados como un JSON con las claves como nombres de columna
            except OperationalError as e:                
                return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)  # Manejar el error de SQL
        return Response({"error":'No se proporcionó un comando SQL válido'}, status=status.HTTP_400_BAD_REQUEST)