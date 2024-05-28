from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Persona
from .serializers import PersonaSerializer
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
        permission_classes = [permissions.AllowAny]  
        if command:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    columns = [col[0] for col in cursor.description] if cursor.description else []  # Check if cursor.description is not None
                    resultados = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                    response = Response(resultados, status=status.HTTP_200_OK)
                    response["Access-Control-Allow-Origin"] = "*"
                    return response  # Devolver los resultados como un JSON con las claves como nombres de columna
            except OperationalError as e:
                response = Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
                response["Access-Control-Allow-Origin"] = "*"             
                return response
        response = Response({"error":'No se proporcionó un comando SQL válido'}, status=status.HTTP_400_BAD_REQUEST)
        response["Access-Control-Allow-Origin"] = "*"
        return response