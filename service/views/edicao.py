from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Edicao


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_edicoes(request):

    edicoes = Edicao.objects.all()
    edicoes_data = []
    for edicao in edicoes:
        edicao_data = {
            'id': edicao.id,
            'descricao': edicao.descricao
        }
        edicoes_data.append(edicao_data)

    return Response(edicoes_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_edicao(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    descricao = data.get('descricao')

    edicao = Edicao.objects.create(descricao=descricao)

    return Response({"message": "Edicao creation success."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_edicao(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    try:
        edicao = Edicao.objects.get(id=id)
    except Edicao.DoesNotExist:
        return Response({"error": "Edicao not found."}, status=404)

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    new_descricao = data.get('descricao')

    edicao.descricao = new_descricao
    
    edicao.save()
    return Response({"message": "Edicao updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_edicao(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        edicao = Edicao.objects.get(id=id)
    except Edicao.DoesNotExist:
        return Response({"error": "Edicao not found."}, status=404)

    edicao.delete()
    return Response({"message": "Edicao deleted successfully."}, status=200)
