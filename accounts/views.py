from django.contrib.auth import login

from rest_framework import views, permissions, status, response, generics

from .serializers import UserSignupSerializer, LoginSerializer, UserSerializer
from .models import User
# Create your views here.

class SignupView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data ,status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=400)
    
class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer
    
    def post(self, request):
        # import ipdb; ipdb.set_trace()
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(serializer.data, status=200)
    
class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data, status=200)

        