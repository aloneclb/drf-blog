from pkg_resources import require
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('Bu emaile sahip kullanıcı zaten var.')
        if value == '':
            raise serializers.ValidationError('Lütfen emailinizi giriniz.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Parola Geçersiz Lütfen 8 haneden fazla karakter içeren parola giriniz.')
        return value  