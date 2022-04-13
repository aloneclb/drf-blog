from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
    
    def validate(self, data):
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError('Bu emaile sahip kullanıcı zaten var.')
        
        return data
