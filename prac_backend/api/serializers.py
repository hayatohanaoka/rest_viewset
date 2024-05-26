from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib import auth

from .models import Equipment, Facility, FacilityType, UserPicture

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id', 'name', 'detail')
        read_only_fields = ('id',)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'quantity', 'facility')
        read_only_fields = ('id',)


class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType
        fields = ('id', 'type', 'facility')
        read_only_fields = ('id',)


class UserRegistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def save(self, **kwargs):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data_keys = data.keys()
        if 'username' in data_keys and 'password' in data_keys:
            return data
        raise serializers.ValidationError('username と password は必須項目です')


class UserUpdateSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def save(self, **kwarg):
        user = self.context['user']
        data_keys = self.validated_data.keys()
        if 'username'   in data_keys: user.username   = self.validated_data['username']
        if 'email'      in data_keys: user.email      = self.validated_data['email']
        if 'first_name' in data_keys: user.first_name = self.validated_data['first_name']
        if 'last_name'  in data_keys: user.last_name  = self.validated_data['last_name']
        user.save()
        return user


class UserPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPicture
        fields = ('image',)
