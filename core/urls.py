from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # drf Auth

    path('__debug__/', include('debug_toolbar.urls')), # Django Debug Toolbar

    path('', include('post.urls', namespace='post')),

    path('api/', include('post_api.urls', namespace='post_api')),

    path('api/members/', include('members_api.urls', namespace='members_api')), # Register Url

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Djangorestfremawork SimpleJWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Djangorestfremawork SimpleJWT
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

