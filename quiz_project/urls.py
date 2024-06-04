# In urls.py of your project (e.g., quiz_project/urls.py)
from django.contrib import admin
from django.urls import path, include  # Import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),  # Include the app's URL patterns
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
