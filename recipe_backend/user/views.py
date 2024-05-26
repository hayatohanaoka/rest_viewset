from rest_framework.response import Response
from rest_framework import viewsets, mixins, permissions, decorators

from .serializers import UserRegistSerializer

# Create your views here.
class UserResistViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistSerializer

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
