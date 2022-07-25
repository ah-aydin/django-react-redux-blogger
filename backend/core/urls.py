from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('auth/tokens/', TokenObtainPairView.as_view(), name='auth-tokens'),
    path('auth/tokens/refresh/', TokenRefreshView.as_view(), name='auth-tokens-refresh'),

    # API
    path('api/user/', include('users.urls'))
]
