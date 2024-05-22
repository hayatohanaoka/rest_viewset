from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import decorators, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Equipment, Facility, FacilityType
from .serializers import (
    EquipmentSerializer,
    FacilitySerializer,
    FacilityTypeSerializer,
    UserRegistSerializer,
    UserLoginSerializer,
    UserUpdateSerializer
)
from .paginations import EquipmentPagination

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
        """
        Facility レコードの作成
        """
        serializer = FacilitySerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def destroy(self, req, facility_id=None):
        """
        Facility レコードの削除
        """
        queryset = Facility.objects.all()
        facility = get_object_or_404(queryset, id=facility_id)
        facility.delete()
        return Response({'result': 'Delete Success'})
    
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


class EquipmentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    lookup_field = 'equipment_id'
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = EquipmentPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'facility__name')

    # def list(self, req):
    #     """
    #     一覧画面
    #     """
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    def retrieve(self, req, equipment_id=None):
        queryset = self.get_queryset()
        equipment = get_object_or_404(queryset, id=equipment_id)
        serializer = self.get_serializer(equipment)
        return Response(serializer.data)
    
    def create(self, req):
        """
        Equipment レコードの作成
        """
        serializer = self.get_serializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
    
    def destroy(self, req, equipment_id=None):
        """
        Equipment レコードの削除
        """
        queryset = self.get_queryset()
        equipment = get_object_or_404(queryset, id=equipment_id)
        equipment.delete()
        return Response({'result': 'Delete Success'})


class FacilityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    model = FacilityType
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class UserViewSet(viewsets.ViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserRegistSerializer
    login_serializer_class = UserLoginSerializer
    update_serializer_class = UserUpdateSerializer
    lookup_field = 'user_id'

    def list(self, req):
        """
        一覧画面
        """
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, req, user_id=None):
        """
        詳細画面
        """
        queryset = get_object_or_404(self.queryset, id=user_id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=['post'])
    def regist(self, req):
        """
        作成処理
        """
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=404)

    @decorators.action(detail=False, methods=['patch'])
    def patch_profile(self, req):
        """
        更新処理
        """
        serializer = self.update_serializer_class(
            context={'user': req.user},
            data=req.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @decorators.action(detail=False, methods=['post'])
    def login(self, req):
        """
        認証処理
        """
        serializer = self.login_serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(
                request=req,
                username=req.data['username'],
                password=req.data['password']
            )

            if not user:
                return Response(serializer.errors, status=401)
            
            auth.login(req, user)
            return Response(serializer.data, status=200)
        return Response(serializer.data, status=400)
