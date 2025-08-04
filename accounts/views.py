from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from accounts.serializers import UserSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    """
    View para registro de usuários seguindo o princípio de responsabilidade única.
    Responsável apenas pelo registro de novos usuários.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Criação de usuário com geração automática de token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Gerar token automaticamente
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    View para login seguindo o princípio de responsabilidade única.
    Responsável apenas pela autenticação.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    """
    View para logout seguindo o princípio de responsabilidade única.
    Responsável apenas pelo logout.
    """
    logout(request)
    return Response({'message': 'Logged out successfully'})
