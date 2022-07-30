from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT
    path('auth/tokens/', TokenObtainPairView.as_view(), name='auth-tokens'),
    path('auth/tokens/refresh/', TokenRefreshView.as_view(), name='auth-tokens-refresh'),

    # API
    path('api/user/', include('users.urls')),
    path('api/blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
