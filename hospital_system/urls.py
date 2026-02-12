from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/user/login/', TokenObtainPairView.as_view()),
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),

    path('api/', include('patients.urls')),
]
