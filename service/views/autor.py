from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Autor


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_autores(request):

    autores = Autor.objects.all()
    autores_data = []
    for autor in autores:
        autor_data = {
            'id': autor.id,
            'nome': autor.nome
        }
        autores_data.append(autor_data)

    return Response(autores_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_autor(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = ['nome']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    nome = data.get('nome')

    autor = Autor.objects.create(nome=nome)

    return Response({"message": "Autor creation success."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_autor(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    try:
        autor = Autor.objects.get(id=id)
    except Autor.DoesNotExist:
        return Response({"error": "Autor not found."}, status=404)

    required_fields = ['nome']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    new_nome = data.get('nome')

    autor.nome = new_nome
    
    autor.save()
    return Response({"message": "Autor updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_autor(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        autor = Autor.objects.get(id=id)
    except Autor.DoesNotExist:
        return Response({"error": "Autor not found."}, status=404)

    autor.delete()
    return Response({"message": "Autor deleted successfully."}, status=200)
