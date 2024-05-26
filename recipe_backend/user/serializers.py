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
