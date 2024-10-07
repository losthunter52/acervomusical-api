from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Formacao


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_formacoes(request):

    formacoes = Formacao.objects.all()
    formacoes_data = []
    for formacao in formacoes:
        formacao_data = {
            'id': formacao.id,
            'descricao': formacao.descricao
        }
        formacoes_data.append(formacao_data)

    return Response(formacoes_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_formacao(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    descricao = data.get('descricao')

    formacao = Formacao.objects.create(descricao=descricao)

    return Response({"message": "Formacao creation success."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_formacao(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    try:
        formacao = Formacao.objects.get(id=id)
    except Formacao.DoesNotExist:
        return Response({"error": "Formacao not found."}, status=404)

    required_fields = ['descricao']

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    new_descricao = data.get('descricao')

    formacao.descricao = new_descricao
    
    formacao.save()
    return Response({"message": "Formacao updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_formacao(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        formacao = Formacao.objects.get(id=id)
    except Formacao.DoesNotExist:
        return Response({"error": "Formacao not found."}, status=404)

    formacao.delete()
    return Response({"message": "Formacao deleted successfully."}, status=200)
