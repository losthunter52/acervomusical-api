from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Partitura, Autor, Genero, Formacao, Edicao, Imagem
from datetime import datetime


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_partituras(request):
    if not request.user.groups.filter(name__in=['admin', 'user']).exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    partituras = Partitura.objects.all().order_by('-ultima_atualizacao')
    partituras_data = []
    for partitura in partituras:

        partitura_data = {
            'id': partitura.id,
            'autor': {
                'id': partitura.autor.id,
                'nome': partitura.autor.nome
            },
            'genero': {
                'id': partitura.genero.id,
                'descricao': partitura.genero.descricao
            },
            'titulo': partitura.titulo,
            'formacao': {
                'id': partitura.formacao.id,
                'descricao': partitura.formacao.descricao
            },
            'edicao': {
                'id': partitura.edicao.id,
                'descricao': partitura.edicao.descricao
            },
            'observacao': partitura.observacao,
            'sequencia': partitura.sequencia,
            'ultima_atualizacao': partitura.ultima_atualizacao
        }
            
        if(partitura.imagem != None):
            partitura_data['imagem'] = {'id': partitura.imagem.id, 'imagem': partitura.imagem.arquivo.url}
        
        partituras_data.append(partitura_data)

    return Response(partituras_data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_partitura(request, id):
    if not request.user.groups.filter(name__in=['admin', 'user']).exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        partitura = Partitura.objects.get(id=id)
    except Partitura.DoesNotExist:
        return Response({"error": "Partitura não encontrada."}, status=404)

    partitura_data = {
            'id': partitura.id,
            'autor': {
                'id': partitura.autor.id,
                'nome': partitura.autor.nome 
            },
            'genero': {
                'id': partitura.genero.id,
                'descricao': partitura.genero.descricao
            },
            'titulo': partitura.titulo,
            'formacao': {
                'id': partitura.formacao.id,
                'descricao': partitura.formacao.descricao
            },
            'edicao': {
                'id': partitura.edicao.id,
                'descricao': partitura.edicao.descricao
            },
            'observacao': partitura.observacao,
            'sequencia': partitura.sequencia,
            'ultima_atualizacao': partitura.ultima_atualizacao
        }
        
    if(partitura.imagem != None):
        partitura_data['imagem'] = {'id': partitura.imagem.id, 'imagem': partitura.imagem.arquivo.url}

    return Response(partitura_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_partitura(request):
    
    if not request.user.groups.filter(name__in=['admin', 'user']).exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = [
        "autor",
        "genero",
        "titulo",
        "formacao",
        "edicao"
    ]

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    autor, created = Autor.objects.get_or_create(nome=data['autor']['nome'])
    genero, created = Genero.objects.get_or_create(descricao=data['genero']['descricao'])
    formacao, created = Formacao.objects.get_or_create(descricao=data['formacao']['descricao'])
    edicao, created = Edicao.objects.get_or_create(descricao=data['edicao']['descricao'])

    partitura = Partitura.objects.create(
        autor=autor,
        genero=genero,
        titulo=data.get('titulo'),
        formacao=formacao,
        edicao=edicao,
        observacao=data.get('observacao', None),
        sequencia=data.get('sequencia', None)
    )

    if 'imagem' in data:
        if not Imagem.objects.filter(id=data.get('imagem')["id"]).exists():
            return Response({"error": "Imagem not found."}, status=400)
        else:
            imagem = Imagem.objects.get(id=data.get('imagem')["id"])
            partitura.imagem = imagem

    partitura.save()

    return Response({"message": "Partitura created successfully."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_partitura(request, id):
    if not request.user.groups.filter(name__in=['admin', 'user']).exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = [
        "autor",
        "genero",
        "titulo",
        "formacao",
        "edicao"
    ]
    
    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    try:
        partitura = Partitura.objects.get(id=id)
    except Partitura.DoesNotExist:
        return Response({"error": "Partitura not found."}, status=404)
    
    autor, created = Autor.objects.get_or_create(nome=data['autor']['nome'])
    genero, created = Genero.objects.get_or_create(descricao=data['genero']['descricao'])
    formacao, created = Formacao.objects.get_or_create(descricao=data['formacao']['descricao'])
    edicao, created = Edicao.objects.get_or_create(descricao=data['edicao']['descricao'])

    partitura.autor=autor
    partitura.genero=genero
    partitura.titulo=data.get('titulo')
    partitura.formacao=formacao
    partitura.edicao=edicao
    partitura.observacao=data.get('observacao', None)
    partitura.sequencia=data.get('sequencia', None)

    partitura.imagem = None
                
    if 'imagem' in data:
        if not Imagem.objects.filter(id=data.get('imagem')["id"]).exists():
            return Response({"error": "Imagem not found."}, status=400)
        else:
            imagem = Imagem.objects.filter(id=data.get('imagem')["id"]).first()
            partitura.imagem = imagem

    partitura.observacao = data.get('observacao', None)

    partitura.save()

    return Response({"message": "Partitura updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_partitura(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        partitura = Partitura.objects.get(id=id)
    except Partitura.DoesNotExist:
        return Response({"error": "Partitura not found."}, status=404)

    partitura.delete()
    return Response({"message": "Partitura deleted successfully."}, status=200)
