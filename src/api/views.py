from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import decorators

from .models import Equipment, Facility
from .serializers import EquipmentSerializer, FacilitySerializer

# Create your views here.
class FacilityViewSet(viewsets.ViewSet):
    lookup_field = 'facility_id'

    def list(self, req):
        """
        一覧画面
        """
        queryset = Facility.objects.all()
        serializer = FacilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, req, facility_id=None):
        """
        詳細画面
        """
        queryset = Facility.objects.all()
        facility = get_object_or_404(queryset, id=facility_id)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)
    
    def create(self, req):
        serializer = FacilitySerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    # detail=False なので、詳細画面配下には付与されない
    @decorators.action(detail=False, methods=['get'])
    def filter_list(self, req):
        params = req.query_params
        if 'name' in params.keys():
            queryset = Facility.objects.filter(name__contains=params['name'])
            serializer = FacilitySerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'No such record.'})
    
    # detail=False なので、詳細画面配下に付与される
    @decorators.action(detail=True, methods=['get'])
    def custom_action(self, req, facility_id=None):
        return Response({'detail': 'テスト'})


class EquipmentViewSet(viewsets.GenericViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def list(self, req):
        """
        一覧画面
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, req):
        serializer = self.get_serializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
