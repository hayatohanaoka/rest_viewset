from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Facility
from .serializers import FacilitySerializer

# Create your views here.
class FacilityViewSet(viewsets.ViewSet):

    def list(self, req):
        """
        一覧画面
        """
        queryset = Facility.objects.all()
        serializer = FacilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, req, pk=None):
        """
        詳細画面
        """
        queryset = Facility.objects.all()
        facility = get_object_or_404(queryset, pk=pk)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)
    
    def create(self, req):
        serializer = FacilitySerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.data, status=400)
