from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/' , include('Users.urls')),
    path('api/rooms/' , include('Rooms.urls')),
    path('api/messages/' , include('Messages.urls'))
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)