from django.urls import path, include
from .views import LoginAPIView, AdminLoginAPIView, RegisterUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', include([
        path('user/', LoginAPIView.as_view(), name='token_obtain_pair'),
        path('admin/', AdminLoginAPIView.as_view(), name='admin_token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    
    path('register/', include([
        path('user/', RegisterUserView.as_view(), name='register_user'),
    ])),
]