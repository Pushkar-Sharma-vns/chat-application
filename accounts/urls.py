from django.urls import path

from .views import SignupView, LoginView, UserRetrieveAPIView

urlpatterns = [
    path('users/signup/', SignupView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('user/', UserRetrieveAPIView.as_view(), name='user_data'),
]
