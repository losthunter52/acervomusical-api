from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Genero


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_generos(request):

    generos = Genero.objects.all()
    generos_data = []
    for genero in generos:
        genero_data = {
            'id': genero.id,
            'descricao': genero.descricao
        }
        generos_data.append(genero_data)

    return Response(generos_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_genero(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    descricao = data.get('descricao')

    genero = Genero.objects.create(descricao=descricao)

    return Response({"message": "Genero creation success."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_genero(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    try:
        genero = Genero.objects.get(id=id)
    except Genero.DoesNotExist:
        return Response({"error": "Genero not found."}, status=404)

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    new_descricao = data.get('descricao')

    genero.descricao = new_descricao
    
    genero.save()
    return Response({"message": "Genero updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_genero(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        genero = Genero.objects.get(id=id)
    except Genero.DoesNotExist:
        return Response({"error": "Genero not found."}, status=404)

    genero.delete()
    return Response({"message": "Genero deleted successfully."}, status=200)
