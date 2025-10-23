import logging
from math import atan2, cos, radians, sin, sqrt

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Document
from api.serializers import DocumentSerializer

logger = logging.getLogger(__name__)


class DocumentView(APIView):
    def post(self, request):
        """Create a new document"""
        try:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"Documento criado: {serializer.data.get('id')}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Erro de validação ao criar documento: {e.detail}")
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro inesperado ao criar documento: {str(e)}", exc_info=True)
            return Response(
                {"error": "Ocorreu um erro ao criar o documento."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        """Search for documents by keyword or phrase, optionally sorted by location"""
        try:
            keyword = request.query_params.get("keyword", None)
            latitude = request.query_params.get("latitude", None)
            longitude = request.query_params.get("longitude", None)

            if not keyword:
                logger.warning("Parâmetro 'keyword' ausente na requisição GET")
                return Response(
                    {"error": "Query parameter 'keyword' is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            documents = Document.objects.filter(
                Q(title__icontains=keyword)
                | Q(author__icontains=keyword)
                | Q(content__icontains=keyword)
            )

            if latitude and longitude:
                try:
                    lat = float(latitude)
                    lon = float(longitude)
                except ValueError:
                    logger.warning(
                        f"Latitude ou longitude inválidas: latitude={latitude}, longitude={longitude}"
                    )
                    return Response(
                        {"error": "Latitude and longitude must be valid numbers."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                def distance(doc):
                    if doc.latitude is None or doc.longitude is None:
                        return float("inf")
                    R = 6371.0
                    dlat = radians(doc.latitude - lat)
                    dlon = radians(doc.longitude - lon)
                    a = (
                        sin(dlat / 2) ** 2
                        + cos(radians(lat))
                        * cos(radians(doc.latitude))
                        * sin(dlon / 2) ** 2
                    )
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                    return R * c

                documents = sorted(documents, key=distance)
                logger.info(
                    f"Documentos ordenados por proximidade: lat={lat}, lon={lon}"
                )

            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"Erro inesperado ao buscar documentos: {str(e)}", exc_info=True
            )
            return Response(
                {"error": "Ocorreu um erro ao buscar os documentos."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
