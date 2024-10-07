from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Imagem

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_imagem(request):

    imagem_file = request.FILES.get('imagem')

    if not imagem_file:
        return Response({"error": "No image file provided."}, status=400)

    imagem = Imagem.objects.create(arquivo=imagem_file)

    return Response({"message": "Image upload successfully.", "id": imagem.id, "imagem_url":imagem.arquivo.url}, status=201)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_imagem(request, id):
    try:
        imagem = Imagem.objects.get(id=id)

    except Imagem.DoesNotExist:
        return Response({"error": "Imagem not found."}, status=404)

    imagem.delete()
    return Response({"message": "Imagem deleted successfully."}, status=200)
