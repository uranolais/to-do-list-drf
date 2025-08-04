from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para usuários seguindo o princípio de responsabilidade única.
    Responsável apenas pela serialização de dados do usuário.
    """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }

    def validate(self, attrs):
        """Validação de senhas."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        """Criação de usuário com senha criptografada."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login seguindo o princípio de responsabilidade única.
    Responsável apenas pela autenticação.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validação de credenciais."""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')

        return attrs 