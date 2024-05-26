from django.contrib import auth
from rest_framework import viewsets, mixins, permissions, decorators
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserRegistSerializer, UserLoginSerializer

# Create your views here.
class UserResistViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistSerializer
    permission_classes = (permissions.AllowAny,)

    @decorators.action(detail=False, methods=['post'])
    def regist(self, req):
        """
        作成処理
        """
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


class UserLoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    @decorators.action(detail=False, methods=['post'])
    def login(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(req, **serializer.validated_data)

            if not user or not user.is_active:
                return Response('認証に失敗したか、削除されたユーザーです', status=400)
            
            auth.login(req, user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    @decorators.action(detail=False, methods=['post'])
    def login_token(self, req):
        """
        セッショントークンを用いてログインする
        """
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(req, **serializer.validated_data)

            if not user or not user.is_active:
                return Response('認証に失敗したか、削除されたユーザーです', status=400)
            
            token = Token.objects.get_or_create(user=user)  # 認証ユーザーを使ってトークンを生成
            return Response({'token': token[0].key}, status=200)
        return Response(serializer.errors, status=400)
    
    @decorators.action(detail=False, methods=['get'])
    def logout(self, req):
        auth.logout(req)
        return Response('ログアウト成功', status=200)
