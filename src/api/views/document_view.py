from math import atan2, cos, radians, sin, sqrt

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Document
from api.serializers import DocumentSerializer


class DocumentView(APIView):
    def post(self, request):
        """Create a new document"""
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Search for documents by keyword or phrase, optionally sorted by location"""
        keyword = request.query_params.get("keyword", None)
        latitude = request.query_params.get("latitude", None)
        longitude = request.query_params.get("longitude", None)

        if not keyword:
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
            lat = float(latitude)
            lon = float(longitude)

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

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
