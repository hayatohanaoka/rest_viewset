from rest_framework import serializers

from .models import CustomUser

class UserRegistSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
    
    username = serializers.CharField()
    email = serializers.EmailField()
    age = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('パスワードが一致しません')
        return data
    
    def save(self):
        user = CustomUser.objects.create_user(
            username= self.validated_data['username'],
            password= self.validated_data['password'],
            email= self.validated_data['email'],
            age= self.validated_data['age']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        data_keys = data.keys()
        if 'email' not in data_keys or 'password' not in data_keys:
            raise serializers.ValidationError('入力項目が不足しています')
        return data
